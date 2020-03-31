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
