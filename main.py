# -*- coding:utf-8 -*- #
# 开始于 2024 年 3 月 17 日，15:10:45
# 该文件仅达到了能够使用的水平
# 可能存在各种BUG

import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from Crypto.Cipher import AES
import ttkbootstrap as tbs
import tkinter.messagebox
from pylab import mpl
import tkinter as tk
import numpy as np
import webbrowser
import threading
import ctypes
import random
import base64
import copy
import time
import json
import sys
import os

# 所有名字
# name_list: list = str('将这个字符串替换为所有的名字，名字之间使用分隔符分隔').split('将这个字符串替换为名字之间的分隔符')
name_list = []

# 数据记录的起始时间
init_time = ''

# 可重复组名单
repeatable_name = []

# 不重复组名单
unrepeatable_names = []

# 总频率
frequency: list = [0 for i in range(len(name_list))]

# 未被点名次数
uncalled_times: list = [0 for i in range(len(name_list))]

# 总权重
weight: list = [1.0 for j in range(len(name_list))]

# 跳过计算
skip_calculate = False

# 根窗口
root = tk.Tk()

# 自定义窗口
customize_window = None

# 数据是否已经显示
chart_exist = False

# 根窗口展示的名字
shown_name = tk.StringVar()

# 标志：是否开始滚动
pause_or_continue = True

selected = None

# 标志：是否启用动态权重模式
enable_weight = tk.IntVar(value=1)

# 标志：是否启用重复
none_repeat = tk.IntVar()

# "不重复模式"复选框
non_repeat_check_box = None

# "不重复模式"复选框文本
none_repeat_text = tk.StringVar(value=f'不重复({len(unrepeatable_names)}/{len(name_list)})')

# 记录可重复组名单启用情况
record_name_repeatable = []

# 记录不可重复组名单启用情况
record_name_unrepeatable = []

# 可重复组名单复选框
set_name_repeatable = []

# 不可重复组名单复选框
set_name_unrepeatable = []

# 标志：自定义窗口是否初始化
is_customize_window_init = False

# 不可重复组权重
unrepeatable_weight = []

# 负反馈力度
Feedback_intensity = 2

# 配置文件内容
DATA = {}

# 课堂选择
Subject = ''

# 悬浮图标窗口
float_window = None

# 根窗口状态
previous_state = 'normal'

# 打开图片
icon_image = Image.open("favicon.ico").resize((64, 64))
icon_photo = ImageTk.PhotoImage(icon_image)

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
        tkinter.messagebox.showerror("错误", "配置文件解析失败，请重新生成")
        exit_exe()


def inv_poc() -> None:
    """
    反转pauseOrContinue
    """
    global pause_or_continue
    pause_or_continue = not pause_or_continue
    return None


def reset_none_repeat() -> None:
    """
    重置不重复组名单
    """
    global unrepeatable_names, unrepeatable_weight, record_name_unrepeatable, pause_or_continue
    if not pause_or_continue:
        tkinter.messagebox.showerror("Error", "不能在暂停滚动时重置名单")
    else:
        unrepeatable_names = copy.deepcopy(repeatable_name)
        unrepeatable_weight = copy.deepcopy(weight)
        for i in record_name_unrepeatable:
            i.set(1)
    return None


def flash_name() -> None:
    global pause_or_continue, repeatable_name, selected, none_repeat, unrepeatable_names, none_repeat_text, frequency, skip_calculate, weight, unrepeatable_weight, enable_weight, uncalled_times

    # 同步权重
    for i in unrepeatable_names:
        unrepeatable_weight.append(weight[repeatable_name.index(i)])

    calculate_weight()

    while True:
        if pause_or_continue:
            # 如果是重复模式
            if none_repeat.get() == 0:
                # 如果使用动态权重调整模式
                if enable_weight.get() == 1:
                    selected = random.choices(repeatable_name, weights=weight, k=1)[0]
                else:
                    selected = random.choice(repeatable_name)
                shown_name.set(selected)
            else:  # 如果是不重复模式
                if enable_weight.get() == 1:
                    selected = random.choices(unrepeatable_names, weights=unrepeatable_weight, k=1)[0]
                else:
                    selected = random.choice(unrepeatable_names)
                shown_name.set(selected)
            if skip_calculate:
                skip_calculate = False
        else:
            # 如果是不重复模式
            if none_repeat.get() == 1:
                if selected in unrepeatable_names:
                    if len(record_name_unrepeatable) != 0:
                        # print(NameSelect1)
                        record_name_unrepeatable[name_list.index(selected)].set(0)
                    unrepeatable_names.remove(selected)
                    skip_calculate = False
                if not unrepeatable_names:
                    # random.seed(time.time())
                    unrepeatable_names = copy.deepcopy(repeatable_name)
            if not skip_calculate:
                frequency[repeatable_name.index(selected)] += 1
                for i in range(len(uncalled_times)):
                    uncalled_times[i] += 1
                uncalled_times[repeatable_name.index(selected)] -= 1
                # print(frequency)
                calculate_weight()
                skip_calculate = True

        none_repeat_text.set('不重复({}/{})'.format(len(unrepeatable_names), len(repeatable_name)))
        # print(len(name1), len(name))
        time.sleep(0.01)


