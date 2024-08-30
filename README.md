# 自适应权重随机点名

[gitee](https://gitee.com/Nept-Epslion/Adaptive-weight-random-roll-call/)

#### 介绍
短期内更加公平的随机点名系统  
**使用了Minecraft的幸运方块MOD作为图标，如果不能使用，请立即告诉我**

#### 软件架构
使用python 3.8开发。

#### 安装教程

1.  安装python 3.8
3.  运行文件 `install modules.bat` 来安装库
4.  按照main.py文件内的指示填写名单和分隔符
5.  运行main.py文件，检验程序是否可以运行
6.  运行命令 `pyinstaller -F -w -i favicon.ico main.py` 或运行文件 `pack to exe.bat` 以打包成可执行文件

#### 使用说明

直接运行main.py文件或打包后的文件

#### TO DO

- [x] 初始化仓库
- [ ] 让老代码能看懂(80%)
- [ ] 修改BUG（结束主进程后子进程报错不能退出）
- [ ] 加密配置文件
- [ ] 使用未被点名次数调节
- [x] 分科记录数据
- [x] 使用JSON格式记录数据
