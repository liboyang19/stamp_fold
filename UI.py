from tkinter import *

root = Tk()

root.title('Canvas')

w = Canvas(root, width=800, height=800)  # background='black' 改变背景色

w.pack()

# 黄色的矩形
w.create_rectangle(60, 60, 800, 800, fill='yellow')  # 参数：左边距, 上边距, 宽, 高


mainloop()