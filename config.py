# -*- coding:utf-8 -*- #
from Crypto.Random import get_random_bytes
from tkinter.messagebox import *
from tkinter import filedialog
from Crypto.Cipher import AES
import tkinter as tk
import base64
import time
import json
import sys

key = b'\x16a\xca\xa7\xa4\n\xef\xc72{\x85\x88HJ\x1e3'
VERSION = "1.2.0"


def encrypt(plain_text: str) -> str:
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(plain_text.encode("utf-8"))
    return base64.b64encode(nonce + tag + cipher_text).decode("utf-8")


def decrypt(encrypted_text: str) -> str:
    encrypted_data = base64.b64decode(encrypted_text)
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    cipher_text = encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        plain_text = cipher.decrypt_and_verify(cipher_text, tag)
        return plain_text.decode("utf-8")
    except ValueError:
        return "Incorrect decryption"


def _validate_ratio(value: str, name: str) -> float | None:
    try:
        ratio = float(value)
    except ValueError:
        showerror("错误", f"{name} 必须是数字")
        return None
    if ratio <= 0:
        showerror("错误", f"{name} 必须大于 0")
        return None
    return ratio


def generate_config_file(entry1: tk.Entry, entry2: tk.Entry, entry3: tk.Entry,
                         entry_rf: tk.Entry, entry_ru: tk.Entry, separate_subjects: int) -> None:
    if entry1.get().strip() == '' or entry2.get() == '' or entry3.get() == '':
        showerror("错误", "不能留空")
        return

    try:
        feedback = int(entry3.get())
    except ValueError:
        showerror("错误", "负反馈强度必须是整数")
        return
    if feedback <= 0:
        showerror("错误", "负反馈强度必须为正整数")
        return

    ratio_f = _validate_ratio(entry_rf.get(), "频率比例")
    ratio_u = _validate_ratio(entry_ru.get(), "未点比例")
    if ratio_f is None or ratio_u is None:
        return
    total_ratio = ratio_f + ratio_u
    if abs(total_ratio - 1.0) > 1e-6:
        showerror("错误", "频率与未点比例之和必须为 1")
        return

    sep = entry2.get()
    raw_names = entry1.get().split(sep)
    name_list = [n.strip() for n in raw_names if n.strip() != '']
    if not name_list:
        showerror("错误", "未检测到有效名字")
        return

    show_name = " ".join(name_list)
    if not askyesno("提示", f"检测到 {len(name_list)} 个名字，是否继续？\n{show_name}"):
        return
    if askyesno("提示", "是否加入当堂老师？"):
        name_list.append("当堂老师")

    def _empty_stat():
        return {"non_repeat_name": name_list[:],
                "frequency": [0] * len(name_list),
                "uncalled_times": [0] * len(name_list)}

    data = {
        "name_list": name_list,
        "version": VERSION,
        "Separate_subjects": int(separate_subjects),
        "Feedback_intensity": feedback,
        "ratio_frequency": ratio_f,
        "ratio_uncalled": ratio_u,
        "init_time": time.strftime("%Y年%b %d日 %a %H:%M:%S", time.localtime()),
        "语文": _empty_stat(), "数学": _empty_stat(), "英语": _empty_stat(),
        "物理": _empty_stat(), "化学": _empty_stat(), "生物": _empty_stat(),
        "历史": _empty_stat(), "政治": _empty_stat(), "地理": _empty_stat(),
        "其他": _empty_stat(),
    }

    json_data = encrypt(json.dumps(data, ensure_ascii=False))
    with open('record.dat', 'w', encoding='utf-8') as f:
        f.write(json_data)

    showinfo(
        "提示",
        "配置文件生成成功！\n将 record.dat 放到点名器的同级目录，并保证该文件不被修改，点名器才能正常工作。\n"
        "如果点名器不能正常工作，请尝试重新生成配置文件或到\n"
        "https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/issues\n报告问题"
    )


def show_data() -> None:
    pass


def analyse_config_file():
    filedialog.askopenfilename(title="选择配置文件", filetypes=(("配置文件", "*.dat"), ("所有文件", "*.*")))


def main() -> None:
    root = tk.Tk()
    root.title('随机点名配置文件生成器')
    root.geometry("280x320")
    try:
        root.iconbitmap('favicon.ico')
    except Exception:
        pass
    root.resizable(height=False, width=False)

    generation = tk.LabelFrame(root, text='生成配置文件')
    generation.grid(row=0, column=0, padx=6, pady=4, columnspan=3, sticky='ew')

    tk.Label(generation, text="请输入所有名字，使用分隔符分割名字：").grid(row=0, column=0, pady=5, columnspan=3)
    entry1 = tk.Entry(generation, width=32)
    entry1.grid(row=1, column=0, padx=2, pady=5, columnspan=3)

    tk.Label(generation, text="请输入分隔符：").grid(row=2, column=0, pady=5, sticky='e')
    entry2 = tk.Entry(generation, width=4)
    entry2.grid(row=2, column=1, pady=5, sticky='w')

    tk.Label(generation, text="请设置负反馈强度(建议2~4)：").grid(row=3, column=0, pady=5, sticky='e')
    entry3 = tk.Entry(generation, width=4)
    entry3.grid(row=3, column=1, pady=5, sticky='w')

    tk.Label(generation, text="频率权重 r_f：").grid(row=4, column=0, pady=5, sticky='e')
    entry_rf = tk.Entry(generation, width=6)
    entry_rf.insert(0, "0.5")
    entry_rf.grid(row=4, column=1, pady=5, sticky='w')

    tk.Label(generation, text="未点权重 r_u：").grid(row=5, column=0, pady=5, sticky='e')
    entry_ru = tk.Entry(generation, width=6)
    entry_ru.insert(0, "0.5")
    entry_ru.grid(row=5, column=1, pady=5, sticky='w')

    ss = tk.IntVar(value=0)
    tk.Checkbutton(generation, text="分科记录数据", variable=ss).grid(row=6, column=0, sticky='w')

    tk.Button(generation, text="生成",
              command=lambda: generate_config_file(entry1, entry2, entry3, entry_rf, entry_ru, ss.get())
              ).grid(row=6, column=2, pady=3)

    root.mainloop()


if __name__ == "__main__":
    if "-ck" in sys.argv or '--create-key' in sys.argv:
        sys.exit(str(get_random_bytes(16)))
    main()