Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

Desktop = WshShell.SpecialFolders("Desktop")
ShortcutPath = Desktop & "\FAX注文処理アプリ起動.lnk"
TargetPath = "C:\Users\ML-Y\Desktop\カーソル\fax_order\FAX注文処理アプリ起動.bat"
WorkingDirectory = "C:\Users\ML-Y\Desktop\カーソル\fax_order"

' 既存のショートカットを削除
If fso.FileExists(ShortcutPath) Then
    fso.DeleteFile ShortcutPath, True
End If

Set Shortcut = WshShell.CreateShortcut(ShortcutPath)
Shortcut.TargetPath = TargetPath
Shortcut.WorkingDirectory = WorkingDirectory
Shortcut.Description = "FAX注文処理アプリを起動します"
Shortcut.Save()

WScript.Echo "ショートカットを作成しました: " & ShortcutPath
