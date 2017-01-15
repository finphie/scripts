# 資格情報を作成

$cred = get-credential
$cred.password | ConvertFrom-SecureString | Set-Content "password.txt"