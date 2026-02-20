
import dearpygui.dearpygui as dpg
from datetime import date
import math
import datetime

class DatePicker:
    def __init__(self,tag:str,input_width:int = 100,input_indent:int = 0, theme= None, function_call=None):
        self.function_call = function_call
        current_date = date.today()
        unmerge_date = str(current_date).split('-')
        self.default_date = {
            'month_day': int(unmerge_date[2]),
            'month': int(unmerge_date[1])-1,
            'year': int(unmerge_date[0][1:]) + 100,
        }

        self.input_tag = f'{tag}_input'
        self.btn_tag = f'{tag}_btn' 
       
        date_str = str(current_date).split('-')

        final_date = list(map(self.add_zero,[date_str[1],date_str[2],date_str[0]]))
        default_date = f'{final_date[0]}/{final_date[1]}/{final_date[2]}'
    
        
        with dpg.group(horizontal= True,tag=f'date_picker_{tag}') :
            dpg.add_input_text(indent= input_indent,tag= self.input_tag,default_value=default_date,width=input_width-24.5, readonly= True)
            dpg.add_image_button(texture_tag='calendar_img',background_color = (37, 150, 190),frame_padding = 0, tag=self.btn_tag, callback=self.show_picker)
                
        if theme is not None:
            dpg.bind_item_theme(f'date_picker_{tag}',theme)
        dpg.add_spacer(width=3)

    def add_zero(self , n):
        if type(n) == str:
            n = int(n)

        if n<10:
            return f'0{n}'
        return n
        
        
    def show_picker(self):
        try:
            dpg.delete_item('date_container')
        except:
            pass

        with dpg.window(pos=dpg.get_item_pos(self.input_tag), tag= 'date_container', no_move= True, no_collapse=True):
            dpg.add_date_picker(tag= 'date_picker',default_value= self.default_date, callback= self.picked_date)

    def picked_date(self,sender,app_data,user_data, ):
        month = app_data['month'] + 1
        day = app_data['month_day']
        year = f'{19 + math.floor(app_data['year']/100)}{self.add_zero(app_data['year']%100)}' #  app_data['year'] - 100

        final_date = list(map(self.add_zero,[month,day,year]))
 
        date = f'{final_date[0]}/{final_date[1]}/{final_date[2]}'

        dpg.set_value(self.input_tag,date )

        self.default_date = {
            'month_day': int(final_date[1]),
            'month': int(final_date[0])-1,
            'year': int(str(final_date[2])[1:]) + 100,
        }

        dpg.delete_item('date_container')
      
        if self.function_call is not None:
            self.function_call()
       
