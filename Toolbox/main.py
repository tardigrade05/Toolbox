from tabs.calculator.Calculator import Calculator
import customtkinter as custom
import calVat as CV
import settlement as SM
import sortItemPrice as SORT_PRICE
import joRma as JR
import search as SEARCH

#import settings as SETTINGS

#import game as GAME

custom.set_appearance_mode("Dark")
custom.set_default_color_theme("dark-blue")
DEMENSION_X = 1050
DEMENSION_Y = 650
root  = custom.CTk()
root.title("ToolBox")
root.geometry(F"{DEMENSION_X}x{DEMENSION_Y}")
#root.iconbitmap("images/tool-box.ico")
#root.resizable(0,0)

tabview = custom.CTkTabview(root,width=DEMENSION_X,height=DEMENSION_Y)

calculator = tabview.add("Calculator")
settlement = tabview.add("Settlement")
sortPrice = tabview.add("SortPrice")
jo_rma_Tab = tabview.add("Jo/Rma")  # add tab at the end
search = tabview.add("Search")  # add tab at the end

# games = tabview.add("Games")
# settingTab = tabview.add("Settings")

tabview.set("Search")
tabview.grid(padx=5, pady=5)
tabview._segmented_button.grid(sticky="W")


Calculator(calculator)
#CV.calVatWindow(calVat)
SM.settlement(settlement)
SORT_PRICE.sortItemPriceWindow(sortPrice)
JR.joRmaMain(jo_rma_Tab)
SEARCH.searchWindow(search,root)



#GAME.gameWindow(games)
#SETTINGS.settingWindow(settingTab)


root.mainloop()