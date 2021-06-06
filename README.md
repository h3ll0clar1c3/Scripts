# Scripts

* LocalAdmins.ps1 - Checks a file of host servers for members of the Administrators, Remote Desktop Users, and Users local groups.
* NSLookUp.ps1 - Runs a NSLookUp query against a file of host servers.
* PrivateIP - Runs a Nmap scan on against a file of host servers with Private IP's to check both TCP and UDP ports.
* PublicIP - Runs a Nmap scan on against a file of host servers with Public IP's to check both TCP and UDP ports.
* RunAs.ps1 - Runs a 'RunAs' command to switch context of user whilst triggering and initiating a reverse shell to the attacker.
* Meterpreter.rc - Sets a Meterpreter listener/handler with options (msfconsole -q -r Meterpreter.rc).
* WEPCracker.py - Wrapper script to crack WEP using Airdecap-ng.


### Local Admins

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


### WEP Cracker

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
    print "Trying with WEP Key: " +wepKey + " Hex: " + hexKey
    p = Popen(['/usr/bin/airdecap-ng', '-w', hexKey, 'WEP-Advanced.cap'], stdout=PIPE)
    output = p.stdout.read()
    finalResult = output.split('\n')[4]
    
    if finalResult.find('1') != -1 :
        print "Success WEP Key Found: " + wepKey
        sys.exit(0)
print "Failure! WEP Key Could not be Found with the existing dictionary!"
```

