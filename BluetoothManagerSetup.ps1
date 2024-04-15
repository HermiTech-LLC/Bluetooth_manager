# Set strict error handling
$ErrorActionPreference = "Stop"

# Setup logging
$logFile = "deploy_bluetooth_manager.log"
Start-Transcript -Path $logFile -Append
Write-Output "Deployment started at $(Get-Date)"

function ExecCmd {
    param([string]$command)
    Write-Host "+ $command" -ForegroundColor Cyan
    & powershell -Command $command
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE: $command"
    }
}

function CommandExists {
    param([string]$command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

Write-Host "Preparing to deploy the BluetoothManager package..."

# Ensure necessary tools and libraries are installed
Write-Host "Checking for required system tools..."

if (-not (CommandExists "python")) {
    Write-Host "Python is not installed, installing it..."
    Start-Process "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
}

if (-not (CommandExists "pip")) {
    Write-Host "pip is not installed, installing it..."
    ExecCmd "python -m ensurepip --upgrade"
}

# Ensure wheel and wxPython are installed for building packages
ExecCmd "pip install wheel wxPython"

# Check Bluetooth support service status and start if not running
$bluetoothService = Get-Service -Name bthserv -ErrorAction SilentlyContinue
if ($bluetoothService -eq $null) {
    Write-Host "Bluetooth service is not available on this system."
} elseif ($bluetoothService.Status -ne 'Running') {
    Write-Host "Starting Bluetooth support service..."
    Start-Service bthserv
} else {
    Write-Host "Bluetooth support service is already running."
}

# Setup and activate the virtual environment
Write-Host "Setting up the virtual environment..."
ExecCmd "python -m venv venv"
. .\venv\Scripts\Activate.ps1

# Install the package using setup.py located at the root
Write-Host "Installing the BluetoothManager package from the root directory..."
ExecCmd "pip install ."

# Verify the installation by attempting to import the package
Write-Host "Verifying the installation..."
$verify = { python -c "from BluetoothManager.manager import BluetoothManager; print('Import successful')" }
Invoke-Command -ScriptBlock $verify
if ($?) {
    Write-Host "Installation verified successfully."
} else {
    Write-Host "Failed to verify the installation. Check logs for details."
    exit 1
}

# Run the SynthDash.py application located at the root
Write-Host "Running the SynthDash.py wxPython dashboard..."
ExecCmd "python .\SynthDash.py"

Write-Host "Deployment completed successfully."

Stop-Transcript