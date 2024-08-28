# -*- coding:utf-8 -*- #

import tkinter as tk
import random
import copy

# =================定义变量================= #

# name_list: list = str('将这个字符串替换为所有的名字，名字之间使用分隔符分隔').split('将这个字符串替换为名字之间的分隔符')
name_list: list = str('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z').split(' ')

init_time = ''

name: list = copy.deepcopy(name_list)

non_repeat_name: list = copy.deepcopy(name_list)

frequency: list = [0 for i in range(len(name_list))]

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

Feedback_intensity = 2  # 负反馈力度
