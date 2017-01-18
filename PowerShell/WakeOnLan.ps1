# Wake on LAN
<#
    「使い方」
    引数にMACアドレス（例.00-00-00-00-00-00）を渡してください。
#>

using namespace System.Net
using namespace System.Net.NetworkInformation
using namespace System.Net.Sockets

Param($macAddress)

# ポート（7, 9, 2304など）
$port = 2304

$header = [byte[]](@(0xFF)*6)
$macAddress = [PhysicalAddress]::Parse($macAddress).GetAddressBytes()
$magicPacket = $header + $macAddress * 16

$client = New-Object UdpClient
$target=[IPAddress]::Broadcast
$client.Connect($target, $port)
$client.Send($magicPacket, $magicPacket.Length) | Out-Null
$client.Close()