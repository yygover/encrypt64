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


def on_entry_change(*args):
    new_value = entry4.get()
    entry5.set(base64.b64decode(new_value).decode().strip())


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
            k = 0
            count = 0
            for path in getfile:
                if os.path.isfile(os.path.join(dirPath, path)):
                    count += 1
            for i in getfile:
                pb['value'] = k / count * 100
                encryptFile(i, dirPath, desPath)
                k += 1
    if filePath:
        encryptFile(os.path.basename(filePath), os.path.dirname(filePath), desPath)
        pb['value'] = 100


def encryptFile(file, path, des):
    text = ""
    if fileE:
        ba = base64.b64encode(file.encode()).decode().strip().replace('\n', '').replace('\]', '').replace('/', '')
    else:
        ba = file
    temp = '''7za.exe a -m0=zstd -mx1 -mhe=on -pwoshiyy00 -aoa "''' + ba + '''.zst" "''' + path + '''/''' + file + '''"'''
    if des:
        temp = '''7za.exe a -m0=zstd -mx1 -mhe=on -pwoshiyy00 -aoa "''' + des + '''/''' + ba + '''.zst" "''' + path + '''/''' + file + '''"'''
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
            k = 0
            count = 0
            for path in getfile:
                if os.path.isfile(os.path.join(dirPath, path)):
                    count += 1
            for i in getfile:
                pb['value'] = k / count * 100
                decryptFile(i, dirPath, desPath)
                k += 1
    if filePath:
        decryptFile(os.path.basename(filePath), os.path.dirname(filePath), desPath)
        pb['value'] = 100


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
    height = round(400 * scale)
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

    frame6 = ttk.Frame(root, padding=10)
    frame6.grid(row=10, column=1)

    label = ttk.Label(frame6, text="进度")
    label.pack(side=LEFT)
    pb = ttk.Progressbar(
        frame6,
        orient='horizontal',
        mode='indeterminate',
        length=400
    )
    pb.pack(side=LEFT)

    label = ttk.Label(root,
                      text="注意:文件夹或文件任选其一\n无目标文件夹时自动设置为程序所在文件夹\n下面是用来解密加密过的文件名的功能\n将加密过的文件名放入加密文件名栏中即可解密")
    label.grid(row=11, column=1)

    frame7 = ttk.Frame(root, padding=10)
    frame7.grid(row=12, column=1)

    En64Label = ttk.Label(frame7, text="加密文件名", padding=(5, 2))
    En64Label.pack(side=LEFT)

    entry4 = StringVar()
    En64Entry = ttk.Entry(frame7, textvariable=entry4, width=70)
    En64Entry.pack(side=LEFT)
    entry4.trace("w", on_entry_change)

    frame8 = ttk.Frame(root, padding=10)
    frame8.grid(row=13, column=1, sticky=E)

    De64Label = ttk.Label(frame8, text="解密文件名", padding=(5, 2))
    De64Label.pack(side=LEFT)

    entry5 = StringVar()
    De64Entry = ttk.Entry(frame8, textvariable=entry5, width=70)
    De64Entry.pack(side=LEFT)

    root.mainloop()
