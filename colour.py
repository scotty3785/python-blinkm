# File: clrpick.py
#    http://infohost.nmt.edu/tcc/help/pubs/tkinter//dialogs.html#tkColorChooser

from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import *

#from demopanels import MsgPanel, SeeDismissPanel
from blinkm import blinkm

class ColorPickDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='clrpickdemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('BlinkM Color Picker Demo')
        self.isapp = isapp
        self._create_widgets()
        self.bm = blinkm(0x09)
        self.bm.goToRGB((0,0,0))
        self.bm.setFadeSpeed(4)
        self.prev_color = (0,0,0)
        
    def _create_widgets(self):
        self.lblColor = Label(self,text="Color")
        self.lblColor.pack(side=TOP)
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = ttk.Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        bgBtn = ttk.Button(demoPanel, text='Go to Colour',
                           width=25, name='bgBtn',
                           command=lambda: self._set_color('goto'))
        fgBtn = ttk.Button(demoPanel, text='Fade to Colour',
                           width=25, name='fgBtn',
                           command=lambda: self._set_color('fade'))
        bgBtn.pack(side=TOP, anchor=CENTER, pady='2m')
        fgBtn.pack(side=TOP, anchor=CENTER, pady='2m')

    def _set_color(self, opt):
        
        # askcolor() returns a tuple of the form
        # ((r,g,b), hex) or (None, None) if cancelled
        color = askcolor(parent=self,
                         title='Choose a {} color'.format(opt),
                         initialcolor=self.prev_color)
        if color[0]:
            hex_colour = color[1]
            r,g,b = color[0]
            r = int(r)
            g = int(g)
            b = int(b)
            self.prev_color = color = (r,g,b)
            if opt == "goto":
                print("Goto Colour {}".format(color))
                self.bm.goToRGB(color)
            elif opt == "fade":
                print("Fade Colour {}".format(color))
                self.bm.fadeToRGB(color)
            self.lblColor['bg'] = hex_colour

if __name__ == '__main__':
    ColorPickDemo().mainloop()
