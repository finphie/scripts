# ネットワークドライブ割り当て

<#
    「使い方」
    1. $path, $drive, $user, $fileを設定する。
    2. PowerShellを実行すると、ネットワークフォルダを割り当てます。
    3. もう一度実行すると、割り当てを解除します。
#>

using namespace System.Management.Automation

# ネットワークフォルダ（\\NAS\Shareなど）
$path = ""
# ドライブ名（Zなど）
$drive = "Z"
# ユーザー名
$user = "user"
# MakePasswordFile.ps1で作成したパスワードファイルのパス
$file = "password.txt"


$dir = Split-Path $MyInvocation.MyCommand.Path -parent
$file = Join-Path $dir $file
$driveName = $drive + ":"

if (Get-PSDrive | Where-Object {$_.Name -eq $drive})
{
    net use $driveName /delete
}
else
{
    $secure = Get-Content $file | ConvertTo-SecureString
    $cred = New-Object PSCredential $user,$secure

    New-PSDrive -Persist -Scope "Global" -Name $drive -PSProvider FileSystem -Root $path -Credential $cred
    
    Invoke-Item $driveName
}