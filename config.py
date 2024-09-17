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

# 密钥
key = b'\x16a\xca\xa7\xa4\n\xef\xc72{\x85\x88HJ\x1e3'

# 版本号
VERSION = "1.1.0"


def encrypt(plain_text):
    """
    加密
    :param plain_text: 明文
    :return: 密文
    """
    global key
    # 创建 AES 加密对象
    cipher = AES.new(key, AES.MODE_EAX)

    # 加密数据并生成认证标签
    nonce = cipher.nonce
    cipher_text, tag = cipher.encrypt_and_digest(plain_text.encode())

    # 返回 nonce, tag 和密文
    return base64.b64encode(nonce + tag + cipher_text).decode()


def decrypt(encrypted_text):
    """
    解密
    :param encrypted_text: 密文
    :return: 加密
    """
    # 解码 base64 编码的加密数据
    encrypted_data = base64.b64decode(encrypted_text)

    # 分割 nonce, tag 和密文
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    cipher_text = encrypted_data[32:]

    # 创建 AES 解密对象
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # 解密并验证数据
    try:
        plain_text = cipher.decrypt_and_verify(cipher_text, tag)
        return plain_text.decode()
    except ValueError:
        return "Incorrect decryption"


def generate_config_file(entry1: tk.Entry, entry2: tk.Entry, entry3: tk.Entry, separate_subjects: int) -> None:
    """
    生成配置文件
    """
    if entry1.get() == '' or entry2.get() == '' or entry3.get() == '':
        showerror("错误", "不能留空")
        return None
    try:
        f = int(entry3.get())
    except ValueError:
        showerror("错误", "这不是数字")
        return None
    name_list = entry1.get().split(entry2.get())
    show_name = ""
    for i in name_list:
        show_name += i + " "
    if not askyesno("提示", f"检测到{len(name_list)}个名字，是否继续？\n{show_name}"):
        return None
    if askyesno("提示", "是否加入当堂老师？"):
        name_list.append("当堂老师")
    data = {"name_list": name_list,
            "version": VERSION,
            "Separate_subjects": separate_subjects,
            "Feedback_intensity": int(entry3.get()),
            "语文": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "数学": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "英语": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "物理": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "化学": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "生物": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "历史": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "政治": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "地理": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "其他": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))], "uncalled_times": [0 for j in range(len(name_list))]},
            "init_time": time.strftime("%Y年%b %d日 %a %H:%M:%S", time.localtime())}
    json_data = encrypt(json.dumps(data))
    # print(json.dumps(data))
    with open('record.dat', 'w', encoding='utf-8') as f:
        f.write(json_data)
        f.close()
    showinfo("提示",
             "配置文件生成成功！\n将 record.dat 放到点名器的同级目录，并保证该文件不被修改，点名器才能正常工作。\n如果点名器不能正常工作，请尝试重新生成配置文件或到\nhttps://gitee.com/Nept"
             "-Epslion/Adaptive-weight-random-roll-call/issues\n报告问题")


def show_data() -> None:
    """
    展示数据
    """
    pass


def analyse_config_file():
    """
    解析配置文件
    """
    file_path = filedialog.askopenfilename(title="选择配置文件", filetypes=(("配置文件", "*.dat"), ("所有文件", "*.*")))


def main() -> None:
    # A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z
    root = tk.Tk()
    root.title('随机点名配置文件生成器')
    root.geometry("240x240")
    # root.geometry("270x240")
    root.iconbitmap('favicon.ico')
    root.resizable(height=False, width=False)

    # 名单生成
    generation = tk.LabelFrame(root, text='生成配置文件')
    generation.grid(row=0, column=0, padx=2, columnspan=3)

    label1 = tk.Label(generation, text="请输入所有名字，使用分隔符分割名字：")
    label1.grid(row=0, column=0, pady=5, columnspan=3)

    entry1 = tk.Entry(generation, width=32)
    entry1.grid(row=1, column=0, padx=2, pady=5, columnspan=3)

    label2 = tk.Label(generation, text="请输入分隔符：")
    label2.grid(row=2, column=0, pady=5)

    entry2 = tk.Entry(generation, width=3)
    entry2.grid(row=2, column=1, pady=5)

    label3 = tk.Label(generation, text="请设置负反馈强度(建议2~4)：")
    label3.grid(row=3, column=0, pady=5)

    entry3 = tk.Entry(generation, width=3)
    entry3.grid(row=3, column=1, pady=5)

    ss = tk.IntVar()
    ss.set(0)

    check_button = tk.Checkbutton(generation, text="分科记录数据", variable=ss)
    check_button.grid(row=4, column=0)

    button1 = tk.Button(generation, text="生成",
                        command=lambda: generate_config_file(entry1, entry2, entry3, ss.get()))
    button1.grid(row=4, column=2, pady=3)

    # 解析名单
    # analyse = tk.LabelFrame(root, text='解析配置文件')
    # analyse.grid(row=4, column=0, padx=20, columnspan=3)
    #
    # button2 = tk.Button(analyse, text="解析文件", command=lambda: analyse_config_file())
    # button2.grid(row=4, column=0, pady=3)
    #
    # button3 = tk.Button(analyse, text="查看统计数据", command=lambda: show_data())
    # button3.grid(row=4, column=2, pady=3)

    root.mainloop()
    return None


if __name__ == "__main__":
    if "-ck" in sys.argv or '--create-key' in sys.argv:
        sys.exit(str(get_random_bytes(16)))
    main()
