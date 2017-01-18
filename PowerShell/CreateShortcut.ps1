# ショートカット作成
<#
    「使い方」
    引数にファイルパスを指定すると、そのファイルのショートカットを作成します。
#>

using namespace System.Runtime.InteropServices

Param($path)

$name = (Read-Host "ショートカット名") + ".lnk"
$desktop = [Environment]::GetFolderPath([Environment+SpecialFolder]::DesktopDirectory)
$shortcutPath = Join-Path $desktop $name

$extension = (Get-Item $path).Extension.Substring(1)
switch ($extension)
{
    "ps1" { $arguments = "-File ""$path"""; $path = "powershell" }
}

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $path
if ($arguments) 
{
    $shortcut.Arguments = $arguments
}
$shortcut.Save()

[Marshal]::FinalReleaseComObject($wsh) | Out-Null
