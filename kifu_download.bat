@powershell -NoProfile -ExecutionPolicy Unrestricted "&([ScriptBlock]::Create((cat -encoding utf8 \"%~f0\" | ? {$_.ReadCount -gt 2}) -join \"`n\"))" %*
@exit /b

# 7zip
$homepage="https://sevenzip.osdn.jp/"
$downloadpage=(wget $homepage|%{$_.Links}|?{$_.innerText -eq "ダウンロード"}|?{$_.href -match "download"}).href
$filehost=(wget $downloadpage|%{$_.Links}|?{$_.innerText -eq "ダウンロード"}|?{$_.href -match "7za"}).href
$7zaarchive=$filehost.split("/")[-2]
$fileref=(wget $filehost|%{$_.Links}|?{$_.href -match $7zaarchive+"$"}).href
$uri = New-Object System.Uri $filehost;
$downloadUrl = New-Object System.Uri ($uri,  ($fileref[0]).Replace('&amp;','&'))
wget -uri $downloadUrl -OutFile $7zaarchive
# Expand zip
Expand-Archive $7zaarchive
$7zaexe = (Get-Item $7zaarchive).BaseName+"/7za.exe"

# 棋譜 - 2018
$homepage="http://wdoor.c.u-tokyo.ac.jp/shogi/x/kifuarchive-daily/"
$links = Invoke-WebRequest -Uri $homepage|%{$_.Links}|?{$_.href -like "wdoor2018*.7z"}| Select-Object -ExpandProperty href
foreach($link in $links){
    $fileName = Split-Path $link -Leaf
    $kifuarchive = Join-Path (pwd) $fileName
    $uri = New-Object System.Uri $homepage;
    $downloadUrl = New-Object System.Uri ($uri, $link)
    Invoke-WebRequest -Uri $downloadUrl.AbsoluteUri -OutFile $kifuarchive
    # Expand 7z
    & "$7zaexe" x "$kifuarchive"
    del $kifuarchive
}

# del zip 7z
rmdir -recurse (Get-Item $7zaarchive).BaseName
del $7zaarchive

