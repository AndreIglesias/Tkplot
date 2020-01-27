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

class MessageItem(Frame):
    """A message to be contained inside a scrollableContainer"""

    def __init__(self, master, message, **kwds):
        Frame.__init__(self, master, **kwds)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.text = Label(self, text=message, anchor='w', bg='gold')
        self.text.grid(row=0, column=0, sticky='nsew')

class CPlot(tkinter.Frame):
	"""docstring for CPlot"""
	def __init__(self, window = None, fg = 'black', fx = "x^2",
		interval = (-50, 50), precision = 0.0001,**kwargs):
		super(CPlot, self).__init__(master = window, **kwargs)
		
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.canv = Canvas(self, bd=0, highlightthickness=0)
		self.canv.grid_rowconfigure(0, weight=1)

		self.hScroll = Scrollbar(self, orient='horizontal',
		                         command=self.canv.xview)
		self.hScroll.grid(row=1, column=0, sticky='we')
		self.vScroll = Scrollbar(self, orient='vertical', command=self.canv.yview)
		self.vScroll.grid(row=0, column=1, sticky='ns')
		self.canv.grid(row=0, column=0, sticky='nsew')

		self.canv.configure(xscrollcommand=self.hScroll.set,
		                    yscrollcommand=self.vScroll.set)

		self.messages = []
		for i in range(20):
		    m = MessageItem(self, 'Something Profound', bd=2, bg='black')
		    m.grid(row=i, column=0, sticky='nsew', padx=2, pady=2)
		    self.messages.append(m)

		#self.update_layout()        
		self.canv.bind('<Configure>', self.on_configure)
	
	def on_configure(self, event):
		w,h = event.width, event.height
		natural = self.frm.winfo_reqwidth()
		self.canv.itemconfigure('inner', width= w if w>natural else natural)
		self.canv.configure(scrollregion=self.canv.bbox('all'))

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
	window.grid_rowconfigure(0, weight=1)
	window.grid_columnconfigure(0, weight=1)
	c = CPlot(window, width = 500, height = 500, bg = 'red')
	c.pack()
	print(c["width"])
	tkinter.mainloop()