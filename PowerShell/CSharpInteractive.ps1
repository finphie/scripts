# C#スクリプトを実行する
<#
    「使い方」
    引数に実行したいC#スクリプトのパスを渡してください。
#>

Param($path)

$path = [System.IO.Path]::GetFullPath($path)

$csiPath = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\MSBuild\ToolsVersions" |
    Sort-Object {[double]$_.PSChildName} -Descending |
    Select-Object -First 1 |
    Get-ItemProperty -Name MSBuildToolsPath |
    Select-Object -ExpandProperty MSBuildToolsPath

Set-Location $csiPath
Invoke-Expression ".\csi.exe ""$path"""