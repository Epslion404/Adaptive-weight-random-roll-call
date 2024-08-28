# -*- coding:utf-8 -*- #

import matplotlib.transforms as mtransforms
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
import ttkbootstrap as tbs
from pylab import mpl
import tkinter as tk
import numpy as np
import threading
import ctypes
import random
import base64
import copy
import time
import json
import sys
import os

# =================定义变量================= #

# name_list: list = str('将这个字符串替换为所有的名字，名字之间使用分隔符分隔').split('将这个字符串替换为名字之间的分隔符')
name_list: list = str('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z').split(' ')

init_time = ''

name: list = copy.deepcopy(name_list)

non_repeat_name: list = copy.deepcopy(name_list)

# 被抽到的频率
frequency: list = [0 for i in range(len(name_list))]

# 权重
weight: list = [1.0 for j in range(len(name_list))]

activated_f = False

# 根窗口
root = tk.Tk()

root1 = None

chart_exist = False

shown_name = tk.StringVar(value=random.choice(name))

pauseOrContinue = True

selected = None

enable_weight = tk.IntVar(value=1)

if_repeated = tk.IntVar()

check_box = None

check_box_text = tk.StringVar(value='{} / {}'.format(len(name), len(non_repeat_name)))

handle = {"control": 1}

NameSelect = []

NameSelect1 = []

SelectGroup = []

SelectGroup1 = []

is_setting_window_init = False

weight_name1 = []

# 负反馈力度
Feedback_intensity = 2


# =================定义函数================= #

def aes_encrypt(plaintext, key):
    """
    AES加密
    :param plaintext: 明文
    :param key: 秘钥
    :return: 密文
    """
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plaintext.encode(), AES.block_size)
    return cipher.encrypt(padded_data)


def aes_decrypt(ciphertext, key):
    """
    AES解密
    :param ciphertext: 密文
    :param key: 秘钥
    :return: 原文
    """
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = cipher.decrypt(ciphertext)
    return unpad(padded_data, AES.block_size).decode()


def cb1():
    global pauseOrContinue
    if pauseOrContinue == 0:
        pauseOrContinue = 1
    else:
        pauseOrContinue = 0
    return


def cb2():
    # print('cb2')
    global name1, weight_name1, NameSelect1, pauseOrContinue
    if not pauseOrContinue:
        pass
    else:
        name1 = copy.deepcopy(name)
        weight_name1 = copy.deepcopy(weight)
        for i in NameSelect1:
            i.set(1)


def flash_name() -> None:
    global pauseOrContinue, name, selected, if_repeated, name1, check_box_text, frequency, activated_f, weight, weight_name1, enable_weight, Feedback_intensity, Exit
    for i in name1:
        weight_name1.append(weight[name.index(i)])

    while True:
        if pauseOrContinue:
            if if_repeated.get() == 0:
                if enable_weight.get() == 1:
                    selected = random.choices(name, weights=weight, k=1)[0]
                else:
                    selected = random.choice(name)
                shown_name.set(selected)
            else:
                if enable_weight.get() == 1:
                    selected = random.choices(name1, weights=weight_name1, k=1)[0]
                else:
                    selected = random.choice(name1)
                shown_name.set(selected)
            if activated_f:
                activated_f = False
        else:
            if if_repeated.get() == 1:
                if selected in name1:
                    if NameSelect1 != []:
                        # print(NameSelect1)
                        NameSelect1[name_list.index(selected)].set(0)
                    name1.remove(selected)
                    activated_f = False
                if not name1:
                    random.seed(time.time())
                    name1 = copy.deepcopy(name)
            if not activated_f:
                frequency[name.index(selected)] += 1
                # print(frequency)
                total = 0
                average = (sum(frequency) / len(frequency)) + 1
                for i in frequency:
                    if i + 1 > average:
                        total += (1 / Feedback_intensity) / (i + 1)
                    elif i + 1 < average:
                        total += Feedback_intensity / (i + 1)
                    else:
                        total += 1 / (i + 1)
                for w, f in zip(range(len(weight)), frequency):
                    if f + 1 > average:
                        weight[w] = ((1 / Feedback_intensity) / (f + 1)) / total
                    elif f + 1 < average:
                        weight[w] = (Feedback_intensity / (f + 1)) / total
                    else:
                        weight[w] = (1 / (f + 1)) / total
                # print(weight)
                weight_name1 = []
                for i in name1:
                    weight_name1.append(weight[name.index(i)])
                # print(weight_name1)
                activated_f = True

        check_box_text.set('不重复({}/{})'.format(len(name1), len(name)))
        # print(len(name1), len(name))
        time.sleep(0.01)


