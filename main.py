# -*- coding:utf-8 -*- #
# 开始于 2024 年 3 月 17 日，15:10:45
# 该文件仅达到了能够使用的水平
# 可能存在各种BUG
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
import ttkbootstrap as tbs
from pylab import mpl
import tkinter as tk
import numpy as np
import threading
import ctypes
import random
import copy
import time
import json
import sys
import os

# name_list: list = str('将这个字符串替换为所有的名字，名字之间使用分隔符分隔').split('将这个字符串替换为名字之间的分隔符')
# 所有名字
name_list: list = str('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z').split(' ')

# 数据记录的起始时间
init_time = ''

name: list = copy.deepcopy(name_list)

non_repeat_name: list = copy.deepcopy(name_list)

frequency: list = [0 for i in range(len(name_list))]

weight: list = [1.0 for j in range(len(name_list))]

activated_f = False

root = tk.Tk()

root1 = None

chart_exist = False

shown_name = tk.StringVar(value=random.choice(name))

pauseOrContinue = True

selected = None

enable_weight = tk.IntVar(value=1)

# 标志：是否启用重复
none_repeat = tk.IntVar()

non_repeat_check_box = None

none_repeat_text = tk.StringVar(value='{} / {}'.format(len(name), len(non_repeat_name)))

handle = {"control": 1}

NameSelect = []

NameSelect1 = []

SelectGroup = []

SelectGroup1 = []

is_setting_window_init = False

weight_name1 = []

Feedback_intensity = 2  # 负反馈力度


def cb1():
    global pauseOrContinue
    if pauseOrContinue == 0:
        pauseOrContinue = 1
    else:
        pauseOrContinue = 0
    return


def cb2():
    # print('cb2')
    global non_repeat_name, weight_name1, NameSelect1, pauseOrContinue
    if not pauseOrContinue:
        pass
    else:
        non_repeat_name = copy.deepcopy(name)
        weight_name1 = copy.deepcopy(weight)
        for i in NameSelect1:
            i.set(1)


