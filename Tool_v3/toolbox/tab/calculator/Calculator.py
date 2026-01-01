import dearpygui.dearpygui as dpg
from toolbox.tab.calculator.calvat import Calvat
from toolbox.tab.calculator.homecredit import Homecredit

class Calculator:
    def __init__(self):

        with dpg.tab_bar():
            with dpg.tab(tag = 'calvat',label="Calvat"):
                Calvat()
            with dpg.tab(tag = 'homecredit',label="Home Credit"):
                Homecredit()

        
        tabs = [
            ('calvat','small_x'),
            ('homecredit','small_x')
        ]

        for tag,font in tabs:
            dpg.bind_item_font(tag,font)