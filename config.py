# -*- coding:utf-8 -*- #

from Crypto.Random import get_random_bytes
from tkinter.messagebox import *
from Crypto.Cipher import AES
import tkinter as tk
import base64
import time
import json
import sys


def main() -> None:
    def generate() -> None:
        if entry1.get() == '' or entry2.get() == '':
            showerror("错误", "不能留空")
            return None
        name_list = entry1.get().split(entry2.get())
        if not ('当堂老师' in name_list):
            name_list.append('当堂老师')
        data = {"name_list": name_list,
                "语文": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "数学": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "英语": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "物理": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "化学": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "生物": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "历史": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "政治": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "地理": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "其他": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
                "init_time": time.strftime("%Y年%b%d日 %a %H:%M:%S", time.localtime())}
        before_encrypt = json.dumps(data)
        key = base64.b64decode('ryGGCqRLpR9nEOS+LL5Duw==')
        cipher = AES.new(key, AES.MODE_EAX)
        # encrypted, tag =
        with open('record.dat', 'w', encoding='utf-8') as f:
            json.dump(data, f)
            f.close()
        showinfo("提示",
                 "将 record.dat 放到点名器的同级目录，并保证该文件不被修改，点名器才能正常工作。\n如果点名器不能正常工作，请尝试重新生成配置文件或到\nhttps://gitee.com/Nept"
                 "-Epslion/Adaptive-weight-random-roll-call/issues\n报告问题")
        sys.exit()

    root = tk.Tk()
    root.title('随机点名配置文件生成器')
    root.geometry("240x240")
    root.iconbitmap('favicon.ico')
    root.resizable(height=False, width=False)

    label1 = tk.Label(root, text="请输入所有名字，使用分隔符分割名字：")
    label1.grid(row=0, column=0, pady=5, columnspan=3)

    entry1 = tk.Entry(root, width=33)
    entry1.grid(row=1, column=0, pady=5, columnspan=3)

    label2 = tk.Label(root, text="请输入分隔符：")
    label2.grid(row=2, column=0, pady=5)

    entry2 = tk.Entry(root, width=3)
    entry2.grid(row=2, column=1, pady=5)

    button1 = tk.Button(root, text="生成", command=lambda: generate())
    button1.grid(row=3, column=2)

    root.mainloop()
    return None


if __name__ == "__main__":
    main()
