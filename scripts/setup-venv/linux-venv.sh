#!/bin/bash

venv_name="ip-venv"
requirements_file="requirements.txt"

if [[ $0 == './script.sh' || $0 == 'script.sh' ]]; then
	cd ../..
fi

echo "Creating Virtual Environment '$venv_name'"
python3 -m venv $venv_name

echo "Activating virtual environment '$venv_name'"
. ./$venv_name/bin/activate

python3 -m ensurepip  # just a check

echo "Installing dependencies..."
if [[ -f $requirements_file ]]; then
	pip install -r $requirements_file
else
	echo "No requirements file found."
	exit
fi

deactivate
exit
