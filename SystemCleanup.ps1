# System Cleanup Script
# Removes temporary files, log files, and clears recycle bin to optimize system performance

Write-Host "Starting System Cleanup..." -ForegroundColor Green

# Function to delete files from a specified directory older than a certain number of days
function Cleanup-Files {
    param (
        [string]$Path,
        [int]$DaysOld = 7
    )
    if (Test-Path $Path) {
        Get-ChildItem -Path $Path -Recurse -File | Where-Object {
            $_.CreationTime -lt (Get-Date).AddDays(-$DaysOld)
        } | Remove-Item -Force -Verbose
    } else {
        Write-Host "Path $Path does not exist." -ForegroundColor Yellow
    }
}

# Cleaning Windows Temp folder
Write-Host "Cleaning Temp folder..." -ForegroundColor Cyan
Cleanup-Files -Path "$env:Temp" -DaysOld 7

# Cleaning system Temp folder
Write-Host "Cleaning System Temp folder..." -ForegroundColor Cyan
Cleanup-Files -Path "C:\Windows\Temp" -DaysOld 7

# Deleting old log files
Write-Host "Cleaning Log files..." -ForegroundColor Cyan
Cleanup-Files -Path "C:\Windows\Logs" -DaysOld 30
Cleanup-Files -Path "C:\ProgramData\Logs" -DaysOld 30

# Clearing Recycle Bin
Write-Host "Clearing Recycle Bin..." -ForegroundColor Cyan
Clear-RecycleBin -Confirm:$false -Verbose

Write-Host "System Cleanup Completed!" -ForegroundColor Green
