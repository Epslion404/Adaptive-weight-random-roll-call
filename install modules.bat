@echo off

.\.venv\Scripts\python.exe -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
.\.venv\Scripts\python.exe -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

.\.venv\Scripts\python.exe -m pip install tkinter
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\python.exe -m pip install msvc-runtime
.\.venv\Scripts\python.exe -m pip install matplotlib
.\.venv\Scripts\python.exe -m pip install ttkbootstrap
.\.venv\Scripts\python.exe -m pip install pycryptodome
.\.venv\Scripts\python.exe -m pip install Nuitka
.\.venv\Scripts\python.exe -m pip install ordered-set
.\.venv\Scripts\python.exe -m pip install zstandard

.\.venv\Scripts\python.exe --version
echo Done!
pause