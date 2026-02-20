import dearpygui.dearpygui as dpg
from toolbox.customWidget.DatePicker import DatePicker
from .autoComplete import AutoComplete
import pandas as pd
from toolbox.models import QoutationItem
from  toolbox import session
from toolbox.utilities.helper import add_comma,initial_val_db
from toolbox.utilities.colorstyles import btnHovered_theme
from toolbox.models import Settings_Model


class Qoutation:
    def __init__(self):
        self.INPUT_WIDTH = 370

        initial_val_db(model=Settings_Model,category='qoutation_proposed_price',tag='qoutation_price_option',value='Price_4')
        
        with dpg.group():
            with dpg.group():
                self.header_navigation()
                dpg.add_spacer(height = 40)
                self.personal_widgets()
                dpg.add_spacer(height = 10)
                self.items_widgets()



    def header_navigation(self):
        with dpg.group(horizontal = True, pos = [920,35]):
            dpg.add_image_button(texture_tag = 'show_img', tag = 'show_qoutation_records')
            dpg.add_image_button(texture_tag = 'settings_img', tag = 'settings_qoutation', callback = lambda s,a,u: self.settings_qoutation(s,a,u))

        dpg.bind_item_theme('show_qoutation_records', btnHovered_theme(colorHov = (122, 154, 247)))
        dpg.bind_item_theme('settings_qoutation', btnHovered_theme(colorHov=(104, 102, 97)))


    def settings_qoutation(self,sender,app_data,user_data):
        radio_prosposed = session.query(Settings_Model).where(Settings_Model.tag == 'qoutation_price_option').first()
        options = ['Price_4','Retail_Price','1% interest','6% interest']
        with dpg.window(label = 'Settings',tag = 'qoutation_setting_window', height = 550, width = 550, no_scroll_with_mouse = True, no_scrollbar = True, no_collapse = True, no_move = True, on_close = dpg.delete_item('qoutation_setting_window')):
            dpg.add_radio_button(tag = 'qoutation_price_option',items = options, default_value = radio_prosposed.value, callback = lambda s,a,u:self.radio_pick_proposed_price(s,a,u))

    def radio_pick_proposed_price(self,sender,app_data,user_data):
        radio_prosposed = session.query(Settings_Model).where(Settings_Model.tag == sender).first()

        radio_prosposed.value = app_data
        session.commit()

        dpg.configure_item(sender,default_value = app_data)

    def personal_widgets(self):
        with dpg.group(horizontal = True) as personal_container:
            with dpg.group(horizontal = True):

                with dpg.group() as lbl_1:
                    dpg.add_text(default_value = "Date")
                    dpg.add_text(default_value = "Customer's Name")
                   
                with dpg.group() as input_1:
                    DatePicker(tag='qoute_date', theme= 'date_theme', input_width=self.INPUT_WIDTH)
                    dpg.add_input_text(width =self.INPUT_WIDTH)
                   
            with dpg.group(horizontal = True):
                with dpg.group() as lbl_2:
                    dpg.add_text(default_value = "Phone Number")
                    dpg.add_text(default_value = "Prepared By")

                with dpg.group() as input_2:
                    dpg.add_input_text(width =self.INPUT_WIDTH)
                    dpg.add_input_text(width =self.INPUT_WIDTH)


        dpg.bind_item_font(input_1,'small')
        dpg.bind_item_font(lbl_1,'small_bold')
        dpg.bind_item_font(input_2,'small')
        dpg.bind_item_font(lbl_2,'small_bold')
        dpg.bind_item_theme(personal_container,'corner_padding')

    def items_widgets(self):
        search_filter = ['Item_ID', 'Item_Name']
        with dpg.group():
            with dpg.group(horizontal = True):
                dpg.add_combo(tag = 'qoute_filter_search',default_value = search_filter[0],items = search_filter, width = 127)
                dpg.add_input_text(tag = 'qoutation_search_input',hint = 'Search...', width = 829, callback = lambda s,a,u:self.autoComplete(s,a,u))
                dpg.add_image_button(texture_tag= 'add_small_img',tag = 'add_item_qoutation',show = False,callback = lambda s,a,u:self.add_item_qoutation(s,a,u))

            dpg.add_spacer(height = 5)
            with dpg.group(tag = 'item_qoutation_container'):
                with dpg.group(horizontal = True) as head:
                    dpg.add_spacer(width = 5)
                    dpg.add_text(default_value = 'Category', color  =(37, 150, 190))
                    dpg.add_spacer(width = 37)
                    dpg.add_text(default_value = 'Quantity', color  =(37, 150, 190))
                    dpg.add_spacer(width = 14)
                    dpg.add_text(default_value = 'Item ID', color  =(37, 150, 190))
                    dpg.add_spacer(width =  75)
                    dpg.add_text(default_value = 'Description', color  =(37, 150, 190))
                    dpg.add_spacer(width = 330)
                    dpg.add_text(default_value = 'Price', color  =(37, 150, 190))
                    dpg.add_spacer(width = 25)
                    dpg.add_text(default_value = 'Total Price', color  =(37, 150, 190))

                with dpg.child_window(tag = 'add_items_container', height = 400):
                    pass
            
                with dpg.group(horizontal = True):
                    dpg.add_button(label = 'Save')
                    dpg.add_input_text(tag = 'all_total_qoutation', default_value = 0)

        dpg.bind_item_font(head, 'small_bold')

        
                
        
        dpg.bind_item_theme('qoutation_search_input', 'corner_padding')
        dpg.bind_item_theme('add_item_qoutation',btnHovered_theme(colorHov = (122, 154, 247)))
    def autoComplete(self,sender,app_data,user_data):
        df = pd.read_feather('sort.feather')
        x,y = tuple(dpg.get_item_pos(sender))
        category_combo = dpg.get_value('qoute_filter_search')

        search_df = df.loc[df[category_combo].str.contains(app_data,case = False)]

        AutoComplete(pos=[x,y+20], data_frame= search_df)

    def add_item_qoutation(self,sender,app_data,user_data):

        extract_db = session.query(QoutationItem).where(QoutationItem.name == user_data).first()
        QouteRows(
            item_id = extract_db.name,
            description = extract_db.description,
            price = extract_db.price_four

        )

        dpg.set_value('qoutation_search_input','')
        dpg.configure_item(sender , show = False)



    
            
