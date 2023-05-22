# https://stackoverflow.com/questions/58127848/tkinter-closing-automatically-a-top-level-window-after-file-is-selected

from tkinter import *
from tkinter import filedialog

window = Tk()
top = Toplevel()


def open_file():
    global demanda
    path = filedialog.askopenfilename()
    demanda = {}
    dia = 0
    with open(path) as f:
        contenido = f.read().split('\n')
        for linea in contenido:
            separado = linea.split()
            for i in range(0, len(separado)):
                demanda[dia] = int(separado[i])
                dia += 1
    top.destroy()

def quit():
    window.destroy()

open_file()
quit()
window.mainloop()
