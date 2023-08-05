#!/bin/bash
# usage: ./run_ingest.sh <recipe-id> <datahub-version> <plugins-required> <tmp-dir>

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Create tmp file to store requirements using provided recipe id. 
req_file="$4/requirements-$1.txt"
touch $req_file
echo "acryl-datahub[datahub-rest,$3]==$2" > $req_file

venv_dir="$4/venv-$1"
python3 -m venv $venv_dir
source $venv_dir/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r $req_file
rm $req_file

# Execute DataHub recipe, based on the recipe id. 
if (python3 -m datahub ingest -c "$4/$1.yml"); then
  rm -r $venv_dir
  exit 0
else
  rm -r $venv_dir
  exit 1
fi