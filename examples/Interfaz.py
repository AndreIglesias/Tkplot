try:
	import tkinter as tk
except:
	import Tkinter as tk
import threading
import random
class Tarjeta(object):
	"""docstring for Tarjeta"""
	def __init__(self, master = None, coords = None, color = "black", image = None):
		super(Tarjeta, self).__init__()
		self.master = master
		self.coords = coords
		if (len(self.coords) != 2) and (len(self.coords) != 4):
			raise ValueError("2 points to form a rectangle")
		if len(self.coords) == 2:
			puntos = []
			for i in self.coords:
				if type(i) != tuple:
					raise ValueError("4 points to form a rectangle")
				else:
					puntos += list(i)
			self.coords = puntos

		self.color = color
		self.shape = self.master.create_polygon(self.coords[0], self.coords[1], self.coords[2], 
			self.coords[1], self.coords[2], self.coords[3], self.coords[0], self.coords[3], fill = self.color)
		print("<class Tarjeta>")
		self.master.bind("<Button-1>", self.press)

	def press(self, event = None):
		r = lambda: random.randint(0,100)
		self.master.itemconfig(self.shape, fill = '#%02X%02X%02X' % (r(),r(),r()))
		x = (self.coords[0]+self.coords[2])/2
		y = (self.coords[1]+self.coords[3])/2
		coords = self.master.coords(self.shape)
		verticalArriba = -2
		verticalAbajo = -2
		horizontalDrcha = -2
		horizontalIzq = -2
		if event.x < x:
			horizontalIzq = 2
		else:
			horizontalDrcha = 2
		if event.y < y:
			verticalArriba = 2
		else:
			verticalAbajo = 2
		for i in range(10):
			coords = self.master.coords(self.shape)
			self.master.coords(self.shape, coords[0] + verticalArriba, coords[1] + horizontalIzq, 
				coords[2] - verticalArriba, coords[3] + horizontalDrcha, coords[4] - verticalAbajo,
				coords[5] + horizontalIzq, coords[6] + verticalAbajo, coords[7] + horizontalDrcha)
			self.master.update()
			self.master.after(10)
		self.master.after(10)
		for i in range(10):
			coords = self.master.coords(self.shape)
			self.master.coords(self.shape, coords[0] - verticalArriba, coords[1] - horizontalIzq, 
				coords[2] + verticalArriba, coords[3] - horizontalDrcha, coords[4] + verticalAbajo,
				coords[5] - horizontalIzq, coords[6] - verticalAbajo, coords[7] - horizontalDrcha)
			self.master.update()
			self.master.after(10)


def DetectButton(ID, event = None):
	ID.config(bg = "#212f3d") #"#17202a") 

def LeaveButton(ID, event = None):
	ID.config(bg = "#1c2833")

def moveHeader(event = None, operator = '<', number = -8):
	if operator == "<":
		frameHeader.unbind("<Motion>")
		frameHeader.bind('<Leave>', lambda event, arg1 = '>', arg2 = -50: moveHeader(event, arg1, arg2))
	else:
		frameHeader.unbind('<Leave>')
		frameHeader.bind("<Motion>", moveHeader)

	x = int(frameHeader.place_info()['x'])
	y = int(frameHeader.place_info()['y'])
	condition = eval(str(y) + operator + str(number))
	while condition:
		condition = eval(str(y) + operator + str(number))
		try:
			if operator == "<":
				frameHeader.place(x = x, y = y+1)
			else:
				frameHeader.place(x = x, y = y-1)
		except: pass
		window.update()
		window.after(2)
		x = int(frameHeader.place_info()["x"])
		y = int(frameHeader.place_info()["y"])

def movHeader(event = None, operator = '<', number = -8):
	hilo = threading.Thread(target = mHeader, args = (operator, number), daemon = True)
	hilo.start()

# ==========================================================================================
# MAIN
# ==========================================================================================

window = tk.Tk()
print(window.winfo_screenwidth())
window.title("Homogeneous Project")
f = tk.Canvas(window, width = 1250, height = 700, bg = "#308180")
f.pack()
print(tk.Canvas.create_polygon)
#shape = f.create_polygon((300,300),(600,300),(300,600),(600,600),fill = "black") #UPLEFT UPRIGH DWLEFT DWRIGHT
f.create_oval(300-5,300-5,300+5,300+5, fill = 'red')
f.create_oval(600-5,300-5,600+5,300+5,fill = 'green')
f.create_oval(300-5,600-5,300+5,600+5,fill = 'yellow')
f.create_oval(600-5,600-5,600+5,600+5,fill = 'blue')
'''
foto = tk.PhotoImage(file="./Images/a.png")
label = tk.Label(f, image=foto)
label.place(x = 0, y = 0)
label.photo = foto
'''

Tarjeta(f, coords = (300,300,600,600))


frameHeader = tk.Frame(f, width = 1250, height = 62, bg = "gray12")
frameHeader.place(x = 0, y = -50)


frameHome = tk.Frame(f, width = 200, height = 700, bg = "#17202a")
frameHome.place(x = -0, y = 0)											# x = 0

NumButtons = 6
Buttons = []
for Button in range(NumButtons):
	B = tk.Label(frameHome, width = 24, height = 4, bg = "#1c2833")
	B.place(x = -0, y = Button*62)  # 212f3d								# x = 0
	Buttons.append(B)

Tarjeta

OptionSqrs = []
colors = []
Jugadores = []
for i in range(len(Jugadores)):
	O = tk.Label(frameHome, width = 24, height = 4, bg = "#1c2833")

# ------------------------------------------------------------------------------------------
# EVENTS AND BINDINGS
# ------------------------------------------------------------------------------------------
frameHeader.bind('<Motion>', moveHeader)
frameHeader.bind('<Leave>', lambda event, arg1 = '>', arg2 = -50: moveHeader(event, arg1, arg2))

list(map(lambda Button: Button.bind("<Motion>", lambda event, 
	arg = Button: DetectButton(arg, event)), Buttons))

list(map(lambda Button: Button.bind("<Leave>", lambda event, 
	arg = Button: LeaveButton(arg, event)), Buttons))

window.bind("<Escape>", quit)

tk.mainloop()
