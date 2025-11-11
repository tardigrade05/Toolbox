import customtkinter  as custom
from customWidget.TextInput import TextInput
from utilities.helper import add_comma
import math

class HomeCredit(custom.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.LBL_FONT = custom.CTkFont('Helvetica',30,'bold')
        self.ENTRY_FONT = custom.CTkFont('Helvetica',30)

        
        self.LBL_WIDTH = 325
        self.ENTRY_WIDTH = 325
        self.PADDING_X = 10
        self.PADDING_Y = 5

        self.widgets()

    def widgets(self):
        self.initial = TextInput(self,"INITIAL PRICE",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.initial.entry.bind("<KeyRelease>",self.press)
        
        self.six_months = TextInput(self,"6 MONTHS INT.",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.nine_months = TextInput(self,"9 MONTHS INT.",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.twelve_above_months = TextInput(self,"12/15/18 MONTHS INT.",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)

        self.pack()


    def formula(self,value):
        six_months = 0.06
        nine_months = 0.08
        twelve_above_months = 0.13

        six_total = math.ceil(value + (value*six_months))
        nine_total = math.ceil(value + (value*nine_months))
        twelve_above_total = math.ceil(value + (value*twelve_above_months))

        self.unabled()
        self.clear()
        self.six_months.entry.insert(0,add_comma(six_total))
        self.nine_months.entry.insert(0,add_comma(nine_total))
        self.twelve_above_months.entry.insert(0,add_comma(twelve_above_total))
        self.disabled()

    def disabled(self):
        self.six_months.entry.configure(state = 'disabled')
        self.nine_months.entry.configure(state = 'disabled')
        self.twelve_above_months.entry.configure(state = 'disabled')

    def unabled(self):
        self.six_months.entry.configure(state = 'normal')
        self.nine_months.entry.configure(state = 'normal')
        self.twelve_above_months.entry.configure(state = 'normal')

    def press(self,e):
        try:
            new_val = float(self.initial.entry.get())
        except:
            new_val = 0
        
        self.formula(new_val)

    def clear(self):
        self.six_months.entry.delete(0,'end')
        self.nine_months.entry.delete(0,'end')
        self.twelve_above_months.entry.delete(0,'end')