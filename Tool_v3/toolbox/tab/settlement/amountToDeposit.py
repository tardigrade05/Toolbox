import dearpygui.dearpygui as dpg
from toolbox.customWidget.customWidgets import LabelInput
from toolbox.utilities.helper import max_char,realtime
from toolbox.models import AtdTables_Model
from sqlalchemy import select
from toolbox import session

class AmountToDeposit:
    def __init__(self):
        self.INPUT_INDENT = 205# + 215
        self.WIDTH = 160
        self.TEXT_INPUT_INDENT = 0
        self.UNIQUE = 'amount_to_deposit'

        self.amountToDeposit_widgets = [
            ('TOTAL SALES','total_sales'),
            ('CARD','card'),
            ('HOME CREDIT','homeCredit'),
            ('PAYTS RA!','normal'),
            ('BILLEASE','billease'),
            ('FORM 2307','form'),
            ('BANK TRANS','bankTrans'),
            ('EXPENSES','expenses')
        ]

        with dpg.theme() as self.atdInput_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text,(60, 133, 250) , category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border,(60, 133, 250) , category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(255,255,255) , category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 3 , category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4 , category=dpg.mvThemeCat_Core)
        

        dpg.add_spacer(height = 5)
        with dpg.group(horizontal = True, pos=(10,350),tag = 'atd_container'):

            self.title_lbl_show(widgets = self.amountToDeposit_widgets[0:4])
            self.input_text_show(widgets = self.amountToDeposit_widgets[0:4])
            

            with dpg.group(horizontal = True, pos = [390,350]):
                self.title_lbl_show(widgets = self.amountToDeposit_widgets[4:8])
                self.input_text_show(widgets = self.amountToDeposit_widgets[4:8])

        dpg.bind_item_font('atd_container','medium_bold')
        dpg.bind_item_theme('atd_container', 'corner_radius')

        dpg.add_spacer(height = 160)

        with dpg.group(horizontal = True , tag = 'amountToDeposit_container'):
            dpg.add_text(default_value = 'AMOUNT TO DEPOSIT')
            dpg.add_input_text(tag = 'amount_to_deposit_atd_input',width = self.WIDTH+189.5,decimal = True, readonly =True)

        
        dpg.bind_item_font('amountToDeposit_container','large_x_bold')
        dpg.bind_item_theme('amount_to_deposit_atd_input', self.atdInput_theme)
                

        exist_total_sales = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'total_sales')).first()
        if exist_total_sales is not None:
            total_sales = exist_total_sales.value
        else:
            total_sales = '0'
        
        dpg.configure_item('total_sales_atd_input',default_value = total_sales, readonly = False,callback = lambda s,a,u: self.press(s,a,u),auto_select_all = True)
  

    
    def title_lbl_show(self,widgets:list):
        with dpg.group() as container:
            for title ,tag in widgets:
                dpg.add_text(tag = f'{tag}_atd_lbl',  default_value = title)

    def input_text_show(self,widgets:list):
        with dpg.group() as container:
            for _,tag in widgets:
                dpg.add_input_text(tag=f'{tag}_atd_input', width=self.WIDTH, decimal=True,readonly = True)
        
        dpg.bind_item_font(container,'medium')

    def press(self,sender,app_data,user_data):
        if max_char(tag_name=sender,data= app_data,number=7):
            return
        exist_total_sales = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'total_sales')).first()
        if exist_total_sales is not None:
            exist_total_sales.value  = app_data
        else:
            total_sales = AtdTables_Model(
                category = 'total_sales',
                tag = 'total_sales',
                value = app_data
            )
            session.add(total_sales)
        session.commit()
        realtime()

        
