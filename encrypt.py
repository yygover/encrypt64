import base64
import ctypes
import os
import subprocess
from tkinter import messagebox, StringVar, BooleanVar, filedialog

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


# フォルダ指定の関数
def dirdialog_clicked(entry):
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    entry.set(iDirPath)


# ファイル指定の関数
def filedialog_clicked(entry):
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname(__file__))
    iFilePath = filedialog.askopenfilename(filetype=fTyp, initialdir=iFile)
    entry.set(iFilePath)


# 実行ボタン押下時の実行関数
def conductMain():
    dirPath = entry1.get()
    filePath = entry2.get()
    desPath = entry3.get()
    if dirPath:
        getfile = os.listdir(dirPath)
        if not getfile:
            messagebox.showerror("error", "没有文件")
        else:
            for i in getfile:
                encryptFile(i, dirPath, desPath)
    if filePath:
        encryptFile(os.path.basename(filePath), os.path.dirname(filePath), desPath)


def encryptFile(file, path, des):
    text = ""
    if fileE:
        ba = base64.b64encode(file.encode()).decode().strip().replace('\n', '').replace('\]', '').replace('/', '')
    else:
        ba = file
    temp = '''7za.exe a -m0=zstd -mx1 -mhe=on -pwoshiyy00 -aoa "''' + ba + '''.zst" "''' + path + '''/''' + file + '''"'''
    if des:
        temp = '''7za.exe a -m0=zstd -mx1 -mhe=on -pwoshiyy00 -aoa "''' + des + '''/''' + ba + '''.zst" "''' + path + '''/''' + file + '''"'''
    print(ba)
    process = subprocess.Popen(temp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exitcode = process.wait()
    if exitcode != 0:
        with process.stdout:
            for line in iter(process.stdout.readline, b''):
                if line.decode('cp936'):
                    text += line.decode('cp936')
            messagebox.showinfo("warnning", text)


def conductMain2():
    dirPath = entry1.get()
    filePath = entry2.get()
    desPath = entry3.get()
    if dirPath:
        getfile = os.listdir(dirPath)
        if not getfile:
            messagebox.showerror("error", "没有文件")
        else:
            for i in getfile:
                decryptFile(i, dirPath, desPath)
    if filePath:
        decryptFile(os.path.basename(filePath), os.path.dirname(filePath), desPath)


def decryptFile(file, path, des):
    text = ""
    temp = '''7za.exe x -pwoshiyy00 -aoa "''' + path + '''/''' + file + '''"'''
    if des:
        temp = '''7za.exe x -pwoshiyy00 -aoa "''' + path + '''/''' + file + '''" -o"''' + des + '''"'''
    process = subprocess.Popen(temp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    exitcode = process.wait()
    if exitcode != 0:
        with process.stdout:
            for line in iter(process.stdout.readline, b''):
                if line.decode('cp936'):
                    text += line.decode('cp936')
            messagebox.showinfo("warnning", text)


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    root = ttk.Window(themename="litera")
    ORIGINAL_DPI = 96
    current_dpi = root.winfo_fpixels('1i')
    scale = current_dpi / ORIGINAL_DPI
    width = round(660 * scale)
    height = round(280 * scale)
    root.title("加解密")
    root.geometry(f"{width}x{height}")
    font = ttk.font.Font(root, size=14)
    style = ttk.Style()
    style.configure('.', font=font)

    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=0, column=1, sticky=E)

    IDirLabel = ttk.Label(frame1, text="整个文件夹", padding=(5, 2))
    IDirLabel.pack(side=LEFT)

    entry1 = StringVar()
    IDirEntry = ttk.Entry(frame1, textvariable=entry1, width=60)
    IDirEntry.pack(side=LEFT)

    IDirButton = ttk.Button(frame1, text="浏览", command=lambda: dirdialog_clicked(entry1))
    IDirButton.pack(side=LEFT)

    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=2, column=1, sticky=E)

    IFileLabel = ttk.Label(frame2, text="单一文件", padding=(5, 2))
    IFileLabel.pack(side=LEFT)

    entry2 = StringVar()
    IFileEntry = ttk.Entry(frame2, textvariable=entry2, width=60)
    IFileEntry.pack(side=LEFT)

    IFileButton = ttk.Button(frame2, text="浏览", command=lambda: filedialog_clicked(entry2))
    IFileButton.pack(side=LEFT)

    frame3 = ttk.Frame(root, padding=10)
    frame3.grid(row=5, column=1, sticky=E)

    TDirLabel = ttk.Label(frame3, text="目标文件夹", padding=(5, 2))
    TDirLabel.pack(side=LEFT)

    entry3 = StringVar()
    TDirEntry = ttk.Entry(frame3, textvariable=entry3, width=60)
    TDirEntry.pack(side=LEFT)

    TDirButton = ttk.Button(frame3, text="浏览", command=lambda: dirdialog_clicked(entry3))
    TDirButton.pack(side=LEFT)

    frame4 = ttk.Frame(root, padding=10)
    frame4.grid(row=7, column=1)

    fileE = BooleanVar()
    fileE.set(True)
    CheckBox = ttk.Checkbutton(frame4, text="文件名加密", variable=fileE, bootstyle="round-toggle")
    CheckBox.pack()

    frame5 = ttk.Frame(root, padding=10)
    frame5.grid(row=9, column=1)

    button1 = ttk.Button(frame5, text="加密", command=conductMain)
    button1.pack(side=LEFT, padx=10)
    button2 = ttk.Button(frame5, text="解密", command=conductMain2)
    button2.pack(side=LEFT, padx=10)

    label = ttk.Label(root, text="注意:文件夹或文件任选其一\n无目标文件夹时自动设置为程序所在文件夹")
    label.grid(row=10, column=1, sticky=W)

    root.mainloop()
