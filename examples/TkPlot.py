# ============================================================================================
# AUTHORS		: QEDD & Ldar01
# PROGRAM		: TkPlot.py
# DESCRIPTION	: Library based on Tkinter.
# DATE			: 12/7/17
# ============================================================================================
from math import *
try:
	import tkinter
except:
    import Tkinter

class CPlot(tkinter.Canvas):
	"""docstring for CPlot"""
	def __init__(self, window = None, fg = 'black', fx = "x^2", interval = (-50, 50), precision = 0.0001,
		bg = None, bd = None, borderwidth = None, 
	 	closeenough = None, confine = None, cursor = None, height = None, 
	 	highlightbackground = None, highlightcolor = None, highlightthickness = None, 
		 insertbackground = None, insertborderwidth = None, insertofftime = None, 
		 insertontime = None, insertwidth = None, offset = None, relief = None, 
		 scrollregion = None, selectbackground = None, selectborderwidth = None, 
		 selectforeground = None, state = None, takefocus = None, width = None, 
		 xscrollcommand = None, xscrollincrement = None, yscrollcommand = None, 
		 yscrollincrement = None):
		super(CPlot, self).__init__(master = window, bg = bg, bd = None, 
			borderwidth = borderwidth, closeenough = closeenough, 
			confine = confine, cursor = cursor, height = height, 
			highlightbackground = highlightbackground, 
			highlightcolor = highlightcolor, highlightthickness = highlightthickness,
			insertbackground = insertbackground, insertborderwidth = insertborderwidth, 
			insertofftime = insertofftime, insertontime = insertontime, 
			insertwidth = insertwidth, offset = offset, relief = relief, 
			scrollregion = scrollregion, selectbackground = selectbackground, 
			selectborderwidth = selectborderwidth, selectforeground = selectforeground, 
			state = state, takefocus = takefocus, width = width, 
			xscrollcommand = xscrollcommand, xscrollincrement = xscrollincrement, 
			yscrollcommand = yscrollcommand, yscrollincrement = yscrollincrement)
		self.window = window
		self.fx = fx
		self.fg = fg
		self.fx = (self.fx.replace("^", "**")).replace(")(", ")*(")
		self.interval = interval
		self.precision = precision

		self.vScroll = tkinter.Scrollbar(self, orient = 'vertical', command = self.yview)
		self.vScroll.grid(row = 0, column = 1, sticky = 'ns')
		self.configure(yscrollcommand = self.vScroll.set)

	def images(self):
		x, y = [], []
		iterator = self.interval[0] - self.precision
		while iterator <= self.interval[1]:
			iterator += self.precision
			try:
				function = self.fx.replace("x", "({0})".format(iterator))
				evaluation = eval(function)
			except:
				continue
			x.append(iterator)
			y.append(evaluation)




if __name__ == '__main__':
	window = tkinter.Tk()
	c = CPlot(window, width = 500, height = 500, bg = 'red')
	c.pack()
	print(c["width"])
	tkinter.mainloop()