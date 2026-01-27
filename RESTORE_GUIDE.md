# 状態を戻す手順ガイド

## 現在の状態について

現在の状態は以下のタグで保存されています：
- **タグ名**: `v1.0`
- **説明**: 基本機能完成版 - 戻りポイント
- **コミットID**: `ce2bd64`

## この状態に戻す方法

### 方法1: タグを使用して戻す（推奨）

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
git checkout v1.0
```

### 方法2: コミットIDを使用して戻す

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
git checkout ce2bd64
```

### 方法3: 最新のコミットに戻す

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
git checkout master
```

## 現在の状態を確認する方法

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
git log --oneline
git tag -l
```

## 変更を保存する方法

修正を加えた後、新しい状態を保存したい場合：

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
git add .
git commit -m "修正内容の説明"
```

## 注意事項

- 戻す前に、現在の変更を保存したい場合は、先にコミットしてください
- 戻すと、その時点以降の変更は失われます
- 変更を失いたくない場合は、新しいブランチを作成してから戻してください

## 新しいブランチを作成してから戻す方法（変更を保持したい場合）

```powershell
cd "C:\Users\ML-Y\Desktop\カーソル\fax_order"
# 現在の変更を新しいブランチに保存
git checkout -b backup-$(Get-Date -Format "yyyyMMdd-HHmmss")
git add .
git commit -m "バックアップ: 現在の状態"
# 元のブランチに戻る
git checkout master
# v1.0の状態に戻す
git checkout v1.0
```
