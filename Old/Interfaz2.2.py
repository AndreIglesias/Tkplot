try:
	import tkinter as tk
except:
	import Tkinter as tk
import threading
import random
class Tarjeta(tk.Canvas):
	"""docstring for Tarjeta"""
	def __init__(self, master = None, width = None, height = None, color = None, image = None, **kwargs):
		bg = master["bg"]
		super(Tarjeta, self).__init__(master = master, width = width, height = height, bg = bg, **kwargs)
		self.master = master
		self.width = width
		self.height = height
		self.coordenadas = [20, 20, self.width - 20, self.height - 20]
		self.color = color
		self.shape = self.create_polygon(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], 
			self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], self.coordenadas[0], self.coordenadas[3], fill = self.color)
		print("<class Tarjeta>")
		self.bind("<Button-1>", self.press)

	def press(self, event = None):
		def animaiton(verticalArriba, verticalAbajo, horizontalDrcha, horizontalIzq, Increase = 1):
			tamano = -5 * Increase
			verticalArriba *= Increase
			verticalAbajo *= Increase
			horizontalDrcha *= Increase
			horizontalIzq *= Increase
			
			for i in range(10):
				coordenadas = self.coords(self.shape)
				self.coords(self.shape, coordenadas[0] - tamano, coordenadas[1] - tamano, 
					coordenadas[2] + tamano, coordenadas[3] - tamano, coordenadas[4] + tamano,
					coordenadas[5] + tamano, coordenadas[6] - tamano, coordenadas[7] + tamano)
				self.master.update()
				self.master.after(10)			
			
			tamano = 0
			
			for i in range(10):
				coordenadas = self.coords(self.shape)
				self.coords(self.shape, coordenadas[0] + verticalArriba - tamano, coordenadas[1] + horizontalIzq - tamano, 
					coordenadas[2] - verticalArriba + tamano, coordenadas[3] + horizontalDrcha - tamano, coordenadas[4] - verticalAbajo + tamano,
					coordenadas[5] + horizontalIzq + tamano, coordenadas[6] + verticalAbajo - tamano, coordenadas[7] + horizontalDrcha + tamano)
				self.master.update()
				self.master.after(10)

		self.master.after(10)

		x = (self.coordenadas[0]+self.coordenadas[2])/2
		y = (self.coordenadas[1]+self.coordenadas[3])/2
		coordenadas = self.coords(self.shape)
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

		animaiton(verticalArriba, verticalAbajo, horizontalDrcha, horizontalIzq, Increase = 1)
		animaiton(verticalArriba, verticalAbajo, horizontalDrcha, horizontalIzq, Increase = -1)
		self.master.after(15)

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
f = tk.Frame(window, width = 1250, height = 700, bg = "#308180")
f.pack()

'''
foto = tk.PhotoImage(file="./Images/a.png")
label = tk.Label(f, image=foto)
label.place(x = 0, y = 0)
label.photo = foto
'''

frameHeader = tk.Frame(f, width = int(f["width"]), height = 62, bg = "gray12")
frameHeader.place(x = 0, y = -50)

NwUsr = Tarjeta(f, height = 400, width = 300, highlightthickness = 0, color = "black")
foto = tk.PhotoImage(file="./Images/SignUp.png")
label = tk.Label(f, image=foto)
label.place(x = 70, y = (f["height"])/2 - int(NwUsr["height"])/2 + 100)
NwUsr.place(x = 0, y = (f["height"])/2 - int(NwUsr["height"])/2)
i = 0
while int(NwUsr.place_info()["x"]) < int(f["width"])/2 - int(NwUsr["height"])/2 + 50:
	i += 8
	NwUsr.place(x = i, y = (f["height"])/2 - int(NwUsr["height"])/2)
	label.place(x = i+70, y = (f["height"])/2 - int(NwUsr["height"])/2 + 100)
	window.update()
	window.after(3)

x = int(NwUsr.place_info()["x"])
for i in range(10):
	NwUsr.place(x = x-i*5, y = (f["height"])/2 - int(NwUsr["height"])/2)
	label.place(x = (x+70)-i*5, y = (f["height"])/2 - int(NwUsr["height"])/2 + 100)
	window.update()
	window.after(15)

label.bind("<Button-1>", NwUsr.press)

frameHome = tk.Frame(f, width = 200, height = 700, bg = "#17202a")
frameHome.place(x = -1000, y = 0)											# x = 0

NumButtons = 6
Buttons = []
for Button in range(NumButtons):
	B = tk.Label(frameHome, width = 24, height = 4, bg = "#1c2833")
	B.place(x = -1000, y = Button*62)  # 212f3d								# x = 0
	Buttons.append(B)



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