def customize_windows() -> None:
    """
    启动自定义窗口
    """
    global is_customize_window_init, customize_window

    if not is_customize_window_init:
        is_customize_window_init = True
        customize_window_init()
    else:
        if isinstance(customize_window, tk.Toplevel):
            customize_window.deiconify()
    return None


def setting_window_on_closing() -> None:
    """
    关闭自定义窗口，实际上是隐藏
    """
    global customize_window
    if isinstance(customize_window, tk.Toplevel):
        customize_window.withdraw()
    return None


def calculate_weight() -> None:
    """
    计算权重
    """
    global frequency, weight, Feedback_intensity, unrepeatable_weight, unrepeatable_names, uncalled_times

    total_f = 0
    average_f = (sum(frequency) / len(frequency)) + 1
    for i in frequency:
        if i + 1 > average_f:
            total_f += (1 / Feedback_intensity) / (i + 1)
        elif i + 1 < average_f:
            total_f += Feedback_intensity / (i + 1)
        else:
            total_f += 1 / (i + 1)

    total_u = 0
    average_u = sum(uncalled_times) / len(uncalled_times) + 1
    for i in uncalled_times:
        if i > average_u:
            total_u += Feedback_intensity * (1 / (i + 1))
        elif i < average_u:
            total_u += (1 / Feedback_intensity) * (1 / (i + 1))
        else:
            total_u += 1 / (i + 1)

    for w, f, u in zip(range(len(weight)), frequency, uncalled_times):
        if f + 1 > average_f:
            weight[w] = (((1 / Feedback_intensity) / (f + 1)) / total_f) * 0.5 + (
                    Feedback_intensity * ((u + 1) / total_u)) * 0.5
        elif f + 1 < average_f:
            weight[w] = ((Feedback_intensity / (f + 1)) / total_f) * 0.5 + (
                    (1 / Feedback_intensity) * ((u + 1) / total_u)) * 0.5
        else:
            weight[w] = ((1 / (f + 1)) / total_f) * 0.5 + ((u + 1) / total_u) * 0.5

    unrepeatable_weight = []
    for i in unrepeatable_names:
        unrepeatable_weight.append(weight[repeatable_name.index(i)])
    return None


