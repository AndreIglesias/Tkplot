try: from Tkinter import *
except: from tkinter import *
import string
from math import *
from tkplot import *
colores = ['red', 'blue', 'green', 'black']

def plotGraph(funcion):
    global ventana
    global c
    global instanciar
    instanciar += 1
    if instanciar == 1:
        c = CPlot(ventana, bg = 'white', fg = 'green', do = False)
    AM = AlgebraicManipulation(funcion)
    funcion = AM.expresion
    c.plot(color = colores[instanciar%len(colores)], fx = funcion)

def continuar(event = None):
    if entrada.get() != "":
        cont = 0
        letras = []
        for letter in string.ascii_letters:
            if letter in entrada.get():
                letras.append(letter)
                cont += 1
        if cont < 100:
            try:
                plotGraph(entrada.get())
                c.place(x = 0, y = 0)
            except: pass

def Blank(event = None):
    global i
    if i == 0:
        Entrada.set("")
        entrada.config(fg='Black')
        i = 1

# ======================================================================================
# MAIN
# ======================================================================================

ventana = Tk()
ventana.bind("<Escape>", quit)
ventana.resizable(0,0)
ventana.title("Graph T")
canvas = Canvas(ventana, height = 500, width = 700, bg = "gray10")
canvas.pack()
instanciar = 0
c = None
i = 0
foto = PhotoImage(file="./Images/blue.png")
label1 = Label(ventana, image=foto)
label1.place(x = 0, y = 0)
label1.photo = foto

canvas2 = Canvas(ventana, height = 250, width = 500, bg = "lavender")
canvas2.place(x = 100, y = 130)

POS = 130
Xint = Label(canvas2, text = "eje X", bg = 'lavender')
Xint.place(x = int(canvas2['width'])-POS, y = 30)
intervaloX = Scale(canvas2, bg = 'lavender', from_= 0, to = 50, orient = HORIZONTAL)
intervaloX.place(x = int(canvas2['width'])-POS, y = 50)

Entrada = StringVar()
Entrada.set("f(x)")
canvas2.create_rectangle(48,198,458,222,fill = 'white', width = 0)
entrada = Entry(ventana, width = 50, textvariable = Entrada, fg = "gray40")
entrada.place(x = int(canvas["width"])/2 - 200, y = int(canvas["height"])/2 + 80)
entrada.bind("<Key>", Blank)
entrada.bind("<ButtonPress-1>", Blank)

lbl = Label(canvas2, text = "Enter what you want to graph:", font = ("Arial", 12), fg = "gray10", bg = "lavender")
lbl.place(x = 50, y = 176)

BContinuar = Button(ventana, text = "Continuar", font = ("Arial, 12"), fg = "gray10", bg = "gray50", command = continuar)
entrada.bind("<Return>", continuar)
BContinuar.place(x = int(canvas["width"]) - 130, y = int(canvas["height"])-50)

mainloop()