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

import time

from acryl.executor.request.execution_request import ExecutionRequest
from acryl.executor.request.signal_request import SignalRequest
from acryl.executor.execution.task import TaskConfig
from acryl.executor.dispatcher.default_dispatcher import DefaultDispatcher
from acryl.executor.execution.reporting_executor import ReportingExecutor, ReportingExecutorConfig
from acryl.executor.secret.datahub_secret_store import DataHubSecretStoreConfig
from acryl.executor.secret.secret_store import SecretStoreConfig
from datahub.ingestion.graph.client import DatahubClientConfig

# this is an integration test of the functionality, basically, manually verified  

if __name__ == "__main__":

    # Main function 

    # Build and register executors with the dispatcher
    local_task_config = TaskConfig(
        name="RUN_INGEST",
        type="acryl.executor.execution.sub_process_ingestion_task.SubProcessIngestionTask", 
        configs=dict({}))
    local_exec_config = ReportingExecutorConfig(
        id="default", 
        task_configs=[local_task_config],
        secret_stores=[
            SecretStoreConfig(type="env", config=dict({})),
            SecretStoreConfig(type="datahub", config=DataHubSecretStoreConfig(
                graph_client_config=DatahubClientConfig(
                    server="http://localhost:8080",
                    token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMSIsImV4cCI6MTY0MjIyMzE5MywianRpIjoiZjIwZjRmMmQtMThlNS00NTRmLTgyMzQtMTg1YzIxZjAwN2QzIiwic3ViIjoiZGF0YWh1YiIsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.e3N4_Z_3QhviYmLW8UXS2KhhcrBIMinDhSjnR05bMbE"
                )
            ))
        ],
        graph_client_config=DatahubClientConfig(
            server="http://localhost:8080",
            token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMSIsImV4cCI6MTY0MjIyMzE5MywianRpIjoiZjIwZjRmMmQtMThlNS00NTRmLTgyMzQtMTg1YzIxZjAwN2QzIiwic3ViIjoiZGF0YWh1YiIsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.e3N4_Z_3QhviYmLW8UXS2KhhcrBIMinDhSjnR05bMbE"
        )
    )
    local_executor = ReportingExecutor(local_exec_config)
    dispatcher = DefaultDispatcher([local_executor])

    endpoint = "http://localhost:8080/" # get from config
    args = {
        'recipe': "{\r\n            \"source\": {\r\n                \"type\": \"mysql\",\r\n                \"config\": {\r\n                    \"host_port\": \"${HOST_PORT}\",\r\n                    \"database\": \"${DATABASE}\",\r\n                    \"username\": \"${MYSQL_USERNAME}\",\r\n                    \"password\": \"${MYSQL_PASSWORD}\"\r\n                }\r\n            },\r\n            \"sink\": {\r\n                \"type\": \"datahub-rest\",\r\n                \"config\": {\r\n                    \"server\":\"http:\/\/localhost:8080\", \"token\":\"eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMSIsImV4cCI6MTY0MjIyMzE5MywianRpIjoiZjIwZjRmMmQtMThlNS00NTRmLTgyMzQtMTg1YzIxZjAwN2QzIiwic3ViIjoiZGF0YWh1YiIsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.e3N4_Z_3QhviYmLW8UXS2KhhcrBIMinDhSjnR05bMbE\"                \r\n                }\r\n            }\r\n        }"
    }

    exec_request = ExecutionRequest(exec_id="1234", name="RUN_INGEST", args=args)
    dispatcher.dispatch(exec_request)

    time.sleep(3)

    # Now kill the process. 
    signal_request = SignalRequest(exec_id="1234", signal="KILL")
    dispatcher.dispatch_signal(signal_request)


