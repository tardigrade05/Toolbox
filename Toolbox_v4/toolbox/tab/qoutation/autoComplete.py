import dearpygui.dearpygui as dpg
from toolbox.tab.sortPrice.SortPrice import SortPrice


class AutoComplete:
    def __init__(self,pos, data_frame):
        self.table_col_width= {
            'Item_ID':0,
            'Item_Name':390,
            'T_Qty':40,
            'Retail_Price':50,
            'Price_4':50,
            'Gmall_Qty':40,
            'SML_Qty':40,
            'Main_Qty':40,
            'SME_Qty':40,
            'Warehouse_Qty':40
        }
    
        try:
            dpg.delete_item('autocomplete_window')
        except:pass
        with dpg.window(pos=pos,tag = 'autocomplete_window',no_focus_on_appearing = True,no_title_bar = True,width=814,height=400):
            dpg.add_button(label = 'close',callback = lambda x:dpg.delete_item('autocomplete_window'))
            
            dpg.add_spacer(height = 20)
            
            with dpg.table(tag = 'autocomplete_table',delay_search = True,clipper = True,width=814,height=400,row_background=True,scrollY = True,resizable = True, header_row = True,freeze_rows = 1):
        
                for column in data_frame.columns.to_list()[1:]:
                    dpg.add_table_column(label = column, init_width_or_weight = self.table_col_width[column], width_fixed = True)
  
                for row_item in data_frame.values.tolist():
                    with dpg.table_row():
                        for column_item in row_item[1:]:
                            dpg.add_selectable(label=column_item,span_columns= True,user_data = (row_item[0],row_item[1]), callback = lambda s,a,u:self.select_item(s,a,u))
            
                # for zero in zeros:

                #     dpg.highlight_table_row('item_table', zero, [255, 0, 0])

    def select_item(self,sender,app_data,user_data):
        
        dpg.configure_item(sender, default_value = False)
        dpg.set_value('qoutation_search_input',user_data[1])
        dpg.configure_item('add_item_qoutation',user_data = user_data[0],show = True) 

        dpg.delete_item('autocomplete_window')