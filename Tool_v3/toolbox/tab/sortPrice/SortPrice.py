
import dearpygui.dearpygui as dpg
import pandas as pd
from pynput.keyboard import Key, Controller
from toolbox.utilities.helper import add_comma
from toolbox.utilities.colorstyles import btnHovered_theme
from toolbox.models import Settings_Model
from sqlalchemy import select
from toolbox import session

class SortPrice:
    def __init__(self):
        self.keyboard = Controller()
        self.disabled_branch = []
        self.temp_df = None

        with dpg.theme() as self.table_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(0,0,0,0))
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,(33, 17, 247))
        
        with dpg.theme() as self.header_col:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding,10,10)
        
        self.conversionText = {
        'Item ID':'Item_ID',
        'Item Name':'Item_Name',
        'Total_Qty':'T_Qty',
        'Total_Retail Price':'Retail_Price',
        'Total_Price 4':'Price_4',
        'DAVAO GMALL_Qty':'Gmall_Qty',
        'Joyo Davao SM LANANG_Qty':'SML_Qty',
        'Maxsun Gempesaw Davao_Qty':'Main_Qty',
        'Joyo SM ECOLAND_Qty':'SME_Qty',
        'Davao Lanang Warehouse_Qty':'Warehouse_Qty'
        } 


        self.converDtypes = {
            'Item_ID':'category',
            'Item_Name':'category',
            'T_Qty':'int16',
            'Retail_Price':'category',
            'Price_4':'category',
            'Gmall_Qty':'int16',
            'SML_Qty':'int16',
            'Main_Qty':'int16',
            'SME_Qty':'int16',
            'Warehouse_Qty':'int16'
        }

        self.table_col_width= {
            'Item_ID':120,
            'Item_Name':400,
            'T_Qty':30,
            'Retail_Price':50,
            'Price_4':50,
            'Gmall_Qty':30,
            'SML_Qty':30,
            'Main_Qty':30,
            'SME_Qty':30,
            'Warehouse_Qty':30
        }

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Left, callback=lambda s,a,u:self.up(s,a,u))
            dpg.add_key_press_handler(dpg.mvKey_Right, callback=lambda s,a,u:self.down(s,a,u))

        try:
            self.df = pd.read_feather('sort.feather')
            self.temp_df = self.df
         
        except:
            self.df = None

        path = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'pick_sort_default_path')).first()
  
        default_dir = path.value if path is not None else '/'
        
        try:
            with dpg.file_dialog(directory_selector=False,default_path = default_dir, show=False, id="pick_data",tag = 'pick_data', width=700 ,height=400, callback = lambda s,a,u:self.extract_data(s,a,u)):
                dpg.add_file_extension(".xlsx")
        except:
            with dpg.file_dialog(directory_selector=False, show=False, id="pick_data",tag = 'pick_data', width=700 ,height=400, callback = lambda s,a,u:self.extract_data(s,a,u)):
                dpg.add_file_extension(".xlsx")

    

        dpg.add_file_dialog(directory_selector=True, show=False, callback=lambda s,a,u:self.default_folder(s,a,u), tag="pick__default_folder",width=700 ,height=400)

        dpg.add_spacer(height = 10)
        with dpg.group():
            with dpg.group(horizontal = True, tag = 'head_tag'): #Item_ID,Item_Name
                dpg.add_combo(tag = 'category_filter',items =['Item_ID', 'Item_Name'], width = 100, default_value = 'Item_ID')
                dpg.add_input_text(tag = 'search_bar', width = 300, callback = lambda s,a,u:self.search_bar(s,a,u))
                dpg.add_image_button(texture_tag='pick_folder_img', tag = 'pick_file', callback = lambda: dpg.show_item('pick_data'))
                dpg.add_image_button(texture_tag='settings_small_img', tag = 'settings_sort', callback = lambda s,a,u:self.settings(s,a,u))

                with dpg.group(horizontal = True, tag = 'check_box', parent = 'head_tag'):
                    if self.df is not None:
                        self.checkboxes(self.df.columns.to_list()[5:])
                    else:
                        pass
            dpg.bind_item_theme('search_bar','corner_radius')
            dpg.bind_item_theme('pick_file',btnHovered_theme(colorHov=(122, 154, 247)))
            dpg.bind_item_theme('settings_sort',btnHovered_theme(colorHov=(244, 122, 122)))
            dpg.bind_item_font('head_tag', 'small')
            dpg.bind_item_font('category_filter', 'combo_font')

            dpg.add_spacer(height =5)
            
            with dpg.group(tag = 'items_container'):
                with dpg.table(tag = 'item_table',clipper = True,parent  = 'items_container',width=1000,height=500,row_background=True,scrollY = True,resizable = True, header_row = True,freeze_rows = 1):
                    if self.df is not None:
                        self.show_items(self.df)
                    else:
                        pass
                dpg.bind_item_theme('item_table',self.table_theme)
                dpg.bind_item_font('item_table','small_x')
        
        dpg.bind_font('small')
    

    def default_folder(self,sender,app_data,user_data):
        path = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'pick_sort_default_path')).first()
        if path is None:
            add_path = Settings_Model(
                category = 'path',
                tag = 'pick_sort_default_path',
                value = app_data['file_path_name']
            )
            print('add succussfully...')
            session.add(add_path)
            
        else:
            path.value = app_data['file_path_name']
            print('updated succussfully...')
        session.commit()

        dpg.set_value('default_sort_path', app_data['file_path_name'])
        dpg.configure_item('pick_data',default_path = app_data['file_path_name'])
        dpg.delete_item('sort_setting_window')


    def settings(self,sender,app_data,user_data):
        path = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'pick_sort_default_path')).first()
        with dpg.window(label = 'Settings',tag = 'sort_setting_window', height = 550, width = 550, no_scroll_with_mouse = True, no_scrollbar = True, no_collapse = True, no_move = True, on_close = dpg.delete_item('sort_setting_window')):
            with dpg.group(horizontal = True):
                dpg.add_text(default_value = 'Default path')
                dpg.add_image_button(texture_tag='pick_folder_img', tag = 'pick_sort_default_path', callback = lambda: dpg.show_item('pick__default_folder'))
                dpg.add_input_text(tag = 'default_sort_path', width = 250, readonly = True)

        if path is not None:
            dpg.set_value('default_sort_path',path.value)

        dpg.bind_item_theme('pick_sort_default_path',btnHovered_theme(colorHov=(122, 154, 247)))
        dpg.bind_item_theme('default_sort_path','corner_radius')



    def search_bar(self,sender,app_data,user_data):
        category_combo = dpg.get_value('category_filter')

        search_df = self.temp_df.loc[self.temp_df[category_combo].str.contains(app_data,case = False)]
        search_df = search_df.reset_index(drop = True)
    

        self.show_items(search_df)

    def extract_data(self,sender,app_data,user_data):
        available_cols_rename = {}
        file_path = app_data['file_path_name']
        self.df= pd.read_excel(file_path,skiprows=3,skipfooter=1).fillna(0)
        if 'Total_Price 4' in self.df.columns.to_list():
            if 'Total_Retail Price' not in self.df.columns.to_list():
                self.df['Total_Retail Price'] = self.df['Total_Price 4'].add(self.df['Total_Price 4'].mul(10/100)).round().astype(int)

                column_to_move = self.df.pop('Total_Retail Price')
                self.df.insert(4, 'Total_Retail Price', column_to_move)

            for column in self.df.columns.to_list():
                if column in self.conversionText:
                    available_cols_rename.update({column:self.conversionText[column]})
            
            self.df['Total_Retail Price'] = self.df['Total_Retail Price'].apply(lambda x: f'{x:,}')
            self.df['Total_Price 4'] = self.df['Total_Price 4'].apply(lambda x: f'{x:,}')

            self.df = self.df[available_cols_rename.keys()].rename(columns=available_cols_rename, errors = 'raise')


            for column in self.df.columns.to_list():
                self.df[column] = self.df[column].astype(self.converDtypes[column])
            


            self.df.to_feather('sort.feather')
            self.checkboxes(self.df.columns.to_list()[5:])

          
            self.show_items(self.df)
            self.disabled_branch = []

        else:
            print('Error Occurs')

    def checkboxes(self, columns = list[str]):
        dpg.delete_item('check_box')
        with dpg.group(horizontal = True, tag = 'check_box', parent = 'head_tag'):
            dpg.add_checkbox(label = 'Zero', tag = 'zero', user_data = 'zero',callback = lambda s,a,u:self.checkbox_clicked(s,a,u))
            for column in columns:
                #column = column.remove('_Qty')
                dpg.add_checkbox(label = column.replace('_Qty',''),tag = column,default_value = True, user_data = column, callback = lambda s,a,u:self.checkbox_clicked(s,a,u))

    def checkbox_clicked(self,sender,app_data,user_data):
        zero_check_val = dpg.get_value('zero')
        category_combo = dpg.get_value('category_filter')
        search_bar = dpg.get_value('search_bar')
        
        if user_data != 'zero':
            if app_data == False:
                self.disabled_branch.append(user_data)
            else:
                self.disabled_branch.remove(user_data)


        self.temp_df = self.df.drop(columns=self.disabled_branch)
        self.temp_df['T_Qty']= self.temp_df.iloc[:,5:].sum(axis = 1)

        if zero_check_val:
            zeros = self.temp_df.query('T_Qty == 0.0 or T_Qty == 0').index.tolist()
            self.temp_df = self.temp_df.drop(index=zeros)

        
        search_df = self.temp_df.loc[self.temp_df[category_combo].str.contains(search_bar,case = False)]
        search_df = search_df.reset_index(drop = True)
    
        self.show_items(search_df)

    def show_items(self,df):
        # pass
     
        zeros = df.query('T_Qty == 0.0 or T_Qty == 0').index.tolist()
        
        
        dpg.delete_item('item_table',children_only = True)

        for column in df.columns.to_list():
            dpg.add_table_column(label = column, init_width_or_weight = self.table_col_width[column],parent = 'item_table')
        
        for row_item in df.values.tolist():
            with dpg.table_row(parent = 'item_table'):
                for column_item in row_item:
                    dpg.add_input_text(default_value=column_item, readonly = True, width = 1000, auto_select_all = True)
    
        for zero in zeros:
            dpg.highlight_table_row('item_table', zero, [255, 0, 0])

    def up(self,sender,app_data,user_data):
        with self.keyboard.pressed(Key.shift):
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)

    def down(self,sender,app_data,user_data):
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
