# ファイルハッシュ値比較
<#
    「使い方」
    引数にハッシュ計算したいファイルパスを渡してください。
    また、クリップボードにハッシュ値をコピーしておくと、比較して一致するかどうか判定します。
    クリップボードに入力がない場合、各種ハッシュ値を表示します。
#>

Param($path)

$clipBoard = Get-Clipboard

$getFileHash =
{
    Param($algorithm)
    Write-Host "（$algorithm）"
    (Get-FileHash $path -Algorithm $algorithm).Hash
}

$hashAlgorithm = @("MD5", "SHA1", "SHA256", "SHA384", "SHA512")
switch ($clipBoard.Length / 2)
{
    16 { $algorithm = $hashAlgorithm[0] }
    20 { $algorithm = $hashAlgorithm[1] }
    32 { $algorithm = $hashAlgorithm[2] }
    48 { $algorithm = $hashAlgorithm[3] }
    64 { $algorithm = $hashAlgorithm[4] }
}

if ($algorithm)
{
    $hash = & $getFileHash $algorithm
    if ($hash -eq $clipBoard)
    {
        "一致"
    }
    else
    {
        "不一致"
        "「$path」のハッシュ値"
        $hash
        "クリップボード内のハッシュ値"
        $clipBoard
    }
}
else
{
    foreach ($h in $hashAlgorithm) { & $getFileHash $h }
}

Read-Host