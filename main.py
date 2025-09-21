import os
from tkinter import Tk, filedialog

from PIL import Image


def get_unique_filename(directory, filename):
    """同名ファイルがあったら (2), (3)... と連番をつける"""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}({counter}){ext}"
        counter += 1
    return new_filename


def process_image():
    # TkinterのGUIを非表示にする
    root = Tk()
    root.withdraw()

    # ユーザーに画像ファイルを選んでもらう
    file_path = filedialog.askopenfilename(
        title="画像を選んでください",
        filetypes=[("画像ファイル", "*.png")],
    )
    if not file_path:
        print("画像が選択されませんでした。")
        return

    # 画像を開く
    img = Image.open(file_path).convert("RGBA")
    datas = img.getdata()

    # グリーンバック透過処理
    new_data = []
    for item in datas:
        r, g, b, a = item
        # 緑っぽい色を透過にする（閾値は調整可能）
        if g == 255 and r == 0 and b == 0:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)

    # 144x384にリサイズ
    img = img.resize((144, 384), Image.NEAREST)

    # 出力先フォルダを固定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # 保存ファイル名を決定（元と同じ名前、被ったら連番）
    base_name = os.path.basename(file_path)
    output_name = get_unique_filename(
        output_dir, os.path.splitext(base_name)[0] + ".png"
    )
    output_path = os.path.join(output_dir, output_name)

    # PNGで保存
    img.save(output_path, "PNG")

    print(f"変換完了！ {output_path} に保存しました。")


if __name__ == "__main__":
    process_image()
