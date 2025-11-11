import customtkinter as custom
from tabs.calculator.Calvat import Calvat
from tabs.calculator.HomeCredit import HomeCredit

class Calculator(custom.CTkTabview):
    def __init__(self,parent):
        super().__init__(parent)
        # DIMENSION_X = 1050
        # DIMENSION_Y = 650
        self.configure(width = 1050, height = 650)

        self.calVat = self.add("Calvat")
        self.homecreditVat = self.add("HomeCredit")

        self.set("Calvat")
        self.grid()
        self._segmented_button.grid(sticky="W")
   
        Calvat(self.calVat)
        HomeCredit(self.homecreditVat)
