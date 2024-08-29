# -*- coding:utf-8 -*- #
# 开始于 2024 年 3 月 17 日，15:10:45
# 该文件仅达到了能够使用的水平
# 可能存在各种BUG

import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
import ttkbootstrap as tbs
import tkinter.messagebox
from pylab import mpl
import tkinter as tk
import numpy as np
import webbrowser
import threading
import inspect
import random
import copy
import time
import json
import sys
import os

# 所有名字
# name_list: list = str('将这个字符串替换为所有的名字，名字之间使用分隔符分隔').split('将这个字符串替换为名字之间的分隔符')
name_list: list = str('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z').split(' ')

# 数据记录的起始时间
init_time = ''

# 可重复组名单
repeatable_name: list = copy.deepcopy(name_list)

# 不重复组名单
unrepeatable_names: list = copy.deepcopy(name_list)

# 总频率
frequency: list = [0 for i in range(len(name_list))]

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
shown_name = tk.StringVar(value=random.choice(repeatable_name))

# 标志：是否开始滚动
pauseOrContinue = True

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


def inv_poc() -> None:
    """
    反转pauseOrContinue
    """
    global pauseOrContinue
    pauseOrContinue = not pauseOrContinue
    return None


def reset_none_repeat() -> None:
    """
    重置不重复组名单
    """
    global unrepeatable_names, unrepeatable_weight, record_name_unrepeatable, pauseOrContinue
    if not pauseOrContinue:
        tkinter.messagebox.showerror("Error", "不能在暂停滚动时重置名单")
    else:
        unrepeatable_names = copy.deepcopy(repeatable_name)
        unrepeatable_weight = copy.deepcopy(weight)
        for i in record_name_unrepeatable:
            i.set(1)
    return None


def flash_name() -> None:
    global pauseOrContinue, repeatable_name, selected, none_repeat, unrepeatable_names, none_repeat_text, frequency, skip_calculate, weight, unrepeatable_weight, enable_weight, Feedback_intensity

    # 同步权重
    for i in unrepeatable_names:
        unrepeatable_weight.append(weight[repeatable_name.index(i)])

    while True:
        if pauseOrContinue:
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
                    if record_name_unrepeatable != []:
                        # print(NameSelect1)
                        record_name_unrepeatable[name_list.index(selected)].set(0)
                    unrepeatable_names.remove(selected)
                    skip_calculate = False
                if not unrepeatable_names:
                    random.seed(time.time())
                    unrepeatable_names = copy.deepcopy(repeatable_name)
            if not skip_calculate:
                frequency[repeatable_name.index(selected)] += 1
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
                unrepeatable_weight = []
                for i in unrepeatable_names:
                    unrepeatable_weight.append(weight[repeatable_name.index(i)])
                # print(weight_name1)
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


def calculate_data() -> list:
    global frequency, weight, Feedback_intensity
    average = (sum(frequency))
    return []


def show_data() -> None:
    """
    展示统计数据
    """
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


def customize_window_init() -> None:
    """
    初始化自定义窗口
    """
    global customize_window, record_name_repeatable, repeatable_name, set_name_repeatable, enable_weight, record_name_unrepeatable, set_name_unrepeatable, chart_exist

    # 初始化自定义窗口
    customize_window = tk.Toplevel(root, width=800, height=600)
    customize_window.resizable(height=False, width=False)
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

    gitee_link_label = tk.Button(customize_window, text="gitee", fg="blue", cursor="hand2", command=lambda: webbrowser.open_new("https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/blob/master/LICENSE"))
    gitee_link_label.grid(row=length // 3 + 3, column=4)

    github_link_label = tk.Button(customize_window, text="github", fg="blue", cursor="hand2",command=lambda: webbrowser.open_new("https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/blob/master/LICENSE"))
    github_link_label.grid(row=length // 3 + 3, column=5)

    # 展示统计数据按钮
    show_chat_button = tk.Button(customize_window, text="展示统计数据", command=show_data_in_customize)
    show_chat_button.grid(row=length // 3 + 1, column=0)

    # 恢复默认设置按钮
    reset_button = tk.Button(customize_window, text="恢复默认设置", command=config_file_error)
    reset_button.grid(row=length // 3 + 1, column=2)

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


def config_file_error() -> None:
    """
    删除配置文件
    """
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame[1]
    caller_line = caller_frame[2]
    caller_function = caller_frame[3]
    print("Caller file:", caller_file)
    print("Caller line:", caller_line)
    print("Caller function:", caller_function)
    os.remove('record.dat')
    sys.exit()


def on_root_closing() -> None:
    global root, customize_window, frequency, init_time, DATA
    root.destroy()
    DATA[Subject]['non_repeat_name'] = unrepeatable_names
    DATA[Subject]['frequency'] = frequency
    # print(Subject, frequency)
    # print(DATA[Subject]['frequency'])
    with open('record.dat', 'w', encoding='utf-8') as f:
        json.dump(DATA, f)
        f.close()
    sys.exit()


def main() -> None:
    """
    初始化随机点名
    """
    global root, shown_name, repeatable_name, selected, none_repeat, none_repeat_text, customize_window, record_name_repeatable, unrepeatable_names, non_repeat_check_box, frequency, init_time, pauseOrContinue, DATA, Subject

    def class_select_cb(index: int):
        global Subject, DATA, unrepeatable_names, frequency
        try:
            subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理', '其他']
            Subject = subjects[index]
            unrepeatable_names = DATA[Subject]['non_repeat_name']
            frequency = DATA[Subject]['frequency']
            select_window.destroy()
        except Exception as ex:
            print(f'Error raised: {ex}')
            config_file_error()
        # 设置根窗口
        root.geometry("240x120+0+0")
        root.resizable(height=False, width=False)
        root.attributes('-topmost', True)
        # root.attributes('-toolwindow', True)
        root.protocol("WM_DELETE_WINDOW", on_root_closing)
        root.overrideredirect(False)

        flash_name_thread = threading.Thread(target=flash_name)
        flash_name_thread.daemon = True  # 守护模式
        flash_name_thread.start()

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
        DATA = {"语文": {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))]},
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
        with open('record.dat', 'w', encoding='utf-8') as f:
            json.dump(DATA, f)
            f.close()

    # 读取配置文件
    with open('record.dat', 'r', encoding='utf-8') as f:
        try:
            DATA = json.load(f)
            subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理', '其他']
            # for i in subjects:
            #     if len(DATA[i]) != 2:
            #         raise RuntimeError("Config file error")
            init_time = DATA['init_time']
        except Exception as ex:
            print(f'Error raised: {ex}')
            f.close()
            config_file_error()

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
    select_window = tk.Tk()
    select_window.geometry("180x120+50+50")
    select_window.resizable(height=False, width=False)
    select_window.overrideredirect(True)
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
    main()
