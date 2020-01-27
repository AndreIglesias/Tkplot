# ============================================================================================
# AUTHORS		: QEDD & Ldar01
# PROGRAM		: TkPlot.py
# DESCRIPTION	: Library based on Tkinter.
# DATE			: 12/7/17
# ============================================================================================
from math import *
try:
	import tkinter
	from tkinter import *
except:
    import Tkinter

class CPlot(tkinter.Frame):
	"""docstring for CPlot"""
	def __init__(self, window = None, fg = 'black', fx = "x^2", scrollregion = None, yaxe = None, xaxe = None,
		bg = None, wfg = 1, width = None, height = None, interval = (-50, 50), precision = 0.1,**kwargs):
		super(CPlot, self).__init__(master = window, bg = bg, width = width, height = height, **kwargs)
		
		self.window = window
		self.fx = fx
		self.fg = fg
		self.fx = (self.fx.replace("^", "**")).replace(")(", ")*(")
		self.interval = interval
		self.precision = precision
		self.scrollregion = scrollregion
		self.yaxe = yaxe
		self.xaxe = xaxe
		self.wfg = wfg
		if yaxe == None: self.yaxe = (width)/2
		if xaxe == None: self.xaxe = (height)/2

		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.canvas = tkinter.Canvas(self, bd=0, highlightthickness=0
			, scrollregion = self.scrollregion, bg = bg, height = height, width = width)
		self.canvas.pack()
		self.canvas.bind('<Motion>', self.motion)
		self.xmouse = None
		self.ymouse = None
		self.coordinates = tkinter.Label(self.canvas, text = '(x = None, y = None)', font = ('Arial', 12), bg = bg)
		self.coordinates.place(x = int(self.canvas['width'])-155, y = int(self.canvas['height'])-30)
		'''
		self.vScroll = tkinter.Scrollbar(self.window, orient = 'vertical', command = self.canvas.yview)
		self.vScroll.place(x = 100, y = 100)#grid(row = 0, column = 1, sticky = 'ns')
		self.canvas.configure(yscrollcommand = self.vScroll.set)
		'''
		self.Pgrid((self.yaxe, self.xaxe))
		x, y = self.plot(self.interval, self.precision, fx = self.fx, color = self.fg, wfg = self.wfg)

		

	def motion(self, event = None):
		try:
			self.canvas.delete(self.xmouse)
		except: pass
		try:
			self.canvas.delete(self.ymouse)
		except: pass
		self.xmouse = self.canvas.create_line(0, event.y, self.canvas['width'], event.y, fill = 'gray')
		self.ymouse = self.canvas.create_line(event.x, 0, event.x, self.canvas['height'], fill = 'gray')
		self.coordinates.config(text = '(x = {0}, y = {1})'.format(event.x - self.yaxe, -1*event.y + self.xaxe)) 


	def Pgrid(self, center):
		dist = 10
		for i in range(100):
			if i%2 == 1: 
				self.canvas.create_line(0, i*dist, int(self.canvas['width']), i*dist, fill = 'gray85')
				self.canvas.create_oval(center[0] - 2, i*dist - 2, center[0] + 2, i*dist + 2, fill = 'black')
			else:
				self.canvas.create_line(i*dist, 0, i*dist, int(self.canvas['height']), fill = 'gray85')
				self.canvas.create_oval(i*dist - 2, center[1] - 2, i*dist + 2, center[1] + 2, fill = 'black')

	def plot(self, interval = (-50,50), precision = 0.1, fx = "x**2", color = "green", wfg = 2):
		x, y = [], []
		fx = (fx.replace("^", "**")).replace(")(", ")*(")
		iterator = interval[0] - precision
		while iterator <= interval[1]:
			iterator += precision
			try:
				function = fx.replace("x", "({0})".format(iterator))
				evaluation = eval(function)
			except:
				continue
			x.append(iterator*50)
			y.append(evaluation*50)
			#if iterator > int(self.canvas['width']) and evaluation > int(self.canvas['height']): break
		self.draw(x, y, (self.yaxe, self.xaxe), color, wfg)
		return x, y


	def draw(self, x, y, center, color, wfg):
		self.canvas.create_line(center[0], int(self.canvas['height']), center[0], 0, width = 2)
		self.canvas.create_line(0, center[1], int(self.canvas['width']), center[1], width = 2)
		coords = []
		for i in range(len(x)):
			coords += [x[i] + center[0], -1*y[i] + center[1]]
		try:
			self.canvas.create_line(coords, fill = color, width = wfg)
		except: pass
		return 0
		




if __name__ == '__main__':
	#window = tkinter.Tk()
	#window.grid_rowconfigure(0, weight=1)
	#window.grid_columnconfigure(0, weight=1)

	root=Tk()
	frame=Frame(root,width=300,height=300)
	frame.grid(row=0,column=0)
	canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
	c = CPlot(frame, width = 800, height = 500, bg = 'white', fx = 'x^3', fg = 'green', wfg = 2)
	hbar=Scrollbar(frame,orient=HORIZONTAL)
	hbar.pack(side=BOTTOM,fill=X)
	hbar.config(command=canvas.xview)
	vbar=Scrollbar(frame,orient=VERTICAL)
	vbar.pack(side=RIGHT,fill=Y)
	vbar.config(command=canvas.yview)
	canvas.config(width=300,height=300)
	canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
	canvas.pack(side=LEFT,expand=True,fill=BOTH)


	#c.grid(row = 0, column = 0)
	c.pack()
	#print(c["width"])
	c.plot(color = 'red', fx = 'x^2 * sin(x)')
	c.plot(color = 'blue', fx = 'cos(x+3)*sin(x*2)')
	c.plot(color = 'black', fx = 'x')
	tkinter.mainloop()