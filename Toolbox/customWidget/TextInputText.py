import customtkinter as custom
from customWidget.TextInput import TextInput
from utilities.helper import add_comma

class TextInputText(custom.CTkFrame):
    def __init__(
        self,
        master,
        text:str,
        prod_text:str,
        padx:int | tuple[int,int],
        pady:int | tuple[int,int],
        anchor:str = None,
        lbl_font = None,
        lbl_width:int = 300,
        entry_font = None,
        entry_width:int = 300,
        prod_font = None,
        prod_width = 300

    ):
        super().__init__(master)
        try:
            self.value = float(text.replace(',',""))*1000
        except:
            self.value = float(text)*1000
        self.product = 0

        self.configure(fg_color = 'transparent')

        self.lbl=custom.CTkLabel(self, font = lbl_font,text=text, width = lbl_width) #
        self.entry=custom.CTkEntry(self, font = entry_font, width = entry_width) # 
        self.entry.bind("<KeyRelease>",self.keyRelease)
        self.product_lbl = custom.CTkLabel(self,text=prod_text,width=prod_width,font=prod_font)


        self.lbl.grid(row = 0, column = 0, padx=padx, pady=pady)
        self.entry.grid(row = 0, column = 1, padx=padx, pady=pady)
        self.product_lbl.grid(row = 0,column = 2, padx=padx, pady=pady)

        self.pack()

    def keyRelease(self,e):
        try:
            self.product = (self.value * float(self.entry.get()))/1000
        except:
            self.product = 0
        self.product_lbl.configure(text = add_comma(str(self.product)))
    
    def getProduct(self):
        return self.product