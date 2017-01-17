# 資格情報を作成

$cred = Get-Credential
$cred.password | ConvertFrom-SecureString | Set-Content "password.txt"