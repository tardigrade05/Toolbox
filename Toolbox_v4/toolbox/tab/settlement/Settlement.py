import dearpygui.dearpygui as dpg
from toolbox.tab.settlement.cashcount import CashCount
from toolbox.tab.settlement.amountToDeposit import AmountToDeposit
from toolbox.tab.settlement.atdtables import AtdTables
from toolbox.utilities.helper import realtime

class Settlement:
    def __init__(self):
        with dpg.group(horizontal = True):
            with dpg.group():
                CashCount()
                AmountToDeposit()
            AtdTables()

            realtime()
                