def show_data() -> None:
    """
    展示统计数据
    """
    global chart_exist, init_time, frequency, weight, Feedback_intensity, uncalled_times

    # print(uncalled_times)

    total_f = 0
    average_f = (sum(frequency) / len(frequency)) + 1
    for i in frequency:
        if i + 1 > average_f:
            total_f += (1 / Feedback_intensity) / (i + 1)
        elif i + 1 < average_f:
            total_f += Feedback_intensity / (i + 1)
        else:
            total_f += 1 / (i + 1)

    total_u = 0
    average_u = sum(uncalled_times) / len(uncalled_times) + 1
    for i in uncalled_times:
        if i > average_u:
            total_u += Feedback_intensity * (1 / (i + 1))
        elif i < average_u:
            total_u += (1 / Feedback_intensity) * (1 / (i + 1))
        else:
            total_u += 1 / (i + 1)

    for w, f, u in zip(range(len(weight)), frequency, uncalled_times):
        if f + 1 > average_f:
            weight[w] = (((1 / Feedback_intensity) / (f + 1)) / total_f) * 0.5 + (
                    Feedback_intensity * ((u + 1) / total_u)) * 0.5
        elif f + 1 < average_f:
            weight[w] = ((Feedback_intensity / (f + 1)) / total_f) * 0.5 + (
                    (1 / Feedback_intensity) * ((u + 1) / total_u)) * 0.5
        else:
            weight[w] = ((1 / (f + 1)) / total_f) * 0.5 + ((u + 1) / total_u) * 0.5

    y1 = np.array(frequency)
    y2 = np.array(uncalled_times)
    y3 = np.array(weight)

    # plt.figure(f'记录始于： {init_time}', figsize=(17, 7), dpi=100)
    # rect1 = [0.05, 0.55, 0.92, 0.4]
    # rect2 = [0.05, 0.06, 0.92, 0.4]
    #
    # ax1 = plt.axes(rect1)
    # plt.bar(name_list, y1, color='green', label="总体频率")
    # plt.axhline(y=average_f - 1, color='r', label="频率总体平均")
    # plt.ylim(bottom=0)
    # plt.ylabel('频率')
    # plt.grid(axis='y')
    # plt.xticks(rotation=45, fontsize=9)
    # ax1.set_xlim(-1.0, len(name_list) + 0.1)
    # plt.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    # label1 = ax1.get_xticklabels()
    # for label in label1:
    #     offset = mtransforms.ScaledTranslation(-1 / 72, 0.05, plt.gcf().dpi_scale_trans)
    #     label.set_transform(label.get_transform() + offset)
    #
    # ax2 = plt.axes(rect2)
    # plt.bar(name_list, y2, color='red')
    # plt.ylabel('权重')
    # plt.grid(axis='y')
    # plt.xticks(rotation=45, fontsize=9)
    # ax2.set_xlim(-1.0, len(name_list) + 0.1)
    # label2 = ax2.get_xticklabels()
    # for label in label2:
    #     offset = mtransforms.ScaledTranslation(-1 / 72, 0.05, plt.gcf().dpi_scale_trans)
    #     label.set_transform(label.get_transform() + offset)

    # plt.xticks(rotation=45, fontsize=9)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(17, 7), dpi=100, num=f'记录始于： {init_time}')

    # ax1.bar(np.arange(len(x)) - 0.2, y1, width=0.4, color='g', label='sin(x)')
    ax1.bar(np.arange(len(name_list)) - 0.2, y1, width=0.4, color="green", label="频率")
    ax1.set_ylabel("频率")
    ax1.set_ylim(bottom=0)
    ax1.set_xticks(np.arange(len(name_list)))
    ax1.set_xticklabels(name_list, fontsize=10, rotation=45)

    ax1_2 = ax1.twinx()
    ax1_2.bar(np.arange(len(name_list)) + 0.2, y2, width=0.4, color="blue", label='距离上次未被抽到的次数')
    ax1_2.set_ylabel('距离上次未被抽到的次数')
    ax1_2.set_ylim(bottom=0)

    ax1_2.axhline(y=average_f - 1, color='r', label="频率总体平均")

    # ax1.legend(loc="lower center", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    # 显示图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax1_2.get_legend_handles_labels()
    handles = handles1 + handles2
    labels = labels1 + labels2
    ax1.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)

    ax2.bar(name_list, y3, color="red", label="权重")
    ax2.set_ylabel("权重")
    ax2.set_ylim(bottom=0)
    ax2.set_xticklabels(name_list, fontsize=10, rotation=45)

    plt.tight_layout()
    plt.show()
    plt.cla()
    plt.close('all')
    chart_exist = False


def show_data_in_customize():
    """
    展示统计数据
    """
    global chart_exist
    if not chart_exist:
        data = threading.Thread(target=show_data)
        data.daemon = True
        data.start()
        chart_exist = True


