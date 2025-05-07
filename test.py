import tkinter as tk
import subprocess

def embed_terminal():
    root = tk.Tk()
    terminal_frame = tk.Frame(root)
    terminal_frame.pack()

    # 运行终端命令
    process = subprocess.Popen("python -?", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 获取终端输出
    output, error = process.communicate()

    # 将输出显示在Tkinter应用程序的界面上
    terminal_text = tk.Text(terminal_frame)
    terminal_text.pack()
    terminal_text.insert(tk.END, output)

    root.mainloop()

if __name__ == "__main__":
    embed_terminal()
