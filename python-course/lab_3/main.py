from tkinter import Tk, Canvas
from module import *

field = None

tk = Tk()

canvas = draw_rectagles_and_return_array(Canvas, "data.txt")

fill(canvas, 11, 22, "red", "full")
fill(canvas, 11, 22, "gray", "horiz")
canvas.pack()
tk.mainloop()
