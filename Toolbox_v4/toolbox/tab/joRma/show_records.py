import dearpygui.dearpygui as dpg
from toolbox import session
from sqlalchemy import select
from toolbox.models import Personal,Item,Settings_Model
from toolbox.utilities.helper import generate_jobOrder, generate_refNumber, initial_val_db
from .export_excel import insertToExcelRMA, insertToExcelJO
from toolbox.utilities.colorstyles import btnHovered_theme

class ShowRecords:
    def __init__(self):
        self.record_selected = None
        self.tbl_cols = ['Date','Client Name','Contact Number','Description','Serial','Tech Finding','Tech Name','Ref Number','Jo Number']
        with dpg.theme() as self.table_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(0,0,0,0))
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,(33, 17, 247))
        
        initial_val_db(model=Settings_Model,category='path',tag= 'pick_records_default_path',value='/')
        records = session.scalars(select(Personal)).all()

        with dpg.window(label= 'Show Records',tag='record_window', no_collapse= True,width=1000,height=600, no_resize= True, no_move= True, no_scrollbar= True, no_scroll_with_mouse=True, on_close = dpg.delete_item('record_window')): #
            self.header_group()
            self.records_tbl(records= records)

    def select_one(self,sender,app_data,user_data):
        if self.record_selected is None :
            self.record_selected = (sender,user_data)
        elif  self.record_selected is not None and (sender,user_data) != self.record_selected:
            dpg.configure_item(self.record_selected[0], default_value = False)
            self.record_selected = (sender,user_data)
        elif (sender,user_data) == self.record_selected:
            self.record_selected = None

    def records_tbl(self, records):
        
        try:
            dpg.delete_item('record_table')
        except:
            pass
        description = ''
        serial = ''
        tech_finding = ''

       

        #'record_table' #record_table
        with dpg.table(tag = 'record_table',clipper = True,width=1000,height=610,row_background=True,scrollY = True,resizable = True, header_row = True,freeze_rows = 1, parent = 'record_window'):
            dpg.add_table_column(label = 'Date', init_width_or_weight = 50)
            dpg.add_table_column(label = 'Client Name', init_width_or_weight = 50)
            dpg.add_table_column(label = 'Contact Number', init_width_or_weight = 50)
            dpg.add_table_column(label = 'Description', init_width_or_weight = 250)
            dpg.add_table_column(label = 'Serial', init_width_or_weight = 50)
            dpg.add_table_column(label = 'Tech Finding', init_width_or_weight = 50)
            dpg.add_table_column(label = 'Tech Name', init_width_or_weight = 50)
            dpg.add_table_column(label = 'Ref Number', init_width_or_weight = 10)
            dpg.add_table_column(label = 'Jo Number', init_width_or_weight = 50)

            for record in records:
                with dpg.table_row():
                    tag_name = f'{record.id}_{record.dr_number}'
                    dpg.add_selectable(tag = tag_name,label= record.date,height=50, span_columns= True, user_data = record.id,callback= self.select_one)
                    dpg.add_selectable(label= record.customer_name,height=50)
                    dpg.add_selectable(label= record.contact_number,height=50)

                    for item in record.items:
                        description += f'{item.description},\n'
                        serial += f'{item.serial},\n'
                        tech_finding += f'{item.tech_finding},\n'

                    dpg.add_selectable(label= description, height=50)
                    dpg.add_selectable(label= serial, height=50)
                    dpg.add_selectable(label= tech_finding, height=50)
                    dpg.add_selectable(label= record.tech_name, height=50)
                    dpg.add_selectable(label= record.reference, height=50)
                    dpg.add_selectable(label= record.job_order, height=50)
                
                description = ''
                serial = ''
                tech_finding = ''

        dpg.bind_item_theme('record_table',self.table_theme)
        dpg.bind_item_font('record_table','small_x')

    def header_group(self):
        with dpg.group(horizontal = True):
            dpg.add_combo(tag ='jorma_record_filter',default_value = self.tbl_cols[0], items = self.tbl_cols, width = 150)
            
            dpg.add_input_text(tag = 'jorma_record_search', hint = 'Search...',width = 300 , callback = lambda s,a,u:self.search(s,a,u))
            dpg.add_combo(tag ='jorma_record_filter_form',default_value = 'JO', items = ['JO','RMA'], width = 70)
            dpg.add_image_button(texture_tag = 'delete_small_img',tag ='jorma_delete_record', callback = lambda s,a,u:self.delete_jorma_record(s,a,u))
            dpg.add_image_button(texture_tag = 'export_excel_img',tag ='jorma_export_excel_record', callback = lambda s,a,u:self.export_to_excel(s,a,u))
            dpg.add_image_button(texture_tag = 'settings_small_img',tag = 'jorma_record_settings', callback = lambda s,a,u:self.settings(s,a,u))


        dpg.bind_item_theme('jorma_record_search', 'corner_radius')
        dpg.bind_item_theme('jorma_record_settings',btnHovered_theme(colorHov=(104, 102, 97)))
        dpg.bind_item_theme('jorma_delete_record',btnHovered_theme(colorHov=(244, 122, 122)))
        dpg.bind_item_theme('jorma_export_excel_record',btnHovered_theme(colorHov=(5, 245, 85)))

    def export_to_excel(self,sender,app_data,user_data):
        try:
            self.record_selected[1]
        except:
            print('select item first...')
            return

        person = session.query(Personal).filter(Personal.id == self.record_selected[1]).first()
        combo_val = dpg.get_value('jorma_record_filter_form')
        if  combo_val == 'JO':
            insertToExcelJO(person = person)
        elif combo_val == 'RMA':
            insertToExcelRMA(person= person)
        print(person)

    def delete_jorma_record(self, sender, app_data,user_data):
        try:
            self.record_selected[1]
        except:
            print('select item first...')
            return
        
        session.query(Personal).filter(Personal.id == self.record_selected[1]).delete()
        session.commit()
        dpg.delete_item(self.record_selected[0])
        dpg.delete_item('tbl_container')
        records = session.scalars(select(Personal)).all()
        self.records_tbl(records= records)
        generate_jobOrder()
        generate_refNumber()
        
        self.record_selected = None

    def settings(self,sender,app_data,user_data):
        path = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'pick_records_default_path')).first()

        dpg.add_file_dialog(directory_selector=True, show=False, callback=lambda s,a,u:self.default_folder(s,a,u), tag="record_excel_default_folder",width=700 ,height=400, cancel_callback = dpg.delete_item('record_excel_default_folder'))
 
        with dpg.window(label = 'Settings',tag = 'records_setting_window', height = 550, width = 550, no_scroll_with_mouse = True, no_scrollbar = True, no_collapse = True, no_move = True, on_close = dpg.delete_item('records_setting_window')):
            
            with dpg.group(horizontal = True):
                dpg.add_text(default_value = 'Save path')
                dpg.add_image_button(texture_tag='pick_folder_img', tag = 'pick_record_default_path', callback = lambda: dpg.show_item('record_excel_default_folder'))
                dpg.add_input_text(default_value = path.value,tag = 'default_record_path', width = 250, readonly = True)


        dpg.bind_item_theme('pick_record_default_path',btnHovered_theme(colorHov=(122, 154, 247)))
        dpg.bind_item_theme('default_record_path','corner_radius')

    def default_folder(self,sender,app_data,user_data):
        path = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'pick_records_default_path')).first()
        path.value = app_data['file_path_name']

        dpg.set_value('default_record_path', path.value)

        session.commit()

    def search(self,sender,app_data,user_data):
        possible_query = {
            'Date':Personal.date,
            'Client Name':Personal.customer_name,
            'Contact Number':Personal.contact_number,
            'Description':Item.description,
            'Serial':Item.serial,
            'Tech Finding':Item.tech_finding,
            'Tech Name':Personal.tech_name,
            'Ref Number':Personal.reference,
            'Jo Number':Personal.job_order
        }
        filter_category = dpg.get_value('jorma_record_filter')

        if str(app_data).strip(' ') != '':
            if filter_category == 'Description' or filter_category == 'Tech Finding' or filter_category == 'Serial':
                records = session.query(Personal).join(Personal.items).filter(possible_query[filter_category].like(f'%{app_data}%')).all()
            else:
                records = session.query(Personal).filter(possible_query[filter_category].like(f'%{app_data}%')).all()
                
            self.records_tbl(records=records)
        elif str(app_data).strip(' ') == '':
            records = session.scalars(select(Personal)).all()
            self.records_tbl(records=records)

