import dearpygui.dearpygui as dpg
import math
from toolbox.utilities.helper import add_comma,max_char, initial_val_db
from toolbox.utilities.colorstyles import btnHovered_theme
from toolbox.models import Settings_Model
from toolbox import session
from sqlalchemy import select

class Homecredit:
    def __init__(self):
        self.WIDTH = 270

        self.calHomecredit_widgets = [
            ('INITIAL PRICE','initial'),
            ('6 MONTHS INT.','six_months'),
            ('9 MONTHS INT.','nine_months'),
            ('12/15/18 MONTHS INT.','twelve_above_months')
        ]

        with dpg.group(pos=[210,80]):
            dpg.add_image_button(texture_tag = 'settings_img',tag = 'homeCredit_settings', pos = (210,60),callback = lambda s,a,u:self.settings(s,a,u))
            dpg.add_spacer(height = 17)
            with dpg.group(horizontal = True):
                with dpg.group(label = 'title' ,tag = 'title_calHomecredit'):
                    for item,_ in self.calHomecredit_widgets:
                        dpg.add_text(default_value = item)

                with dpg.group(label = 'input' ,tag = 'input_calHomecredit'):
                    for _,item in self.calHomecredit_widgets:
                        dpg.add_input_text(tag=f'{item}_calHomecredit', width=self.WIDTH , decimal=True,readonly = True)

        dpg.bind_item_theme('homeCredit_settings',btnHovered_theme(colorHov=(104, 102, 97)))
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
        six_months_db = initial_val_db(Settings_Model,category='hc_interest',tag= 'six_interest_val', value= '6')
        nine_months_db = initial_val_db(Settings_Model,category='hc_interest',tag= 'nine_interest_val', value= '8')
        twelveAbove_months_db = initial_val_db(Settings_Model,category='hc_interest',tag= 'twelve_above_interest_val', value= '13')

        six_months = int(six_months_db)/100
        nine_months = int(nine_months_db)/100
        twelve_above_months = int(twelveAbove_months_db)/100

        print(value)
        print(six_months)
        print(nine_months)
        print(twelve_above_months)

        six_total = math.ceil(value + (value*six_months))
        nine_total = math.ceil(value + (value*nine_months))
        twelve_above_total = math.ceil(value + (value*twelve_above_months))

        dpg.set_value(f'six_months_calHomecredit',add_comma(six_total))
        dpg.set_value(f'nine_months_calHomecredit',add_comma(nine_total))
        dpg.set_value(f'twelve_above_months_calHomecredit',add_comma(twelve_above_total))

    def settings(self,sender,app_data, user_data):
        dpg.set_value(f'initial_calHomecredit','')
        dpg.set_value(f'six_months_calHomecredit','')
        dpg.set_value(f'nine_months_calHomecredit','')
        dpg.set_value(f'twelve_above_months_calHomecredit','')
        try:
            dpg.delete_item('homecredit_setting_window')
        except:pass
        with dpg.window(label = 'Settings',tag = 'homecredit_setting_window', height = 550, width = 550, no_scroll_with_mouse = True, no_scrollbar = True, no_collapse = True, no_move = True, on_close = dpg.delete_item('homecredit_setting_window')):
            six = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'six_interest_val')).first()
            nine = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'nine_interest_val')).first()
            twelve_above = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'twelve_above_interest_val')).first()

            
            with dpg.group(horizontal = True):
                with dpg.group():
                    dpg.add_text(default_value = '6 months % ')
                    dpg.add_text(default_value = '9 months % ')
                    dpg.add_text(default_value = '12 above months % ')
                with dpg.group(tag = 'hc_settings_input'):
                    dpg.add_input_text(tag ='six_input' ,default_value = six.value, width = 50, user_data = 'six_interest_val',callback  = lambda s,a,u:self.change_interest(s,a,u))
                    dpg.add_input_text(tag ='nine_input',default_value = nine.value,width = 50, user_data = 'nine_interest_val',callback  = lambda s,a,u:self.change_interest(s,a,u))
                    dpg.add_input_text(tag ='twelve_above_input',default_value = twelve_above.value,width = 50, user_data = 'twelve_above_interest_val',callback  = lambda s,a,u:self.change_interest(s,a,u))

        dpg.bind_item_theme('hc_settings_input','corner_radius')

    def change_interest(self,sender,app_data,user_data):
        db = session.scalars(select(Settings_Model).where(Settings_Model.tag == user_data)).first()
        db.value = app_data
        session.commit()
       
