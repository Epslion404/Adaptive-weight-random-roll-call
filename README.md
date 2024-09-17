# 自适应权重随机点名

[github](https://github.com/Epslion404/Adaptive-weight-random-roll-call)

#### 介绍

短期内更加公平的随机点名系统  
**使用了Minecraft的幸运方块MOD作为图标，如果不能使用，请立即告诉我**

#### 软件架构

使用python 3.8开发。

#### 安装教程

1. 安装python 3.8
2. 运行文件 `install modules.bat` 来安装库
3. 按照main.py文件内的指示填写名单和分隔符
4. 运行main.py文件，检验程序是否可以运行
5. 运行命令 `pyinstaller -F -w -i favicon.ico main.py` 或运行文件 `pack to exe.bat` 以打包成可执行文件

#### 使用说明

直接运行 `main.py` 文件或打包后的文件

#### TO DO

- [x] 初始化仓库
- [x] 让老代码能看懂(80%)
- [ ] 修改BUG（结束主进程后子进程报错不能退出）
- [x] 加密配置文件
- [x] 使用未被点名次数调节
- [x] 分科记录数据
- [x] 使用JSON格式记录数据
- [x] 不重复启动
- [x] 最小化为图标
- [ ] 自定义频率调节与未被点名次数调节的比例

#### 原理

由于随机函数短期内的随机结果并不均匀，容易引起同学与老师们引入某些不切实际的猜想与偏见——认为随机点名并不“随机”。因此我们需要在保留随机功能的前提下对系统添加负反馈调节，即使用加权随机函数。  
  
最先想到的方法是利用频率倒数调节法(Reciprocal frequency adjustment method, RFA)。即利用所有人被抽取的频率的倒数作为权重来调节，唯一需要注意的是需要处理的是频率为0的情况。在这里我选择在计算时将所有人的频率+1。即：
$$
w=\frac{1}{f_n+1}
$$
事实上，控制反馈调节的强度也同样重要，引入负反馈强度$\Psi$，于是权重可以表示为：
$$
w_n=\frac{\hat f_n}{\Sigma f}
$$
其中$\hat f_n$为加入反馈的频率，若使用$\bar{f}$表示总体平均频率，则$\hat f_n$可以表示为：
$$
\hat f_n=\begin{cases}
\ \frac{\Psi}{f_n+1}, & f_n < \bar{f} \\
\ \frac{1}{\Psi(f_n+1)}, & f_n > \bar{f} \\
\ \frac{1}{f_n+1}, & f_n = \bar{f}
\end{cases}
$$  
$\Sigma f$为：
$$
\Sigma f = \sum_{i=0}^{m} \begin{cases}
\ \frac{\Psi}{f_i+1}, & f_i < \bar{f} \\
\ \frac{1}{\Psi(f_i+1)}, & f_i > \bar{f} \\
\ \frac{1}{f_i+1}, & f_i = \bar{f}
\end{cases}
$$。

但随着软件的使用，经常发现很长一段时间内抽不到某位同学，之后又在一段较短的时间内被频繁抽取，个人频率迅速追平平均频率。因此，我们不仅要考虑宏观调节，也需要考虑微观调节，为此，我选择记录每位同学距离上一次被抽到的次数$\mu$来调节(NLT)。在这种情况下，权重可以表示为：
$$
w_n=r_f\cdot\frac{\hat f_n}{\Sigma f}+r_\mu\cdot\frac{\hat\mu_n}{\Sigma\mu}
$$
其中$r_f$、$r_\mu$分别为RFA调节与NLT调节的占比，$\hat\mu_n$为加入反馈的距离上一次被抽到的次数。若使用$\bar{\mu}$表示距离上一次被抽到的次数的总体平均，则$\hat\mu_n$可以表示为：
$$
\hat\mu_n=\begin{cases}
\ \frac{\Psi \mu_n}{\Sigma\mu}, & \mu_n < \bar\mu \\
\ \frac{\mu_n}{\Psi\Sigma\mu}, & \mu_n > \bar\mu \\
\ \frac{\mu}{\Sigma\mu}, & \mu_n = \bar\mu
\end{cases}
$$
$\Sigma\mu$为：
$$
\Sigma\mu = \sum_{i=0}^{m} \begin{cases}
\ \Psi\mu_i, & \mu_i < \bar{\mu} \\
\ \frac{\mu_i}{\Psi}, & \mu_i > \bar{\mu} \\
\ \mu_i, & \mu_i = \bar{\mu}
\end{cases}
$$

#### 参与贡献

除了我自己暂时还没人 φ(゜▽゜*)♪
