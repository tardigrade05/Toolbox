import dearpygui.dearpygui as dpg
import math
from toolbox.utilities.helper import add_comma,max_char

class Homecredit:
    def __init__(self):
        self.WIDTH = 270

        self.calHomecredit_widgets = [
            ('INITIAL PRICE','initial'),
            ('6 MONTHS INT.','six_months'),
            ('9 MONTHS INT.','nine_months'),
            ('12/15/18 MONTHS INT.','twelve_above_months')
        ]

        with dpg.group(horizontal = True,pos=[210,80]):
            with dpg.group(label = 'title' ,tag = 'title_calHomecredit'):
                for item,_ in self.calHomecredit_widgets:
                    dpg.add_text(default_value = item)

            with dpg.group(label = 'input' ,tag = 'input_calHomecredit'):
                for _,item in self.calHomecredit_widgets:
                    dpg.add_input_text(tag=f'{item}_calHomecredit', width=self.WIDTH , decimal=True,readonly = True)

        dpg.bind_item_font('title_calHomecredit','large_bold')
        dpg.bind_item_font('input_calHomecredit','large')
        dpg.bind_item_theme('input_calHomecredit','corner_radius')
        dpg.configure_item('initial_calHomecredit',callback = lambda s,a,u:self.initial_press(s,a,u),readonly = False)

    def initial_press(self,sender,app_data,user_data):
        max_char(tag_name='initial_calHomecredit',data=app_data,number=12)
        try:
            new_val = float(dpg.get_value(f'initial_calHomecredit'))
        except:
            new_val = 0
        
        self.formula(new_val)

    def formula(self,value):
        six_months = 0.06
        nine_months = 0.08
        twelve_above_months = 0.13

        six_total = math.ceil(value + (value*six_months))
        nine_total = math.ceil(value + (value*nine_months))
        twelve_above_total = math.ceil(value + (value*twelve_above_months))

        dpg.set_value(f'six_months_calHomecredit',add_comma(six_total))
        dpg.set_value(f'nine_months_calHomecredit',add_comma(nine_total))
        dpg.set_value(f'twelve_above_months_calHomecredit',add_comma(twelve_above_total))