def flash_name() -> None:
    global pauseOrContinue, name, selected, none_repeat, non_repeat_name, none_repeat_text, frequency, activated_f, weight, weight_name1, enable_weight, Feedback_intensity, Exit
    for i in non_repeat_name:
        weight_name1.append(weight[name.index(i)])

    while True:
        if pauseOrContinue:
            if none_repeat.get() == 0:
                if enable_weight.get() == 1:
                    selected = random.choices(name, weights=weight, k=1)[0]
                else:
                    selected = random.choice(name)
                shown_name.set(selected)
            else:
                if enable_weight.get() == 1:
                    selected = random.choices(non_repeat_name, weights=weight_name1, k=1)[0]
                else:
                    selected = random.choice(non_repeat_name)
                shown_name.set(selected)
            if activated_f:
                activated_f = False
        else:
            if none_repeat.get() == 1:
                if selected in non_repeat_name:
                    if NameSelect1 != []:
                        # print(NameSelect1)
                        NameSelect1[name_list.index(selected)].set(0)
                    non_repeat_name.remove(selected)
                    activated_f = False
                if not non_repeat_name:
                    random.seed(time.time())
                    non_repeat_name = copy.deepcopy(name)
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
                for i in non_repeat_name:
                    weight_name1.append(weight[name.index(i)])
                # print(weight_name1)
                activated_f = True

        none_repeat_text.set('不重复({}/{})'.format(len(non_repeat_name), len(name)))
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
    root1.iconbitmap('favicon.ico')

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
        if name_list[i] in non_repeat_name:
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

    reset_b = tk.Button(root1, text="恢复默认设置", command=config_file_error)
    reset_b.grid(row=length // 3 + 1, column=1)

    mode = tk.Checkbutton(root1, text='自适应权重随机模式', variable=enable_weight)
    mode.grid(row=length // 3 + 1, column=4)

    root1.mainloop()


def cb5():
    global NameSelect1, name_list, non_repeat_name, weight_name1, weight
    for i in range(len(NameSelect)):
        if NameSelect1[i].get() == 1:
            if not (name_list[i] in non_repeat_name):
                non_repeat_name.append(name_list[i])
        if NameSelect1[i].get() == 0:
            if name_list[i] in non_repeat_name:
                non_repeat_name.remove(name_list[i])
    weight_name1 = []
    for i in non_repeat_name:
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


def config_file_error():
    os.remove('record.dat')
    sys.exit()


def on_root_closing():
    global root, root1, frequency, init_time
    root.destroy()
    with open('record.dat', 'w', encoding='utf-8') as f:
        for i in non_repeat_name:
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
    global root, shown_name, name, selected, none_repeat, none_repeat_text, root1, NameSelect, non_repeat_name, non_repeat_check_box, frequency, init_time

    # 定义样式
    style = tbs.style.Style(theme='minty')
    top6 = style.master

    # 根窗口
    root.title('随机点名')
    root.geometry("0x0")
    root.iconbitmap('favicon.ico')
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
    # if not os.path.exists('record.dat'):
    #     with open('record.dat', 'w', encoding='utf-8') as f:
    #         for i in name_list:
    #             f.write(i + ';')
    #         f.write('\n')
    #         for i in frequency:
    #             f.write(str(i) + ';')
    #         f.write('\n' + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
    if not os.path.exists('record.dat'):
        data = {"non_repeat_name": name_list, "frequency": [0 for i in range(len(name_list))],
                "init_time": time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())}
        json_string = json.dumps(data)
        with open('record.dat', 'w', encoding='utf-8') as f:
            f.write(json_string)

    # 读取配置文件
    with open('record.dat', 'r', encoding='utf-8') as f:
        try:
            read = f.read()
            non_repeat_name = str(read.split('\n')[0]).split(';')[:-1]
            # print(len(name1))
            temp: list = str(read.split('\n')[1]).split(';')[:-1]
            for i in range(len(frequency)):
                frequency[i] = int(temp[i])
            init_time = read.split('\n')[2]
        except:
            f.close()
            config_file_error()

    # 指定默认字体
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['axes.unicode_minus'] = False

    # 设置随机数种子
    random.seed(time.time())

    # 设置根窗口
    root.geometry("240x120+0+0")
    root.resizable(height=False, width=False)
    root.attributes('-topmost', True)
    # root.attributes('-toolwindow', True)
    root.protocol("WM_DELETE_WINDOW", on_root_closing)
    init_window.destroy()  # 销毁加载窗口
    root.overrideredirect(False)

    # 显示名字的标签
    name_label = tk.Label(root, textvariable=shown_name, font=("黑体", 40, "bold"), relief=tk.RIDGE)
    name_label.place(relx=0.1, rely=0.5)
    name_label.pack(expand=True)

    # 暂停/继续滚动按钮
    button = tk.Button(root, text="暂停/继续", command=cb1)
    button.pack(expand=True)

    # 置0
    none_repeat = tk.IntVar()
    # 复选框文本
    none_repeat_text = tk.StringVar(value=f'不重复({len(non_repeat_name)}/{len(name)})')

    # 自定义按钮
    customize_button = tk.Button(root, text="自定义", command=setting_window)
    customize_button.pack(side=tk.LEFT)

    non_repeat_check_box = tk.Checkbutton(root, textvariable=none_repeat_text, variable=none_repeat)
    none_repeat.set(1)
    non_repeat_check_box.pack(expand=True, side=tk.LEFT)

    reset_button = tk.Button(root, text="重置", command=cb2)
    reset_button.pack(side=tk.LEFT)

    flash_name_thread = threading.Thread(target=flash_name)
    flash_name_thread.setDaemon(True)
    flash_name_thread.start()
    # print(NameSelect[0].get())
    root.mainloop()
    return None


if __name__ == "__main__":
    main()
