import customtkinter as custom


class TextInput(custom.CTkFrame):
    def __init__(
        self,
        master,
        text:str,
        padx:int | tuple[int,int],
        pady:int | tuple[int,int],
        anchor:str = None,
        lbl_font = None,
        lbl_width:int = 300,
        entry_font = None,
        entry_width:int = 300,
        
        ):
        super().__init__(master)
        #self.configure(bg_color = 'blue')

        self.lbl=custom.CTkLabel(self, font = lbl_font,text=text, width = lbl_width) #
        self.entry=custom.CTkEntry(self, font = entry_font, width = entry_width) # 

        self.lbl.grid(row = 0, column = 0, padx=padx, pady=pady)
        self.entry.grid(row = 0, column = 1, padx=padx, pady=pady)

        self.configure(fg_color = 'transparent')
        self.pack()