def create_floating_icon() -> None:
    """
    创建悬浮窗
    """
    global float_window, root, icon_photo

    # 悬浮图标窗口
    float_window = tk.Toplevel()
    float_window.overrideredirect(True)  # 去掉窗口标题栏
    float_window.geometry(f"64x64+{root.winfo_x()}+{root.winfo_y()}")  # 图标窗口的大小和初始位置
    float_window.attributes("-topmost", True)  # 保持图标窗口在最前面
    float_window.focus_set()

    # 图标 Label
    icon_label = tk.Label(float_window, image=icon_photo)
    icon_label.pack(side=tk.LEFT)

    # 拖动功能
    def start_move(event):
        float_window.x = event.x
        float_window.y = event.y

    def on_move(event):
        x = float_window.winfo_x() + event.x - float_window.x
        y = float_window.winfo_y() + event.y - float_window.y
        float_window.geometry(f"+{x}+{y}")

    icon_label.bind("<Button-1>", start_move)
    icon_label.bind("<B1-Motion>", on_move)

    # 双击图标时恢复主窗口
    def on_double_click(event):
        root.deiconify()  # 恢复主窗口显示
        root.geometry(f"+{float_window.winfo_x()}+{float_window.winfo_y()}")
        float_window.destroy()  # 关闭悬浮窗口

    icon_label.bind("<Double-1>", on_double_click)
    return None


def check_window_state() -> None:
    """
    检查窗口状态的函数
    """
    global previous_state
    current_state = root.wm_state()  # 获取当前窗口状态

    if current_state == 'iconic' and previous_state != 'iconic':
        root.withdraw()  # 隐藏主窗口
        create_floating_icon()  # 显示悬浮图标

    previous_state = current_state
    root.after(100, check_window_state)
    return None


