$ErrorActionPreference = "Stop"
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Desktop = [Environment]::GetFolderPath("Desktop")
    $ShortcutName = "FAX Order App.lnk"
    $ShortcutPath = [System.IO.Path]::Combine($Desktop, $ShortcutName)
    $TargetPath = "C:\Users\ML-Y\Desktop\カーソル\fax_order\FAX注文処理アプリ起動.bat"
    $WorkingDirectory = "C:\Users\ML-Y\Desktop\カーソル\fax_order"

    Write-Host "Creating shortcut at: $ShortcutPath"
    Write-Host "Target: $TargetPath"
    
    # 既存のショートカットを削除（存在する場合）
    if (Test-Path $ShortcutPath) {
        Remove-Item $ShortcutPath -Force
        Write-Host "Existing shortcut removed"
    }
    
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetPath
    $Shortcut.WorkingDirectory = $WorkingDirectory
    $Shortcut.Description = "FAX Order Processing App Launcher"
    $Shortcut.Save()

    Write-Host "Shortcut created successfully!"
    exit 0
} catch {
    Write-Host "Error: $_"
    Write-Host "Error details: $($_.Exception.Message)"
    exit 1
}
