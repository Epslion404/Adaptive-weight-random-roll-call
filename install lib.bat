@echo off

python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

python -m pip install tkinter
python -m pip install pyinstaller
python -m pip install msvc-runtime
python -m pip install matplotlib
python -m pip install ttkbootstrap
python -m pip install pycryptodome

python --version
echo success!
pause