# Copyright 2021 Acryl Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import subprocess
import os
import yaml
import json
import re
import logging
import asyncio
import time 
from collections import deque
from acryl.executor.execution.task import Task
from acryl.executor.execution.task import TaskError
from acryl.executor.result.execution_result import Type
from acryl.executor.context.executor_context import ExecutorContext
from acryl.executor.context.execution_context import ExecutionContext
from acryl.executor.common.config import ConfigModel, BaseModel
from acryl.executor.execution.task import TaskConfig
from acryl.executor.secret.secret_store import SecretStore, SecretStoreConfig
from acryl.executor.secret.secret_store_registry import SecretStoreRegistry
from typing import List

logger = logging.getLogger(__name__)

MAX_LOG_LINES = 2000

def _format_log_lines(lines: List[str]) -> str: 
    return "".join(lines)

class SubProcessIngestionTaskConfig(ConfigModel):
    tmp_dir: str = "/tmp/datahub/ingest"

class SubProcessIngestionTaskArgs(ConfigModel):
    recipe: str
    version: str

class SubProcessIngestionTask(Task):

    config: SubProcessIngestionTaskConfig
    tmp_dir: str # Location where tmp files will be written (recipes) 
    ctx: ExecutorContext

    @classmethod
    def create(cls, config: dict, ctx: ExecutorContext) -> "Task":
        config = SubProcessIngestionTaskConfig.parse_obj(config)
        return cls(config, ctx)

    def __init__(self, config: SubProcessIngestionTaskConfig, ctx: ExecutorContext):
        self.config = config
        self.tmp_dir = config.tmp_dir
        self.ctx = ctx 

    async def execute(self, args: dict, ctx: ExecutionContext) -> None:

        exec_id = ctx.exec_id # The unique execution id. 

        # 0. Validate arguments 
        validated_args = SubProcessIngestionTaskArgs.parse_obj(args)

        # 1. Resolve the recipe (combine it with others)
        recipe: dict = self._resolve_recipe(validated_args.recipe, ctx)

        # 2. Write recipe file to local FS (requires write permissions to /tmp directory)
        file_name: str = f"{exec_id}.yml"  
        self._write_recipe_to_file(self.tmp_dir, file_name, recipe)

        # 3. Spin off subprocess to run the run_ingest.sh script
        datahub_version = validated_args.version # The version of DataHub CLI to use. 
        plugins = recipe["source"]["type"] # The source type -- ASSUMPTION ALERT: This should always correspond to the plugin name. 
        command_script: str = "run_ingest.sh" # TODO: Make sure this is EXECUTABLE.  

        stdout_lines = deque(maxlen=MAX_LOG_LINES)

        # TODO: Inject a token into the recipe to run such that it "just works" (currently, a token is required)

        ingest_process = subprocess.Popen([command_script, exec_id, datahub_version, plugins, self.tmp_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        try: 
            while ingest_process.poll() is None:
                line = ingest_process.stdout.readline()

                sys.stdout.write(line)
                stdout_lines.append(line)
                await asyncio.sleep(0)

            return_code = ingest_process.poll()

        except asyncio.CancelledError:
            # Terminate the running child process 
            ingest_process.terminate()
            raise  

        finally:
            ctx.get_report().report_info(f"stdout={_format_log_lines(stdout_lines)}")
            
            # Cleanup by removing the recipe file
            self._remove_recipe_file(self.tmp_dir, file_name)

        if return_code != 0:
            # Failed
            ctx.get_report().report_info("Failed to execute 'datahub ingest'")
            raise TaskError("Failed to execute 'datahub ingest'") 
        
        # Report Successful execution
        ctx.get_report().report_info("Successfully executed 'datahub ingest'")


    def close(self) -> None:
        pass

    def _resolve_recipe(self, recipe: str, ctx: ExecutionContext):
        # Now attempt to find and replace all secrets inside the recipe. 
        secret_pattern = re.compile('.*?\${(\w+)}.*?')

        resolved_recipe = recipe
        secret_matches = secret_pattern.findall(resolved_recipe)

        # 1. Extract all secrets needing resolved. 
        secrets_to_resolve = [] 
        if secret_matches:
            for match in secret_matches:
                secrets_to_resolve.append(match)

        # 2. Resolve secret values
        secret_values_dict = self._resolve_secrets(secrets_to_resolve, self.ctx)

        # 3. Substitute secrets into recipe file
        if secret_matches:
            for match in secret_matches:
                # a. Check if secret was successfully resolved.
                secret_value = secret_values_dict.get(match)
                if secret_value is None:
                    # Failed to resolve secret. 
                    raise TaskError(f"Failed to resolve secret with name {match}. Aborting recipe execution.")
                    
                # b. Substitute secret value. 
                resolved_recipe = resolved_recipe.replace(
                    f'${{{match}}}', secret_value
                )

        json_recipe = json.loads(resolved_recipe)

        # Inject run_id into the recipe
        json_recipe["run_id"] = ctx.exec_id

        # TODO: Inject the ingestion source id as well.

        # For now expect that the recipe is complete, this may not be the case, however for hybrid deployments. Secret store!
        return json_recipe

    # TODO: move this to a utility class. 
    def _resolve_secrets(self, secret_names: List[str], ctx: ExecutorContext):
        # Attempt to resolve secret using by checking each configured secret store.
        secret_stores = ctx.get_secret_stores()
        final_secret_values = dict({})

        for secret_store in secret_stores:
            try: 
                # Retrieve secret values from the store. 
                secret_values_dict = secret_store.get_secret_values(secret_names)
                # Overlay secret values from each store, if not None. 
                for secret_name, secret_value in secret_values_dict.items():
                    if secret_value is not None:
                        final_secret_values[secret_name] = secret_value
            except Exception:
                logger.exception(f"Failed to fetch secret values from secret store with id {secret_store.get_id()}")
        return final_secret_values

    def _write_recipe_to_file(self, dir_path: str, file_name: str, recipe: dict):

        # 1. Create directories to the path
        os.makedirs(dir_path, mode = 0o777, exist_ok = True)

        # 2. Dump recipe dictionary to a YAML string
        yaml_recipe = yaml.dump(recipe)

        # 3. Write YAML to file  
        file_handle = open(dir_path + "/" + file_name, "w")
        n = file_handle.write(yaml_recipe)
        file_handle.close()

    def _remove_recipe_file(self, dir_path: str, file_name: str):
        # 1. Create abs file path
        file_path = dir_path + "/" + file_name

        # 2 remove path 
        os.remove(file_path)

