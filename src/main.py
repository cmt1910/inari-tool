import os
import sys
from tkinter import Tk, filedialog, messagebox

from PIL import Image


def collect_cli_file_paths():
    """コマンドライン（ドラッグ＆ドロップ）で渡されたファイルを検証する"""
    args = sys.argv[1:]
    if not args:
        return None, []

    valid_paths = []
    errors = []
    for raw_path in args:
        normalized = os.path.abspath(raw_path)
        if not os.path.exists(normalized):
            errors.append((raw_path, "ファイルが見つかりません。"))
            continue
        if not os.path.isfile(normalized):
            errors.append((raw_path, "ファイルではありません。"))
            continue
        valid_paths.append(normalized)

    return valid_paths, errors


def get_program_dir() -> str:
    """配布物/実行ファイルが存在するディレクトリを返す（Nuitka対応）"""
    try:
        from __compiled__ import containing_dir  # type: ignore

        return containing_dir
    except Exception:
        return os.path.dirname(os.path.abspath(sys.argv[0]))


def get_unique_filename(directory, filename):
    """同名ファイルがあったら (2), (3)... と連番をつける"""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}({counter}){ext}"
        counter += 1
    return new_filename


def convert_image(file_path: str, output_dir: str) -> str:
    with Image.open(file_path) as opened:
        img = opened.convert("RGBA")

    datas = img.getdata()
    new_data = []
    for item in datas:
        r, g, b, a = item
        if g == 255 and r == 0 and b == 0:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)

    target_w, target_h = 144, 384
    src_w, src_h = img.size
    crop_box = (0, 0, min(target_w, src_w), min(target_h, src_h))
    cropped = img.crop(crop_box)

    if cropped.size != (target_w, target_h):
        canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        canvas.paste(cropped, (0, 0))
        result = canvas
    else:
        result = cropped

    base_name = os.path.basename(file_path)
    output_name = get_unique_filename(
        output_dir, os.path.splitext(base_name)[0] + ".png"
    )
    output_path = os.path.join(output_dir, output_name)
    result.save(output_path, "PNG")
    return output_path


def process_image(initial_paths=None, initial_errors=None):
    root = Tk()
    root.withdraw()

    try:
        errors = [] if initial_errors is None else list(initial_errors)

        if initial_paths is None:
            file_paths = filedialog.askopenfilenames(
                title="画像を選んでください",
                filetypes=[("画像ファイル", "*.png")],
            )
            if not file_paths:
                messagebox.showinfo("処理中止", "画像が選択されませんでした。")
                return
        else:
            file_paths = initial_paths
            if not file_paths and errors:
                error_lines = [
                    f"{os.path.basename(src)}: {msg}"
                    for src, msg in errors
                ]
                messagebox.showerror(
                    "エラー",
                    "ファイルを読み込めませんでした。\n\n" + "\n".join(error_lines),
                )
                return
            if not file_paths:
                messagebox.showinfo("処理中止", "画像が選択されませんでした。")
                return

        prog_dir = get_program_dir()
        output_dir = os.path.join(prog_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        success = []
        for file_path in file_paths:
            try:
                output_path = convert_image(file_path, output_dir)
                success.append((file_path, output_path))
            except Exception as exc:
                errors.append((file_path, str(exc)))

        if success:
            if len(success) == 1:
                _, output_path = success[0]
                messagebox.showinfo(
                    "変換完了", f"変換が完了しました！\n保存先: {output_path}"
                )
            else:
                lines = [
                    f"{os.path.basename(src)}: {dst}" for src, dst in success
                ]
                message = [
                    f"{len(success)}件の画像を変換しました。",
                    "保存先:",
                    *lines,
                ]
                messagebox.showinfo("変換完了", "\n".join(message))

        if errors:
            error_lines = [
                f"{os.path.basename(src)}: {msg}" for src, msg in errors
            ]
            messagebox.showerror(
                "エラー",
                "一部の画像でエラーが発生しました。\n\n" + "\n".join(error_lines),
            )

    except Exception as e:
        messagebox.showerror("エラー", f"処理中にエラーが発生しました。\n\n{e}")

    finally:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    cli_files, cli_errors = collect_cli_file_paths()
    if cli_files is None:
        process_image()
    else:
        process_image(cli_files, cli_errors)
