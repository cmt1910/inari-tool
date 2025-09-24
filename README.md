# inari-tool

ダイアログで選択した`144x384`サイズの画像のグリーンバック`RGB(0, 255, 0)`を透過するツールです。
Windowsのみ動作を確認しています。

## 使い方

- 実行ファイルを通常起動するとダイアログが開き、変換したいPNGファイルを選択できます。
- 変換したいPNGファイルを`inari-tool.exe`にドラッグ＆ドロップしても同様に変換できます。複数ファイルのドロップにも対応しています。

> [!TIP]
> `144x384`以外のサイズを入力した場合、`144x384`にトリミングされます

## ビルド方法

uvをインストールした上でpowershellで以下のコマンドを実行してください。

```powershell
uv run python -m nuitka --standalone --onefile --enable-plugin=tk-inter --windows-console-mode=disable "./src/main.py" -o "inari-tool"
```
