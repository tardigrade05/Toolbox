import customtkinter as custom
from utilities.helper import deal_with_decimal,add_comma
from customWidget.TextInput import TextInput

class Calvat(custom.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.FLOATS_VALUES = 1000
        self.LBL_WIDTH = 325
        self.ENTRY_WIDTH = 325
        self.PADDING_Y = (5,0)
        self.PADDING_X = 10
        self.LBL_FONT = custom.CTkFont('Helvetica',29,'bold')
        self.ENTRY_FONT = custom.CTkFont('Helvetica',29)

        self.widgets()

        self.pack(fill = custom.BOTH,expand = True)

    def widgets(self):
        self.totalSales = TextInput(self,"TOTAL SALES",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.totalSales.entry.bind("<KeyRelease>", lambda e: self.press(e,self.totalSales.entry))

        self.optionPublicOrPrivate = custom.CTkComboBox(self,values=["Private",'Public'],width=100, command= lambda e: self.press(e,self.totalSales.entry))
        self.optionPublicOrPrivate.place(x=115,y = 0)
        
        self.lessVat = TextInput(self,"LESS: 12% VAT",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.netVal = TextInput(self,"NET OF VAT/TOTAL",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.lessPwd = TextInput(self,"LESS:SC/PWD DISC.",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.totalDue = TextInput(self,"TOTAL DUE",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.lessWithHolding = TextInput(self,"LESS: WITHHOLDING",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.totalAmountDue = TextInput(self,"TOTAL AMOUNT DUE",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.vatable = TextInput(self,"VATABLE(V)",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.vatExempt = TextInput(self,"VAT-EXEMPT(E)",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.zeroRated = TextInput(self,"ZERO RATED(Z)",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.vat = TextInput(self,"VAT(12%)",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)
        self.total = TextInput(self,"TOTAL",self.PADDING_X,self.PADDING_Y,'e',self.LBL_FONT,self.LBL_WIDTH,self.ENTRY_FONT,self.ENTRY_WIDTH)

    def clear(self):
        self.lessVat.entry.delete(0,'end')
        self.netVal.entry.delete(0,'end')
        self.lessWithHolding.entry.delete(0,'end')
        self.totalAmountDue.entry.delete(0,'end')
        self.total.entry.delete(0,'end')

    def disabled(self):
        self.lessVat.entry.configure(state = 'disabled')
        self.netVal.entry.configure(state = 'disabled')
        self.lessWithHolding.entry.configure(state = 'disabled')
        self.totalAmountDue.entry.configure(state = 'disabled')
        self.total.entry.configure(state = 'disabled')

    def unabled(self):
        self.lessVat.entry.configure(state = 'normal')
        self.netVal.entry.configure(state = 'normal')
        self.lessWithHolding.entry.configure(state = 'normal')
        self.totalAmountDue.entry.configure(state = 'normal')
        self.total.entry.configure(state = 'normal')
     
    def set_entry_value(self, lessVat:str= "", netVal:str= "",lessWithHolding:str= "",totalAmountDue:str= "",total:str= ""):
        self.unabled()
        self.clear()
        self.lessVat.entry.insert(0,add_comma(lessVat))
        self.netVal.entry.insert(0,add_comma(netVal))
        self.lessWithHolding.entry.insert(0,add_comma(lessWithHolding))
        self.totalAmountDue.entry.insert(0,add_comma(totalAmountDue))
        self.total.entry.insert(0,add_comma(total))
        self.disabled()

    def press(self,e,entry):
        contain = entry.get()
        max_chars = 12
        if len(entry.get()) > max_chars:
            contain = entry.get()[:max_chars]
            entry.delete(0, 'end')
            entry.insert(0, contain)

            return

        try:
            new_val = float(entry.get())
        except:
            new_val = 0
    
        self.formula(new_val)

    def formula(self,value):
        try:
            CONST_VAT = 1.12*self.FLOATS_VALUES #1120
            SIX_PERCENT = 0.06*self.FLOATS_VALUES #60
            ONE_PERCENT = 0.01*self.FLOATS_VALUES #10
            TOTAL_SALES = float(value)*self.FLOATS_VALUES

            if self.optionPublicOrPrivate.get() == "Private":
                PERCENT = ONE_PERCENT
            else:
                PERCENT = SIX_PERCENT

            netVal = deal_with_decimal((TOTAL_SALES/CONST_VAT),self.FLOATS_VALUES) #possible 45.809
            lessVat = TOTAL_SALES - netVal
            lessWithHolding = deal_with_decimal((netVal * PERCENT)/(self.FLOATS_VALUES*self.FLOATS_VALUES),self.FLOATS_VALUES)
            totalAmountDue = TOTAL_SALES-lessWithHolding

            self.set_entry_value(
                lessVat = str(lessVat/self.FLOATS_VALUES),
                netVal = str(netVal/self.FLOATS_VALUES),
                lessWithHolding=str(lessWithHolding/self.FLOATS_VALUES),
                totalAmountDue=str(totalAmountDue/self.FLOATS_VALUES),
                total= value
                )

        except ValueError:
            self.set_entry_value()


