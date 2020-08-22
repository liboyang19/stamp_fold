from tkinter import *

master = Tk()

# frame1 = Frame(master, width=100, height=100, bg="blue", colormap="new")
# frame1.pack()
#
# frame2 = Frame(master, width=100, height=100, bg="red", colormap="new")
# frame2.pack()
#
# frame3 = Frame(master, width=100, height=100, bg="black", colormap="new")
# frame3.pack()

w1 = Label(master, text="Red", bg="red", fg="white")
w1.pack()
w2 = Label(master, text="Green", bg="green", fg="black")
w2.pack()


mainloop()