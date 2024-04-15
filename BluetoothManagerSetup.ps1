# Ensure the script is running with administrative privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "You do not have Administrator rights to run this script! Please re-run as an Administrator."
    break
}

# Set Execution Policy to allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Install Python and pip if they are not already installed
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Output "Python is not installed. Installing Python..."
    # Installing Python; adjust the path and version as necessary
    Start-Process "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
}

# Check pip installation and install if necessary
$pipInstalled = Get-Command pip -ErrorAction SilentlyContinue
if (-not $pipInstalled) {
    Write-Output "Pip is not installed. Installing pip..."
    python -m ensurepip --upgrade
}

# Install required Python packages
Write-Output "Installing required Python packages..."
pip install -r requirements.txt

# Configuration file placement (if required)
$configPath = "config.yaml"
if (-not (Test-Path $configPath)) {
    Write-Output "Placing the configuration file..."
    Copy-Item -Path "config.yaml.template" -Destination $configPath
}

# Running the Bluetooth Manager script
Write-Output "Starting the Bluetooth Manager..."
python .\BluetoothManager.py

# Restore original execution policy if needed
Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser -Force
