# inari-tool

ダイアログで選択した`144x384`サイズの画像のグリーンバック`RGB(0, 255, 0)`を透過するツールです。

> [!TIP]
> `144x384`以外のサイズを入力した場合、`144x384`にリサイズされます

## ビルド方法

uvをインストールした上でpowershellで以下のコマンドを実行してください。

```powershell
uv run python -m nuitka --standalone --onefile --enable-plugin=tk-inter --windows-console-mode=disable main.py -o "inari-tool"
```
