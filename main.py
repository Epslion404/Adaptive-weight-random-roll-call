# -*- coding:utf-8 -*- #
import matplotlib.transforms as mtransforms  # noqa: F401
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

name_list = []
init_time = ''
repeatable_name = []
unrepeatable_names = []
frequency: list = []
uncalled_times: list = []
weight: list = []
skip_calculate = False
root = tk.Tk()
customize_window = None
chart_exist = False
shown_name = tk.StringVar()
pause_or_continue = True
selected = None
enable_weight = tk.IntVar(value=1)
none_repeat = tk.IntVar()
non_repeat_check_box = None
none_repeat_text = tk.StringVar(value='不重复(0/0)')
record_name_repeatable = []
record_name_unrepeatable = []
set_name_repeatable = []
set_name_unrepeatable = []
is_customize_window_init = False
unrepeatable_weight = []
Feedback_intensity = 2
DATA = {}
Subject = ''
float_window = None
previous_state = 'normal'
icon_photo = None
try:
    icon_image = Image.open("favicon.ico").resize((32, 32))
    icon_photo = ImageTk.PhotoImage(icon_image)
except Exception:
    icon_photo = None
r_f = 0.5
r_u = 0.5
key = b'\x16a\xca\xa7\xa4\n\xef\xc72{\x85\x88HJ\x1e3'
VERSION = "1.1.0"


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
        tkinter.messagebox.showerror("错误", "配置文件解析失败，请重新生成")
        exit_exe()


def inv_poc() -> None:
    global pause_or_continue
    pause_or_continue = not pause_or_continue


def reset_none_repeat() -> None:
    global unrepeatable_names, unrepeatable_weight, record_name_unrepeatable
    if not pause_or_continue:
        tkinter.messagebox.showerror("错误", "不能在暂停滚动时重置名单")
        return
    unrepeatable_names = copy.deepcopy(repeatable_name)
    unrepeatable_weight = copy.deepcopy(weight)
    for v in record_name_unrepeatable:
        v.set(1)


def compute_weights(freq: list, uncalled: list, feedback: int, ratio_f: float, ratio_u: float) -> list:
    if not freq:
        return []
    fi1 = [f + 1 for f in freq]
    avg_f = sum(fi1) / len(fi1)
    hat_f, sum_f = [], 0.0
    for v in fi1:
        if v > avg_f:
            val = 1.0 / (feedback * v)
        elif v < avg_f:
            val = feedback / v
        else:
            val = 1.0 / v
        hat_f.append(val)
        sum_f += val

    ui1 = [u + 1 for u in uncalled]
    avg_u = sum(ui1) / len(ui1)
    hat_u, sum_u = [], 0.0
    for v in ui1:
        if v > avg_u:
            val = feedback * v
        elif v < avg_u:
            val = v / feedback
        else:
            val = v
        hat_u.append(val)
        sum_u += val

    if sum_f == 0:
        sum_f = 1.0
    if sum_u == 0:
        sum_u = 1.0

    return [ratio_f * (f / sum_f) + ratio_u * (u / sum_u) for f, u in zip(hat_f, hat_u)]


def calculate_weight() -> None:
    global weight, unrepeatable_weight, repeatable_name, unrepeatable_names
    weight[:] = compute_weights(frequency, uncalled_times, Feedback_intensity, r_f, r_u)
    unrepeatable_weight = []
    for name in unrepeatable_names:
        if name in repeatable_name:
            unrepeatable_weight.append(weight[repeatable_name.index(name)])


def flash_name() -> None:
    global selected, none_repeat, unrepeatable_names, none_repeat_text
    global frequency, skip_calculate, weight, unrepeatable_weight, enable_weight, uncalled_times

    calculate_weight()

    while True:
        if pause_or_continue:
            if not repeatable_name:
                time.sleep(0.05)
                continue
            if none_repeat.get() == 0:
                selected = random.choices(repeatable_name, weights=weight or None, k=1)[0] if enable_weight.get() == 1 else random.choice(repeatable_name)
            else:
                if not unrepeatable_names:
                    unrepeatable_names = copy.deepcopy(repeatable_name)
                    calculate_weight()
                selected = random.choices(unrepeatable_names, weights=unrepeatable_weight or None, k=1)[0] if enable_weight.get() == 1 else random.choice(unrepeatable_names)
            shown_name.set(selected)
            if skip_calculate:
                skip_calculate = False
        else:
            if none_repeat.get() == 1:
                if selected in unrepeatable_names:
                    if record_name_unrepeatable:
                        record_name_unrepeatable[name_list.index(selected)].set(0)
                    unrepeatable_names.remove(selected)
                    skip_calculate = False
                if not unrepeatable_names:
                    unrepeatable_names = copy.deepcopy(repeatable_name)
            if not skip_calculate:
                frequency[repeatable_name.index(selected)] += 1
                for i in range(len(uncalled_times)):
                    uncalled_times[i] += 1
                uncalled_times[repeatable_name.index(selected)] = 0
                calculate_weight()
                skip_calculate = True

        none_repeat_text.set('不重复({}/{})'.format(len(unrepeatable_names), len(repeatable_name)))
        time.sleep(0.01)