def setting_window():
    global is_setting_window_init, root1

    if not is_setting_window_init:
        is_setting_window_init = True
        setting_window_init()
    else:
        if isinstance(root1, tk.Toplevel):
            root1.deiconify()


def setting_window_on_closing():
    global root1
    if isinstance(root1, tk.Toplevel):
        root1.withdraw()


def show_data():
    global chart_exist, init_time, frequency, weight, Feedback_intensity
    total = 0
    average = (sum(frequency) / len(frequency)) + 1
    for i in frequency:
        if i + 1 > average:
            total += (1 / Feedback_intensity) / (i + 1)
        elif i + 1 < average:
            total += Feedback_intensity / (i + 1)
        else:
            total += 1 / (i + 1)
    for w, f in zip(range(len(weight)), frequency):
        if f + 1 > average:
            weight[w] = ((1 / Feedback_intensity) / (f + 1)) / total
        elif f + 1 < average:
            weight[w] = (Feedback_intensity / (f + 1)) / total
        else:
            weight[w] = (1 / (f + 1)) / total

    y1 = np.array(frequency)
    y2 = np.array(weight)
    plt.figure('Data', figsize=(17, 7), dpi=100)
    rect1 = [0.05, 0.55, 0.92, 0.4]
    rect2 = [0.05, 0.06, 0.92, 0.4]
    ax1 = plt.axes(rect1)
    plt.bar(name_list, y1, color='green')
    plt.axhline(y=average - 1, color='r', label="AVERAGE")
    plt.ylim(bottom=0)
    plt.ylabel('频率')
    plt.grid(axis='y')
    plt.xticks(rotation=45, fontsize=9)
    ax1.set_xlim(-1.0, len(name_list) + 0.1)
    label1 = ax1.get_xticklabels()
    for label in label1:
        offset = mtransforms.ScaledTranslation(-1 / 72, 0.05, plt.gcf().dpi_scale_trans)
        label.set_transform(label.get_transform() + offset)

    ax2 = plt.axes(rect2)
    plt.bar(name_list, y2, color='red')
    plt.ylabel('权重')
    plt.grid(axis='y')
    plt.xticks(rotation=45, fontsize=9)
    ax2.set_xlim(-1.0, len(name_list) + 0.1)
    label2 = ax2.get_xticklabels()
    for label in label2:
        offset = mtransforms.ScaledTranslation(-1 / 72, 0.05, plt.gcf().dpi_scale_trans)
        label.set_transform(label.get_transform() + offset)
    ax2.text(1, 0.05, '纪录始于 ' + init_time, fontsize=10)
    plt.show()
    plt.cla()
    plt.close('all')
    chart_exist = False


