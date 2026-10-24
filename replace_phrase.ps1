$old = "nhớ người đào giếng"
$new = "nhớ nguồn"
Get-ChildItem -Path . -Recurse -File | ForEach-Object {
    $path = $_.FullName
    $content = Get-Content -LiteralPath $path -Raw -ErrorAction SilentlyContinue
    if ($null -ne $content -and $content -like "*$old*") {
        $updated = $content -replace [regex]::Escape($old), $new
        Set-Content -LiteralPath $path -Value $updated -Encoding UTF8
        Write-Host "Updated $path"
    }
}

