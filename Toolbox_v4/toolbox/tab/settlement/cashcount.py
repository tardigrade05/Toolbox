import dearpygui.dearpygui as dpg
from toolbox.utilities.helper import max_char,add_comma,clean_data,realtime
from toolbox.models import CashCount_Model,AtdTables_Model
from sqlalchemy import select
from toolbox import session
from pynput.keyboard import Key, Controller
from toolbox.utilities.colorstyles import btnHovered_theme

class CashCount:
    def __init__(self):
        self.WIDTH = 60
        self.keyboard = Controller()
        red_theme = btnHovered_theme(colorHov = (244, 122, 122))

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Up, callback=lambda s,a,u:self.up(s,a,u))
            dpg.add_key_press_handler(dpg.mvKey_Down, callback=lambda s,a,u:self.down(s,a,u))

        self.cashcount_widgets = [
            ('1000', 'one_thousand',100000), #00
            ('500', 'five_hundred',50000),
            ('200', 'two_hundred',20000),
            ('100', 'one_hundred',10000),
            ('50', 'fifty_pesos',5000),
            ('20','twenty_pesos',2000),
            ('10','ten_pesos',1000),
            ('5','five_pesos',500),
            ('1', 'one_peso',100),
            ('.50','fifty_cent',50),
            ('.25','twoFive_cent',25),
            ('.10','ten_cent',10),
            ('.05','five_cent',5),
            ('.01','one_cent',1)
        ]

        with dpg.group(horizontal = True, pos=(170,35),tag = 'cashcount_container'):
            self.title_lbl_show(widgets = self.cashcount_widgets[0:7],category='lbl')
            self.input_text_show(widgets = self.cashcount_widgets[0:7])
            self.title_lbl_show(widgets = self.cashcount_widgets[0:7],category='product',default_val='0')

            with dpg.group(horizontal = True, pos = [410,35]):
                self.title_lbl_show(widgets = self.cashcount_widgets[7:14],category='lbl')
                self.input_text_show(widgets = self.cashcount_widgets[7:14])
                self.title_lbl_show(widgets = self.cashcount_widgets[7:14],category='product',default_val='0')

        dpg.add_spacer(height = 265)
        with dpg.group(horizontal = True):
            dpg.add_input_text(tag = "total_cashcount", width = 170, indent = 270,default_value = 0,readonly =True)
            dpg.add_image_button(texture_tag = 'clear_img', tag = 'clear' , callback = lambda s,a,u:self.clear(s,a,u))

        target_row = session.scalars(select(CashCount_Model)).all()
        if target_row is not None:
            total = 0
            for row in target_row:
                dpg.set_value(row.tag,row.value)
                dpg.set_value(str(row.tag).replace('input','product'),add_comma(int(row.product)/100))
                total += int(row.product)

            dpg.set_value('total_cashcount',add_comma(int(total)/100))

        dpg.bind_item_theme('cashcount_container','corner_radius') 
        dpg.bind_item_theme('total_cashcount','corner_radius') 
        dpg.bind_item_theme('clear',red_theme)
        
        dpg.bind_item_font("cashcount_container","medium")
        dpg.bind_item_font("total_cashcount","medium")

    def clear(self, sender, app_data,user_data):
        tables = [
            'card_atd_tables',
            'homeCredit_atd_tables',
            'billease_atd_tables',
            'form_atd_tables',
            'bankTrans_atd_tables',
            'expenses_atd_tables'
        ]

        for table in tables:
            session.query(AtdTables_Model).filter(AtdTables_Model.category == table).delete()
            dpg.delete_item(f'{table}_table')

        session.query(CashCount_Model).delete()
        session.query(AtdTables_Model).filter(AtdTables_Model.category == 'total_sales').delete()
        
        session.commit()

        for _,tag,_ in self.cashcount_widgets:
            dpg.set_value(f'{tag}_cashcount_input','')
            dpg.set_value(f'{tag}_cashcount_product','0')

        dpg.set_value('total_sales_atd_input','0')
        realtime()

    def title_lbl_show(self,widgets:list,category:str, default_val= None):
        if default_val is None:
            with dpg.group() as container:
                for title ,tag,_ in widgets:
                    dpg.add_text(tag = f'{tag}_cashcount_{category}',  default_value = title)
        else:
            with dpg.group() as container:
                for title ,tag,_ in widgets:
                    dpg.add_text(tag = f'{tag}_cashcount_{category}',  default_value = default_val)

        dpg.bind_item_font(container,'medium_bold')
    
    def input_text_show(self,widgets:list):
        with dpg.group() as container:
            for _,tag,value in widgets:
                dpg.add_input_text(tag=f'{tag}_cashcount_input', width=self.WIDTH, decimal=True, user_data = value,callback = lambda s,a,u:self.press(s,a,u))
        
    def press(self,sender, app_data,user_data):
        if max_char(tag_name=sender,data= app_data,number=2):
            return

        try:
            product = int(user_data) * int(app_data)
        except:
            product = 0

        target_row = session.scalars(select(CashCount_Model).filter(CashCount_Model.tag == sender)).first()

        if target_row is None:
            add_value = CashCount_Model(
                        category = 'cashcount',
                        tag =  sender,
                        value = app_data,
                        product = product
                    )
            session.add(add_value)
            
        else:
            target_row.value = app_data
            target_row.product = product

        session.commit()
        dpg.configure_item(str(sender).replace('input','product'),default_value= add_comma(str(product/100)))
        
        self.total_cashcount()
        realtime()

    def total_cashcount(self):
        total = 0
        all_cashcount = session.scalars(select(CashCount_Model).filter(CashCount_Model.category== 'cashcount')).all()
        for product in all_cashcount:

            total += int(product.product)
        
        dpg.set_value('total_cashcount',add_comma(int(total)/100))

    def up(self, sender, app_data,user_data):
        with self.keyboard.pressed(Key.shift):
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)

    def down(self, sender, app_data,user_data):
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)

