"""This module contains code for the main window"""

from tkinter import BOTH, CENTER, LEFT, RAISED, TOP, X, ttk
from tkinter.ttk import Frame, Checkbutton, Label, Button

from dppeeper.ic.ic_definition import ICDefinition
from dppeeper.ui.ui_utilities import UIUtilities

class MainWin(Frame):
    _ic_definition: ICDefinition

    _IC_NAME_LABEL_STYLE = 'ICNAME.TLabel'

    _POWER_LABEL_STYLE = 'PWR.TLabel'
    _HI_LABEL_STYLE = 'HI.TLabel'
    _LO_LABEL_STYLE = 'LO.TLabel'
    _Z_LABEL_STYLE = 'Z.TLabel'

    _RESET_BUTTON_STYLE = 'RESET.TButton'

    def __init__(self, name: str, ic_definition: ICDefinition) -> None:
        super().__init__()

        self._ic_definition = ic_definition

        self.buildStyles()
        self.initUI(name)

    def centerWindow(self):
        w = 400
        h = 600

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w)//2
        y = (sh - h)//2

        self.master.geometry(f'{w}x{h}+{x}+{y}')

    def buildStyles(self) -> None:
        style = ttk.Style()

        style.configure(self._IC_NAME_LABEL_STYLE, font=('Arial', '16', 'bold'))
        style.configure(self._POWER_LABEL_STYLE, background='#AAAAAA')
        style.configure(self._HI_LABEL_STYLE, background='#B7FFB7')
        style.configure(self._LO_LABEL_STYLE, background='#FFB7B7')
        style.configure(self._Z_LABEL_STYLE, background='#FFF4B7')

        style.configure(self._RESET_BUTTON_STYLE, font=('Sans','10','bold'), foreground='red')        

    def initUI(self, name: str) -> None:
        name_label = Label(self, text=self._ic_definition.name, anchor=CENTER, style=self._IC_NAME_LABEL_STYLE)
        name_label.pack(side=TOP, anchor=CENTER, fill=X)

        grid_w: int; grid_h: int
        grid_w, grid_h = UIUtilities.calculateGridSize(self._ic_definition.pins_per_side)

        grid_frame = Frame(self)
        grid_frame.pack(side=TOP, anchor=CENTER)
        for col in range(0, grid_w):
            grid_frame.columnconfigure(col, pad=15)
        for row in range(0, grid_h):
            grid_frame.rowconfigure(row, pad=10)
        
        for i, pin in enumerate(self._ic_definition.zif_map):
            l_x: int; l_y: int
            c_x: int; c_y: int
            l_x, l_y = UIUtilities.calculatePinPosition(i + 1, True, self._ic_definition.pins_per_side)
            c_x, c_y = UIUtilities.calculatePinPosition(i + 1, False, self._ic_definition.pins_per_side)

            if pin == 21: # GND pins
                gnd_lbl = Label(grid_frame, text='GND', width = 6, anchor=CENTER, style=self._POWER_LABEL_STYLE)
                gnd_lbl.grid(row=l_y, column=l_x)
            elif pin == 42: # Power pins
                pwr_lbl = Label(grid_frame, text='PWR', width = 6, anchor=CENTER, style=self._POWER_LABEL_STYLE)
                pwr_lbl.grid(row=l_y, column=l_x)
            else:
                gen_lbl = Label(grid_frame, text=self._ic_definition.pin_names[i], width = 6, anchor=CENTER, style=self._LO_LABEL_STYLE)
                gen_lbl.grid(row=l_y, column=l_x)
                gen_chk = Checkbutton(grid_frame, text=None, takefocus=False)
                gen_chk.invoke()
                gen_chk.grid(row=c_y, column=c_x)

        button_frame = Frame(self, relief=RAISED, borderwidth=1, padding=5)
        button_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=CENTER)

        inner_button_frame = Frame(button_frame)
        inner_button_frame.pack(side=TOP, anchor=CENTER)

        set_button = Button(inner_button_frame, text='SET')
        set_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)
        read_button = Button(inner_button_frame, text='READ')
        read_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)
        clear_button = Button(inner_button_frame, text='CLEAR')
        clear_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)
        pcycle_button = Button(inner_button_frame, text='P.CYCLE', style=self._RESET_BUTTON_STYLE)
        pcycle_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)

        clock_button_frame = Frame(button_frame)
        clock_button_frame.pack(side=TOP, anchor=CENTER)
        
        for i, clk_pin in enumerate(self._ic_definition.clk_pins):
            clk_button = Button(clock_button_frame, text=f'Clock {i+1}')
            clk_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)

        self.pack(fill=BOTH, expand=1)

        self.master.title(name)