def setting_window_init():
    global root1, NameSelect, name, SelectGroup, enable_weight, NameSelect1, SelectGroup1, chart_exist

    def inner_show_data():
        global chart_exist
        if not chart_exist:
            data = threading.Thread(target=show_data)
            data.setDaemon(True)
            data.start()
            chart_exist = True

    # https://www.cnblogs.com/zwnsyw/p/17426304.html
    root1 = tk.Toplevel(root, width=800, height=600)
    root1.resizable(height=False, width=False)
    root1.attributes('-topmost', True)
    root1.protocol("WM_DELETE_WINDOW", setting_window_on_closing)
    root1.iconbitmap(r'c:\favicon.ico')

    if handle["control"] == 0:
        return

    handle["control"] = 0

    SelectGroup = []
    SelectGroup1 = []
    length = len(name_list)

    name_group = tk.LabelFrame(root1, text='可重复组')
    name_group.grid(row=0, column=0, columnspan=3)

    for i in range(length):
        t = tk.IntVar()
        t.set(1)
        NameSelect.append(t)
        but = tk.Checkbutton(name_group, text=name_list[i], variable=NameSelect[i], command=cb4)
        but.grid(row=i // 3, column=i % 3)
        SelectGroup.append(but)

    name1_group = tk.LabelFrame(root1, text='不重复组')
    name1_group.grid(row=0, column=4, columnspan=3)

    for i in range(length):
        t = tk.IntVar()
        if name_list[i] in name1:
            t.set(1)
        else:
            t.set(0)
        NameSelect1.append(t)
        but = tk.Checkbutton(name1_group, text=name_list[i], variable=NameSelect1[i], command=cb5)
        but.grid(row=i // 3, column=i % 3)
        SelectGroup1.append(but)

    ret = tk.Button(root1, text="确认", command=setting_window_on_closing)
    ret.grid(row=length // 3 + 2, column=6)

    show_chat = tk.Button(root1, text="展示统计数据", command=lambda: inner_show_data())
    show_chat.grid(row=length // 3 + 1, column=0)

    reset_b = tk.Button(root1, text="恢复默认设置", command=cb3)
    reset_b.grid(row=length // 3 + 1, column=1)

    mode = tk.Checkbutton(root1, text='自适应权重随机模式', variable=enable_weight)
    mode.grid(row=length // 3 + 1, column=4)

    root1.mainloop()


def cb5():
    global NameSelect1, name_list, name1, weight_name1, weight
    for i in range(len(NameSelect)):
        if NameSelect1[i].get() == 1:
            if not (name_list[i] in name1):
                name1.append(name_list[i])
        if NameSelect1[i].get() == 0:
            if name_list[i] in name1:
                name1.remove(name_list[i])
    weight_name1 = []
    for i in name1:
        weight_name1.append(weight[name_list.index(i)])


def cb4():
    global NameSelect, name_list, name
    for i in range(len(NameSelect)):
        if NameSelect[i].get() == 1:
            if not (name_list[i] in name):
                name.append(name_list[i])
        if NameSelect[i].get() == 0:
            if name_list[i] in name:
                name.remove(name_list[i])


def cb3():
    os.remove('record.dat')
    sys.exit()


def closing():
    global root, root1, frequency, init_time
    root.destroy()
    with open(r'c:\record.dat', 'w', encoding='utf-8') as f:
        for i in name1:
            f.write(i + ';')
        f.write('\n')
        for i in frequency:
            f.write(str(i) + ';')
        f.write('\n' + init_time)
    sys.exit()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main() -> None:
    """
    初始化随机点名
    """
    global root, shown_name, name, selected, if_repeated, check_box_text, root1, NameSelect, non_repeat_name, check_box, frequency, init_time
    # 定义样式
    style = tbs.style.Style(theme='minty')
    top6 = style.master

    # 根窗口
    root.title('随机点名')
    root.geometry("0x0")
    root.iconbitmap(r'c:\favicon.ico')
    root.overrideredirect(True)

    # 加载窗口
    init_window = tk.Toplevel(root)
    init_window.title('随机点名')
    init_window.geometry("240x120+50+50")
    init_window.resizable(height=False, width=False)
    init_window.overrideredirect(True)

    # 加载窗口的文字
    label1 = tk.Label(init_window, text='加载中...', font=("黑体", 20, "bold"), relief=tk.RIDGE)
    label1.place(relx=0.1, rely=0.5)
    label1.pack(expand=True)

    # 检测配置文件是否存在
    if not os.path.exists('record.dat'):
        with open('record.dat', 'w', encoding='utf-8') as f:
            for i in name_list:
                f.write(i + ';')
            f.write('\n')
            for i in frequency:
                f.write(str(i) + ';')
            f.write('\n' + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

    # 读取配置文件
    with open('record.dat', 'r', encoding='utf-8') as f:
        try:
            read = f.read()
            name1 = str(read.split('\n')[0]).split(';')[:-1]
            # print(len(name1))
            temp: list = str(read.split('\n')[1]).split(';')[:-1]
            for i in range(len(frequency)):
                frequency[i] = int(temp[i])
            init_time = read.split('\n')[2]
        except:
            f.close()
            cb3()
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['axes.unicode_minus'] = False
    random.seed(time.time())

    root.geometry("240x120")
    root.resizable(height=False, width=False)
    root.attributes('-topmost', True)
    # root.attributes('-toolwindow', True)
    root.protocol("WM_DELETE_WINDOW", closing)
    init_window.destroy()
    root.overrideredirect(False)

    name_label = tk.Label(root, textvariable=shown_name, font=("黑体", 40, "bold"), relief=tk.RIDGE)
    name_label.place(relx=0.1, rely=0.5)
    name_label.pack(expand=True)

    button = tk.Button(root, text="暂停/继续", command=cb1)
    button.pack(expand=True)

    if_repeated = tk.IntVar()
    check_box_text = tk.StringVar(value='不重复({}/{})'.format(len(name1), len(name)))

    setting = tk.Button(root, text="自定义", command=setting_window)
    setting.pack(side=tk.LEFT)

    check_box = tk.Checkbutton(root, textvariable=check_box_text, variable=if_repeated)
    if_repeated.set(1)
    check_box.pack(expand=True, side=tk.LEFT)

    b_reset = tk.Button(root, text="重置", command=cb2)
    b_reset.pack(side=tk.LEFT)

    flash_name_thread = threading.Thread(target=flash_name)
    flash_name_thread.setDaemon(True)
    flash_name_thread.start()
    # print(NameSelect[0].get())
    root.mainloop()
    return None


if __name__ == "__main__":
    main()

text = 'hello world'
key = get_random_bytes(16)
b = aes_encrypt(text, key)
print(base64.b64encode(b))
print(base64.b64decode(base64.b64encode(b)) == b)
print(aes_decrypt(b, key))
