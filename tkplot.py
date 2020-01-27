# ============================================================================================
# AUTHORS		: QEDD
# PROGRAM		: tkplot.py
# DESCRIPTION	: Library based on Tkinter.
# DATE			: 12/7/17
# ============================================================================================
from math import *
try:
    import tkinter
    from tkinter import *
except:
    import Tkinter
try:
    import tkMessageBox
except:
    from tkinter import messagebox


class CPlot(tkinter.Frame):
    """docstring for CPlot"""

    def __init__(self, window=None, fg='black', fx="x^2", scrollregion=None, yaxe=None, xaxe=None, scrollrange=None, do=True,
                 bg=None, wfg=2, width=300, height=300, interval=(-50, 50), vrange=100, scale=50, precision=0.1, **kwargs):
        super(CPlot, self).__init__(master=window, bg=bg, width=width, height=height, **kwargs)

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
        self.scale = scale
        self.vrange = vrange
        if yaxe == None:
            self.yaxe = (width) / 2
        if xaxe == None:
            self.xaxe = (height) / 2
        if scrollregion == None:
            scrollregion = (-width, -height, width * 2, height * 2)
        if scrollrange != None:
            scrollregion = (-scrollrange, -scrollrange, width + scrollrange, height + scrollrange)
        self.scrollregion = scrollregion
        print(self.scrollregion)

        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        self.canvas = tkinter.Canvas(self, bd=0, highlightthickness=0,
                                     scrollregion=self.scrollregion, bg=bg, height=height, width=width)

        self.window.bind('<Motion>', self.motion)
        self.xmouse = None
        self.ymouse = None
        self.coordinates = tkinter.Label(
            self.canvas, text='(x = None, y = None)', font=('Arial', 12), bg=bg)
        self.coordinates.place(x=int(self.canvas['width']) - 155, y=int(self.canvas['height']) - 30)

        hbar = Scrollbar(self, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        vbar.config(command=self.canvas.yview)
        hbar.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        self.Pgrid((self.yaxe, self.xaxe))
        self.functions = []
        if do:
            x, y = self.plot(self.interval, self.precision, fx=self.fx, color=self.fg, wfg=self.wfg)
            if x == []:
                raise ValueError("Invalid Function")

    def ClearButt(self):
        button = ClearButton(master=self.window, )

    class ClearButton(tkinter.Button):
        """docstring for ClearButton"""

        def __init__(self, master=None, width=None, command=None, text="Clear", height=None, **kwargs):
            super(ClearButton, self).__init__(master=window, width=width,
                                              height=height, command=self.command, **kwargs)
            # def clearAll():
            #list(map(lambda x: self.canvas.delete(x), self.functions))
            #self.command = clearAll

    def motion(self, event=None):
        try:
            self.canvas.delete(self.xmouse)
        except:
            pass
        try:
            self.canvas.delete(self.ymouse)
        except:
            pass
        self.xmouse = self.canvas.create_line(
            self.scrollregion[0], event.y, self.scrollregion[-2], event.y, fill='gray')
        self.ymouse = self.canvas.create_line(
            event.x, self.scrollregion[1], event.x, self.scrollregion[-1], fill='gray')
        self.coordinates.config(text='(x = {0}, y = {1})'.format((event.x - self.yaxe) / self.scale,
                                                                 (-1 * event.y + self.xaxe) / self.scale))

    def Pgrid(self, center):
        dist = 10
        for i in range(-self.vrange * self.scale, self.vrange * self.scale):
            widd = 1
            if i % 2 == 1:
                if (i + 1) / 2 % 4 == 0:
                    widd = 2
                self.canvas.create_line(self.interval[0] * (self.scale + 8), i * dist, self.interval[1] * (self.scale + 8),
                                        i * dist, fill='gray85', width=widd)

                self.canvas.create_oval(center[0] - 2, i * dist - 2,
                                        center[0] + 2, i * dist + 2, fill='black')
            else:
                if i / 2 % 4 == 1:
                    widd = 2
                self.canvas.create_line(i * dist, self.interval[0] * self.vrange, i * dist,
                                        int(self.canvas['height']) + self.interval[1] * self.vrange, fill='gray85', width=widd)

                self.canvas.create_oval(
                    i * dist - 2, center[1] - 2, i * dist + 2, center[1] + 2, fill='black')

    def plot(self, interval=(-50, 50), precision=0.1, fx="x**2", color="green", wfg=2):
        x, y = [], []
        numb = '1234567890'
        fx = (fx.replace("^", "**")).replace(")(", ")*(")
        for i in numb:
            fx = (fx.replace(i + 'x', i + '*x')).replace('x' + i, 'x*' + i)
        iterator = interval[0] - precision
        while iterator <= interval[1]:
            iterator += precision
            try:
                function = fx.replace("x", "({0})".format(iterator))
                evaluation = eval(function)
                print(function, " = ", evaluation)
            except:
                continue
            x.append(iterator * self.scale)
            y.append(evaluation * self.scale)
        if x == []:
            try:
                tkMessageBox.showinfo("Invalid Function", "Insert a Valid Function")
            except:
                messagebox.showinfo("Invalid Function", "Insert a Valid Function")
            raise ValueError("Invalid Function")
        else:
            self.draw(x, y, (self.yaxe, self.xaxe), color, wfg)
        return x, y

    def draw(self, x, y, center, color, wfg):
        self.canvas.create_line(center[0], -self.vrange * self.scale * 2,
                                center[0], self.vrange * self.scale * 2, width=2)
        self.canvas.create_line(-self.vrange * self.scale * 2,
                                center[1], self.vrange * self.scale * 2, center[1], width=2)
        coords = []
        for i in range(len(x)):
            coords += [x[i] + center[0], -1 * y[i] + center[1]]
        try:
            self.functions.append(self.canvas.create_line(coords, fill=color, width=wfg))
        except:
            pass
        self.canvas.pack()
        return 0


class AlgebraicManipulation(object):
    """docstring for AlgebraicManipulation"""

    def __init__(self, expresion):
        super(AlgebraicManipulation, self).__init__()
        self.expresion = expresion

        numb = '1234567890'
        self.expresion = self.expresion.replace(")(", ")*(")
        var = ['x', 'y']
        for j in var:
            for i in numb:
                self.expresion = (self.expresion.replace(
                    i + j, i + '*' + j)).replace(j + i, j + '*' + i)

        if self.expresion.count("=") > 1:
            raise ValueError('Not valid extra sign "="')  # VALIDATE

        if self.expresion.count("y^2") > 1:
            raise ValueError('Not valid extra sign "y"')  # VALIDATE

        if "=" in self.expresion:
            self.Ans = self.expresion.split('=')[1]
            self.expresion = self.expresion.split('=')[0]
            for i in range(5):
                expSeparate = self.Separate(self.expresion, {"+", "-"})
                self.expresion, self.Ans = self.ClearTerms(expSeparate, self.Ans)

                self.expresion = self.expresion.replace("-(", "-1*(")
                expSeparate = self.Separate(self.expresion, {"*", "/"})
                self.expresion, self.Ans = self.ClearFactors(expSeparate, self.Ans)

                expSeparate = self.Separate(self.expresion, {"^"})
                self.expresion, self.Ans = self.ClearExponents(expSeparate, self.Ans)

                # print(expSeparate)
                if self.expresion[0] in {"+", "-", "^", "*", "/"}:
                    self.expresion = self.expresion[1:]
                if self.ParenthesisExterior(self.expresion):
                    self.expresion = self.expresion[1:-1]

                #print(self.expresion, '=', self.Ans)
            self.Ans = self.Ans.replace("^", "**")

            if len(self.expresion) == 1:
                try:
                    self.expresion = self.Ans
                except:
                    pass
        self.expresion = self.expresion.replace("^", "**")

    def ParenthesisExterior(self, expresion):
        SameParenthesis = 0
        FstOpen = False
        contParen = 0
        for i in expresion:
            if i == "(":
                contParen += 1
                FstOpen = True
            elif i == ")":
                contParen -= 1

            if (contParen == 0) and FstOpen:
                SameParenthesis += 1
        if SameParenthesis == 1:
            return True
        return False

    def ClearFactors(self, expSeparate, Ans):
        for i in expSeparate:
            if "y" not in i:
                Ans = "(" + Ans + ")"
                Ans += "/" + i
                index = expSeparate.index(i)
                expSeparate.pop(index)
                expSeparate.insert(index, None)
        Ans = Ans.replace('*/', '/').replace('/*', '/').replace('**', '*').replace('//', '*')
        expSeparate = list(filter(lambda x: x != None, expSeparate))
        #print(expSeparate, '=', Ans)
        return expSeparate[0], Ans

    def ClearExponents(self, expSeparate, Ans):
        for i in expSeparate:
            if "y" not in i:
                Ans = "[" + Ans + "]"
                Ans += "^" + i
                if "]^^2" in Ans:
                    Ans = Ans.replace("[", "sqrt(").replace("]^^2", ")")
                index = expSeparate.index(i)
                expSeparate.pop(index)
                expSeparate.insert(index, None)
        Ans = Ans.replace('^^', '^(1.0/')
        expSeparate = list(filter(lambda x: x != None, expSeparate))
        return expSeparate[0], Ans

    def ClearTerms(self, expSeparate, Ans):
        for i in expSeparate:
            if "y" not in i:
                Ans += "-" + i
                index = expSeparate.index(i)
                expSeparate.pop(index)
                expSeparate.insert(index, None)
        Ans = Ans.replace('+-', '-').replace('-+', '-').replace('++', '+').replace('--', '+')
        expSeparate = list(filter(lambda x: x != None, expSeparate))
        return expSeparate[0], Ans

    def strInsert(self, position, string, new):
        return string[:position] + new + string[position:]

    def Separate(self, expresion, operators):
        notParenthesis = 0
        helper = 0
        for i in range(len(expresion)):
            i += helper
            if expresion[i] == "(":
                notParenthesis += 1
            elif expresion[i] == ")":
                notParenthesis -= 1

            if (notParenthesis == 0) and (expresion[i] in set(operators)):
                expresion = self.strInsert(i, expresion, "@")
                helper += 1
        expresion = expresion.split("@")
        return expresion


if __name__ == '__main__':
    AM = AlgebraicManipulation("2x-3-(y^3+1)/(x-2)=-7")
    print(AM.expresion)

    '''
	window = Tk()
	c = CPlot(window, width = 800, height = 500, bg = 'white', fx = 'x^3',
		fg = 'green', wfg = 2, scrollregion=(-500, -1000, 500+1000, 800+1000))
	c.pack()
	c.plot(color = 'red', fx = 'x^2 * sin(x)')
	c.plot(color = 'blue', fx = 'cos(x+3)*sin(x*2)')
	c.plot(color = 'black', fx = 'x')
	tkinter.mainloop()
	'''