def customize_windows() -> None:
    global is_customize_window_init, customize_window
    if not is_customize_window_init:
        is_customize_window_init = True
        customize_window_init()
    else:
        if isinstance(customize_window, tk.Toplevel):
            customize_window.deiconify()


def setting_window_on_closing() -> None:
    global customize_window
    if isinstance(customize_window, tk.Toplevel):
        customize_window.withdraw()


def show_data() -> None:
    global chart_exist, init_time, frequency, uncalled_times, name_list, r_f, r_u, Feedback_intensity
    if not name_list:
        tkinter.messagebox.showinfo("提示", "暂无数据可展示")
        chart_exist = False
        return

    disp_weight = compute_weights(frequency, uncalled_times, Feedback_intensity, r_f, r_u)

    y1 = np.array(frequency)
    y2 = np.array(uncalled_times)
    y3 = np.array(disp_weight)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(17, 7), dpi=100, num=f'记录始于： {init_time}  总计点名：{sum(frequency)}次')
    ax1.bar(np.arange(len(name_list)) - 0.2, y1, width=0.4, color="green", label="频率")
    ax1.set_ylabel("频率")
    ax1.set_ylim(bottom=0)
    ax1.set_xticks(np.arange(len(name_list)))
    ax1.set_xticklabels(name_list, fontsize=10, rotation=45)

    ax1_2 = ax1.twinx()
    ax1_2.bar(np.arange(len(name_list)) + 0.2, y2, width=0.4, color="blue", label='距离上次未被抽到的次数')
    ax1_2.set_ylabel('距离上次未被抽到的次数')
    ax1_2.set_ylim(bottom=0)
    ax1_2.axhline(y=(sum(y1) / len(y1) if len(y1) else 0), color='r', label="频率总体平均")

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
    global chart_exist
    if not chart_exist:
        data = threading.Thread(target=show_data, daemon=True)
        data.start()
        chart_exist = True


def create_floating_icon() -> None:
    global float_window, root, icon_photo
    if icon_photo is None:
        return
    float_window = tk.Toplevel()
    float_window.overrideredirect(True)
    float_window.geometry(f"32x32+{root.winfo_x() + 117}+{root.winfo_y() + 1}")
    float_window.attributes("-topmost", True)
    float_window.focus_set()

    icon_label = tk.Label(float_window, image=icon_photo, cursor="fleur")
    icon_label.pack(side=tk.LEFT)

    def start_move(event):
        float_window.x = event.x
        float_window.y = event.y

    def on_move(event):
        x = float_window.winfo_x() + event.x - float_window.x
        y = float_window.winfo_y() + event.y - float_window.y
        float_window.geometry(f"+{x}+{y}")

    icon_label.bind("<Button-1>", start_move)
    icon_label.bind("<B1-Motion>", on_move)

    def on_double_click(event):
        root.deiconify()
        root.geometry(f"+{float_window.winfo_x() - 117}+{float_window.winfo_y() - 1}")
        float_window.destroy()

    icon_label.bind("<Double-1>", on_double_click)


def check_window_state() -> None:
    global previous_state
    current_state = root.wm_state()
    if current_state == 'iconic' and previous_state != 'iconic':
        root.withdraw()
        create_floating_icon()
    previous_state = current_state
    root.after(100, check_window_state)


