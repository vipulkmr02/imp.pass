$venv_name = "ip-venv"

Write-Host "Creating virtual environment '$venv_name'..."
python -m venv "$venv_name"

$activate_script = "$venv_name/Scripts/Activate.ps1"
Write-Host "Activating the virtual environment..."
. $activate_script

python3 -m ensurepip  # just a check

$requirements_file = "requirements.txt"
if (Test-Path $requirements_file) {
    Write-Host "Installing dependencies from '$requirements_file'..."
    pip install -r $requirements_file
} else {
    Write-Host "No '$requirements_file' found. quitting."
	exit
}

Write-Host "Virtual environment setup completed."