def customize_window_init() -> None:
    """
    初始化自定义窗口
    """
    global customize_window, record_name_repeatable, repeatable_name, set_name_repeatable, enable_weight, record_name_unrepeatable, set_name_unrepeatable, chart_exist, VERSION

    # 初始化自定义窗口
    customize_window = tk.Toplevel(root, width=800, height=600)
    customize_window.resizable(height=False, width=False)
    customize_window.title(f"随机点名 - 版本{VERSION}")
    customize_window.attributes('-topmost', True)
    customize_window.protocol("WM_DELETE_WINDOW", setting_window_on_closing)
    customize_window.iconbitmap('favicon.ico')

    set_name_repeatable = []
    set_name_unrepeatable = []
    length = len(name_list)

    # 自定义可重复组
    repeatable_name_group = tk.LabelFrame(customize_window, text='可重复组')
    repeatable_name_group.grid(row=0, column=0, columnspan=3)

    for i in range(length):
        t = tk.IntVar()
        t.set(1)
        record_name_repeatable.append(t)
        but = tk.Checkbutton(repeatable_name_group, text=name_list[i], variable=record_name_repeatable[i],
                             command=repeatable_name_group_update)
        but.grid(row=i // 3, column=i % 3)
        set_name_repeatable.append(but)

    unrepeatable_group_lf = tk.LabelFrame(customize_window, text='不重复组')
    unrepeatable_group_lf.grid(row=0, column=4, columnspan=3)

    for i in range(length):
        t = tk.IntVar()
        if name_list[i] in unrepeatable_names:
            t.set(1)
        else:
            t.set(0)
        record_name_unrepeatable.append(t)
        but = tk.Checkbutton(unrepeatable_group_lf, text=name_list[i], variable=record_name_unrepeatable[i],
                             command=unrepeatable_name_group_update)
        but.grid(row=i // 3, column=i % 3)
        set_name_unrepeatable.append(but)

    # 确认按钮
    return_to_root_button = tk.Button(customize_window, text="确认", command=setting_window_on_closing)
    return_to_root_button.grid(row=length // 3 + 4, column=6)

    # 关于
    about_label = tk.Button(customize_window, text="对本软件使用、转载、修改等请遵守开源协议")
    about_label.grid(row=length // 3 + 3, columnspan=4)

    gitee_link_label = tk.Button(customize_window, text="gitee", fg="blue", cursor="hand2",
                                 command=lambda: webbrowser.open_new(
                                     "https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/blob/master/LICENSE"))
    gitee_link_label.grid(row=length // 3 + 3, column=4)

    github_link_label = tk.Button(customize_window, text="github", fg="blue", cursor="hand2",
                                  command=lambda: webbrowser.open_new(
                                      "https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/blob/master/LICENSE"))
    github_link_label.grid(row=length // 3 + 3, column=5)

    # 展示统计数据按钮
    show_chat_button = tk.Button(customize_window, text="展示统计数据", command=show_data_in_customize)
    show_chat_button.grid(row=length // 3 + 1, column=0)

    adaptive_weight_mode = tk.Checkbutton(customize_window, text='自适应权重随机模式', variable=enable_weight)
    adaptive_weight_mode.grid(row=length // 3 + 1, column=4)

    customize_window.mainloop()


def unrepeatable_name_group_update():
    global record_name_unrepeatable, name_list, unrepeatable_names, unrepeatable_weight, weight
    for i in range(len(record_name_repeatable)):
        if record_name_unrepeatable[i].get() == 1:
            if not (name_list[i] in unrepeatable_names):
                unrepeatable_names.append(name_list[i])
        if record_name_unrepeatable[i].get() == 0:
            if name_list[i] in unrepeatable_names:
                unrepeatable_names.remove(name_list[i])
    unrepeatable_weight = []
    for i in unrepeatable_names:
        unrepeatable_weight.append(weight[name_list.index(i)])


def repeatable_name_group_update():
    global record_name_repeatable, name_list, repeatable_name
    for i in range(len(record_name_repeatable)):
        if record_name_repeatable[i].get() == 1:
            if not (name_list[i] in repeatable_name):
                repeatable_name.append(name_list[i])
        if record_name_repeatable[i].get() == 0:
            if name_list[i] in repeatable_name:
                repeatable_name.remove(name_list[i])


def on_root_closing() -> None:
    global root, customize_window, frequency, init_time, DATA, uncalled_times
    root.destroy()
    DATA[Subject]['non_repeat_name'] = unrepeatable_names
    DATA[Subject]['frequency'] = frequency
    DATA[Subject]['uncalled_times'] = uncalled_times
    # print(Subject, frequency)
    # print(DATA[Subject]['frequency'])
    with open('record.dat', 'w', encoding='utf-8') as f:
        f.write(encrypt(json.dumps(DATA)))
        f.close()
    exit_exe()


def exit_exe() -> None:
    """
    退出程序
    """
    if os.path.exists("running.dat"):
        os.remove("running.dat")
    sys.exit()


def main() -> None:
    """
    初始化随机点名
    """
    global root, shown_name, repeatable_name, selected, none_repeat, none_repeat_text, customize_window, record_name_repeatable, unrepeatable_names, non_repeat_check_box, frequency, init_time, pause_or_continue, DATA, Subject, name_list, repeatable_name, unrepeatable_names, shown_name, none_repeat_text, weight, uncalled_times, Feedback_intensity

    if os.path.exists('running.dat'):
        root.destroy()
        tkinter.messagebox.showinfo("提示", "随机点名已经在运行了")
        exit_exe()
    else:
        with open("running.dat", 'w') as f:
            f.write('?')
        ctypes.windll.kernel32.SetFileAttributesW('running.dat', 0x02)

    def class_select_cb(index: int):
        global Subject, DATA, unrepeatable_names, frequency, uncalled_times
        try:
            s = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理', '其他']
            Subject = s[index]
            unrepeatable_names = DATA[Subject]['non_repeat_name']
            frequency = DATA[Subject]['frequency']
            uncalled_times = DATA[Subject]['uncalled_times']
            if ss == 1:
                select_window.destroy()
        except Exception as e:
            tkinter.messagebox.showerror("错误", f'Error raised: {e}')
            exit_exe()
        # 设置根窗口
        root.geometry("240x120+0+0")
        root.resizable(height=False, width=False)
        root.attributes('-topmost', True)
        # root.attributes('-alpha', 0.2)
        # root.attributes('-toolwindow', True)
        root.protocol("WM_DELETE_WINDOW", on_root_closing)
        root.overrideredirect(False)

        flash_name_thread = threading.Thread(target=flash_name)
        flash_name_thread.daemon = True  # 守护模式
        flash_name_thread.start()

        check_window_state()
        root.mainloop()

    # 定义样式
    style = tbs.style.Style(theme='minty')
    top6 = style.master

    # 根窗口
    root.title('随机点名')
    root.geometry("0x0")
    root.overrideredirect(True)
    root.iconbitmap('favicon.ico')

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
        tkinter.messagebox.showerror("错误", "没有找到配置文件")
        exit_exe()

    # 读取配置文件
    with open('record.dat', 'r', encoding='utf-8') as f:
        try:
            DATA = json.loads(decrypt(f.read()))
            subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理', '其他']
            # for i in subjects:
            #     if len(DATA[i]) != 2:
            #         raise RuntimeError("Config file error")
            name_list = DATA["name_list"]
            init_time = DATA['init_time']
            ss = DATA["Separate_subjects"]
            Feedback_intensity = DATA["Feedback_intensity"]
            repeatable_name = copy.deepcopy(name_list)
            unrepeatable_names = copy.deepcopy(name_list)
            shown_name = tk.StringVar(value=random.choice(repeatable_name))
            none_repeat_text = tk.StringVar(value=f'不重复({len(unrepeatable_names)}/{len(name_list)})')
            weight = [1.0 for j in range(len(name_list))]
        except Exception as ex:
            tkinter.messagebox.showerror("错误", f'Error raised: {ex}')
            f.close()
            exit_exe()

    # 指定默认字体
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['axes.unicode_minus'] = False

    # 设置随机数种子
    random.seed(time.time())

    # 显示名字的标签
    name_label = tk.Label(root, textvariable=shown_name, font=("黑体", 40, "bold"), relief=tk.RIDGE)
    name_label.place(relx=0.1, rely=0.5)
    name_label.pack(expand=True)

    # 暂停/继续滚动按钮
    button = tk.Button(root, text="暂停/继续", command=inv_poc)
    button.pack(expand=True)

    # 置0
    none_repeat = tk.IntVar()
    none_repeat_text = tk.StringVar(value=f'不重复({len(unrepeatable_names)}/{len(name_list)})')

    # 自定义按钮
    customize_button = tk.Button(root, text="自定义", command=customize_windows)
    customize_button.pack(side=tk.LEFT)

    # 不重复复选框
    non_repeat_check_box = tk.Checkbutton(root, textvariable=none_repeat_text, variable=none_repeat)
    none_repeat.set(1)
    non_repeat_check_box.pack(expand=True, side=tk.LEFT)

    reset_button = tk.Button(root, text="重置", command=reset_none_repeat)
    reset_button.pack(side=tk.LEFT)

    init_window.destroy()  # 销毁加载窗口

    if ss == 0:
        class_select_cb(0)
    else:
        select_window = tk.Tk()
        select_window.geometry("180x120+50+50")
        select_window.resizable(height=False, width=False)
        select_window.attributes('-topmost', True)
        label1 = tk.Label(select_window, text='选择当堂科目', font=("黑体", 20, "bold"), relief=tk.RIDGE)
        label1.grid(row=0, columnspan=5, pady=5)
        button01 = tk.Button(select_window, text="语文", command=lambda: class_select_cb(0))
        button01.grid(row=1, column=0, pady=5)
        button02 = tk.Button(select_window, text="数学", command=lambda: class_select_cb(1))
        button02.grid(row=1, column=1, pady=5)
        button03 = tk.Button(select_window, text="英语", command=lambda: class_select_cb(2))
        button03.grid(row=1, column=2, pady=5)
        button04 = tk.Button(select_window, text="物理", command=lambda: class_select_cb(3))
        button04.grid(row=1, column=3, pady=5)
        button05 = tk.Button(select_window, text="化学", command=lambda: class_select_cb(4))
        button05.grid(row=1, column=4, pady=5)
        button06 = tk.Button(select_window, text="生物", command=lambda: class_select_cb(5))
        button06.grid(row=2, column=0, pady=5)
        button07 = tk.Button(select_window, text="历史", command=lambda: class_select_cb(6))
        button07.grid(row=2, column=1, pady=5)
        button08 = tk.Button(select_window, text="政治", command=lambda: class_select_cb(7))
        button08.grid(row=2, column=2, pady=5)
        button09 = tk.Button(select_window, text="地理", command=lambda: class_select_cb(8))
        button09.grid(row=2, column=3, pady=5)
        button10 = tk.Button(select_window, text="其他", command=lambda: class_select_cb(9))
        button10.grid(row=2, column=4, pady=5)
        # print(DATA)
        select_window.mainloop()

    return None


if __name__ == "__main__":
    if "-version" in sys.argv:
        sys.exit(VERSION)
    main()