class QouteRows:
    instances = []
    total = 0
    def __init__(self,item_id,description,price):
        self.price = price
        self.prev_total_price = float(str(self.price).replace(',',''))
        
        category_list = ['CPU','MB','RAM','SSD','PSU','CASE','VC','MON','CASE FAN','CPU FAN','AIO','KBM','MOU','UPS','AVR','PRN']
        self.class_len = len(QouteRows.instances)
        with dpg.group(tag = f'qoute_item_{self.class_len}',horizontal = True , parent = 'add_items_container') as rows:
            dpg.add_combo(tag = f'qoute_category_{self.class_len}',default_value = category_list[0],items = category_list, width = 110, height_mode = 200)
            dpg.add_input_int(tag = f'quote_qty_{self.class_len}', width = 80, min_value = 0,default_value = 1, min_clamped = True , callback = lambda s,a,u:self.change_qty(s,a,u))
            dpg.add_input_text(tag = f'qoute_item_id_{self.class_len}',readonly = True,default_value = item_id,hint = 'Item Code', width = 135)
            dpg.add_input_text(tag = f'qoute_description_{self.class_len}',readonly = True,default_value = description,hint = 'Description', width = 419)
            dpg.add_input_text(tag = f'qoute_price_{self.class_len}',readonly = True,default_value = price,hint = 'Price', width = 70)
            dpg.add_input_text(tag = f'qoute_tPrice_{self.class_len}' ,readonly = True,default_value = price,hint = 'Total Price', width = 100)
            dpg.add_image_button(tag = f'qoute_delete_{self.class_len}',texture_tag = 'delete_small_img', callback = lambda s,a,u:self.delete_row(s,a,u) )

        QouteRows.total += float(str(self.price).replace(',',''))
        dpg.set_value('all_total_qoutation',QouteRows.total)

        dpg.bind_item_theme(f'qoute_delete_{self.class_len}' , btnHovered_theme(colorHov=(244, 122, 122)))
        dpg.bind_item_theme(rows , 'corner_padding')
        dpg.bind_item_font(rows,'small')

        QouteRows.instances.append(self)
    
    def change_qty(self,sender,app_data,user_data):
        new_total_price = float(str(self.price).replace(',','')) * app_data
        dpg.set_value(f'qoute_tPrice_{self.class_len}', add_comma(new_total_price))

        QouteRows.total-= self.prev_total_price
        QouteRows.total += new_total_price
        self.prev_total_price = new_total_price
        dpg.set_value('all_total_qoutation',QouteRows.total)

    def delete_row(self,sender,app_data,user_data):
        dpg.delete_item(f'qoute_item_{self.class_len}')
        QouteRows.total-= self.prev_total_price
        dpg.set_value('all_total_qoutation',QouteRows.total)









        