def customize_window_init() -> None:
    global customize_window, record_name_repeatable, repeatable_name, set_name_repeatable
    global enable_weight, record_name_unrepeatable, set_name_unrepeatable, chart_exist, VERSION, r_f, r_u

    record_name_repeatable = []
    record_name_unrepeatable = []
    set_name_repeatable = []
    set_name_unrepeatable = []

    customize_window = tk.Toplevel(root, width=820, height=640)
    customize_window.resizable(height=False, width=False)
    customize_window.title(f"随机点名 - 版本{VERSION}")
    customize_window.attributes('-topmost', True)
    customize_window.protocol("WM_DELETE_WINDOW", setting_window_on_closing)
    try:
        customize_window.iconbitmap('favicon.ico')
    except Exception:
        pass

    length = len(name_list)

    repeatable_name_group = tk.LabelFrame(customize_window, text='可重复组')
    repeatable_name_group.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    for i in range(length):
        t = tk.IntVar(value=1 if name_list[i] in repeatable_name else 0)
        record_name_repeatable.append(t)
        but = tk.Checkbutton(repeatable_name_group, text=name_list[i], variable=record_name_repeatable[i],
                             command=repeatable_name_group_update)
        but.grid(row=i // 3, column=i % 3)
        set_name_repeatable.append(but)

    unrepeatable_group_lf = tk.LabelFrame(customize_window, text='不重复组')
    unrepeatable_group_lf.grid(row=0, column=4, columnspan=3, padx=5, pady=5)
    for i in range(length):
        t = tk.IntVar(value=1 if name_list[i] in unrepeatable_names else 0)
        record_name_unrepeatable.append(t)
        but = tk.Checkbutton(unrepeatable_group_lf, text=name_list[i], variable=record_name_unrepeatable[i],
                             command=unrepeatable_name_group_update)
        but.grid(row=i // 3, column=i % 3)
        set_name_unrepeatable.append(but)

    ratio_frame = tk.LabelFrame(customize_window, text='权重参数')
    ratio_frame.grid(row=length // 3 + 1, column=0, columnspan=3, pady=10, padx=5, sticky='w')
    tk.Label(ratio_frame, text=f"当前配置: r_f={r_f:.2f}, r_u={r_u:.2f} (仅可在配置生成器修改)")\
        .grid(row=0, column=0, padx=5, pady=5, sticky='w')

    show_chat_button = tk.Button(customize_window, text="展示统计数据", command=show_data_in_customize)
    show_chat_button.grid(row=length // 3 + 1, column=4, pady=5, padx=5)

    adaptive_weight_mode = tk.Checkbutton(customize_window, text='自适应权重随机模式', variable=enable_weight)
    adaptive_weight_mode.grid(row=length // 3 + 1, column=5, pady=5, padx=5)

    about_label = tk.Button(customize_window, text="对本软件使用、转载、修改等请遵守开源协议")
    about_label.grid(row=length // 3 + 3, column=0, columnspan=4, pady=8)
    tk.Button(customize_window, text="gitee", fg="blue", cursor="hand2",
              command=lambda: webbrowser.open_new(
                  "https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/blob/master/LICENSE")
              ).grid(row=length // 3 + 3, column=4, pady=8)
    tk.Button(customize_window, text="github", fg="blue", cursor="hand2",
              command=lambda: webbrowser.open_new(
                  "https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/blob/master/LICENSE")
              ).grid(row=length // 3 + 3, column=5, pady=8)

    tk.Button(customize_window, text="确认", command=setting_window_on_closing)\
        .grid(row=length // 3 + 4, column=6, pady=10)

    customize_window.mainloop()


def unrepeatable_name_group_update():
    global record_name_unrepeatable, name_list, unrepeatable_names, unrepeatable_weight, weight
    for i in range(len(record_name_unrepeatable)):
        if record_name_unrepeatable[i].get() == 1:
            if name_list[i] not in unrepeatable_names:
                unrepeatable_names.append(name_list[i])
        else:
            if name_list[i] in unrepeatable_names:
                unrepeatable_names.remove(name_list[i])
    unrepeatable_weight = [weight[name_list.index(n)] for n in unrepeatable_names if n in name_list]


def repeatable_name_group_update():
    global record_name_repeatable, name_list, repeatable_name
    for i in range(len(record_name_repeatable)):
        if record_name_repeatable[i].get() == 1:
            if name_list[i] not in repeatable_name:
                repeatable_name.append(name_list[i])
        else:
            if name_list[i] in repeatable_name:
                repeatable_name.remove(name_list[i])


def on_root_closing() -> None:
    global DATA
    try:
        DATA[Subject]['non_repeat_name'] = unrepeatable_names
        DATA[Subject]['frequency'] = frequency
        DATA[Subject]['uncalled_times'] = uncalled_times
        DATA["ratio_frequency"] = r_f
        DATA["ratio_uncalled"] = r_u
        with open('record.dat', 'w', encoding='utf-8') as f:
            f.write(encrypt(json.dumps(DATA, ensure_ascii=False)))
    finally:
        root.destroy()
        exit_exe()


def exit_exe() -> None:
    if os.path.exists("running.dat"):
        try:
            os.remove("running.dat")
        except Exception:
            pass
    sys.exit()


def main() -> None:
    global shown_name, repeatable_name, none_repeat, none_repeat_text
    global frequency, init_time, DATA, Subject, name_list, weight, uncalled_times
    global Feedback_intensity, r_f, r_u

    if os.path.exists('running.dat'):
        root.destroy()
        tkinter.messagebox.showinfo("提示", "随机点名已经在运行了")
        exit_exe()
    else:
        with open("running.dat", 'w') as f:
            f.write('?')
        try:
            ctypes.windll.kernel32.SetFileAttributesW('running.dat', 0x02)
        except Exception:
            pass

    def class_select_cb(index: int):
        global Subject, DATA, unrepeatable_names, frequency, uncalled_times
        try:
            subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理', '其他']
            Subject = subjects[index]
            unrepeatable_names = DATA[Subject]['non_repeat_name'][:]
            frequency[:] = DATA[Subject]['frequency'][:]
            uncalled_times[:] = DATA[Subject]['uncalled_times'][:]
            if ss == 1:
                select_window.destroy()
        except Exception as e:
            tkinter.messagebox.showerror("错误", f'Error raised: {e}')
            exit_exe()

        root.geometry("240x120+0+0")
        root.resizable(height=False, width=False)
        root.attributes('-topmost', True)
        root.protocol("WM_DELETE_WINDOW", on_root_closing)
        root.overrideredirect(False)

        flash_name_thread = threading.Thread(target=flash_name, daemon=True)
        flash_name_thread.start()
        check_window_state()
        root.mainloop()

    style = tbs.style.Style(theme='minty')
    _ = style.master

    root.title('随机点名')
    root.geometry("0x0")
    root.overrideredirect(True)
    try:
        root.iconbitmap('favicon.ico')
    except Exception:
        pass

    init_window = tk.Toplevel(root)
    init_window.title('随机点名')
    init_window.geometry("240x120+50+50")
    init_window.resizable(height=False, width=False)
    init_window.overrideredirect(True)
    tk.Label(init_window, text='加载中...', font=("黑体", 20, "bold"), relief=tk.RIDGE)\
        .pack(expand=True)

    if not os.path.exists('record.dat'):
        tkinter.messagebox.showerror("错误", "没有找到配置文件")
        exit_exe()

    with open('record.dat', 'r', encoding='utf-8') as f:
        try:
            DATA = json.loads(decrypt(f.read()))
            name_list = DATA["name_list"]
            init_time = DATA['init_time']
            ss = DATA["Separate_subjects"]
            Feedback_intensity = DATA["Feedback_intensity"]
            r_f = DATA.get("ratio_frequency", 0.5)
            r_u = DATA.get("ratio_uncalled", 0.5)
            total_ratio = r_f + r_u
            if total_ratio <= 0:
                r_f, r_u = 0.5, 0.5
            else:
                r_f /= total_ratio
                r_u /= total_ratio
            repeatable_name[:] = name_list
            unrepeatable_names[:] = name_list
            shown_name.set(random.choice(repeatable_name) if repeatable_name else '')
            none_repeat_text.set(f'不重复({len(unrepeatable_names)}/{len(name_list)})')
            weight[:] = [1.0 for _ in range(len(name_list))]
            frequency[:] = [0 for _ in range(len(name_list))]
            uncalled_times[:] = [0 for _ in range(len(name_list))]
        except Exception as ex:
            tkinter.messagebox.showerror("错误", f'Error raised: {ex}')
            exit_exe()

    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['axes.unicode_minus'] = False
    random.seed(time.time())

    tk.Label(root, textvariable=shown_name, font=("黑体", 40, "bold"), relief=tk.RIDGE).pack(expand=True)

    tk.Button(root, text="暂停/继续", command=inv_poc).pack(expand=True)

    none_repeat.set(1)
    tk.Checkbutton(root, textvariable=none_repeat_text, variable=none_repeat).pack(expand=True, side=tk.LEFT)
    tk.Button(root, text="自定义", command=customize_windows).pack(side=tk.LEFT)
    tk.Button(root, text="重置", command=reset_none_repeat).pack(side=tk.LEFT)

    init_window.destroy()

    if ss == 0:
        class_select_cb(0)
    else:
        select_window = tk.Toplevel(root)
        select_window.geometry("180x120+50+50")
        select_window.resizable(height=False, width=False)
        select_window.attributes('-topmost', True)
        tk.Label(select_window, text='选择当堂科目', font=("黑体", 20, "bold"), relief=tk.RIDGE)\
            .grid(row=0, columnspan=5, pady=5)
        buttons = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理', '其他']
        for idx, title in enumerate(buttons):
            tk.Button(select_window, text=title, command=lambda i=idx: class_select_cb(i))\
                .grid(row=1 + idx // 5, column=idx % 5, pady=5)
        select_window.mainloop()


if __name__ == "__main__":
    if "-version" in sys.argv:
        sys.exit(VERSION)
    main()