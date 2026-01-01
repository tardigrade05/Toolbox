import dearpygui.dearpygui as dpg
from toolbox.models import AtdTables_Model
from toolbox import session
from sqlalchemy import select
from toolbox.utilities.helper import add_comma,deal_with_decimal,realtime
from toolbox.utilities.colorstyles import btnHovered_theme

class TableTab:
    def __init__(self,tag:str, unique:str,themes:list = None):
        
        self.tag = tag
        self.category = f"{tag}_{unique}"
        self.category_input = f'{self.category}_inputVal'
        self.category_table = f'{self.category}_table'
        self.main_container = f'{self.category}_main_container'
        self.selected = []
        
        with dpg.group(tag = self.main_container):
            dpg.add_spacer(height = 10)
    
            with dpg.group(horizontal = True):
                dpg.add_input_text(tag = self.category_input, hint = 'Type here...', width = 130,height = 30,decimal = True,callback= lambda s,a,u:self.add_value(s,a,u),on_enter = True)
    
                dpg.add_image_button(texture_tag = 'add_img',label = 'Add', tag = f'{self.category}_add', callback = lambda s,a,u:self.add_value(s,a,u))
                dpg.add_image_button(texture_tag = 'delete_all_img', label = 'Delete All', tag = f'{self.category}_deleteAll', callback = lambda s,a,u:self.delete_all(s,a,u))
                dpg.add_image_button(texture_tag = 'edit_img', label = 'Edit',show = False, tag = f'{self.category}_edit', callback = lambda s,a,u:self.edit_value(s,a,u))
                dpg.add_image_button(texture_tag = 'delete_img', label = 'Delete',show = False, tag = f'{self.category}_delete', callback = lambda s,a,u:self.delete_value(s,a,u))
                dpg.add_image_button(texture_tag = 'default_img', label = 'Default',show= False, tag = f'{self.category}_default', callback = lambda s,a,u:self.default_btn(s,a,u))
                dpg.add_spacer(height = 40)

                self.show_values()

        dpg.bind_item_theme(self.category_input, themes[3])
        dpg.bind_item_theme(f'{self.category}_add', themes[1]) #
        dpg.bind_item_theme(f'{self.category}_deleteAll',themes[0] )
        dpg.bind_item_theme(f'{self.category}_edit', themes[1])
        dpg.bind_item_theme(f'{self.category}_delete', themes[0])
        dpg.bind_item_theme(f'{self.category}_default', themes[2])

        dpg.bind_item_font(self.category_input,'medium_y')

    def add_value(self,sender,app_data,user_data):
        new_value = deal_with_decimal(float(dpg.get_value(self.category_input)))
        add_value = AtdTables_Model(
            category = self.category,
            value = str(new_value)
        )
        session.add(add_value)
        session.commit()

        self.show_values()

        dpg.set_value(self.category_input,'')
        self.selected = []
        dpg.focus_item(self.category_input)

    def show_values(self):
        try:
            category_values = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == self.category)).all()
        except:
            category_values = []

        dpg.delete_item(self.category_table)
        with dpg.table(tag = self.category_table,parent  = self.main_container,row_background=True, header_row=False,height=485,scrollY = True):
            dpg.add_table_column(label = '')
        
            for value in category_values:
                with dpg.table_row():
                    dpg.add_selectable(label = add_comma(int(value.value)/1000), tag = f'{value.category}_{value.id}', callback = lambda s,a,u:self.select_item(s,a,u), user_data = (value.id,value.value))
                    dpg.bind_item_font(f'{value.category}_{value.id}','medium_y')

        realtime()
    def delete_all(self,sender,app_data,user_data):
        session.query(AtdTables_Model).filter(AtdTables_Model.category == self.category).delete()
        session.commit()
        self.show_values()
        self.selected = []

    def delete_value(self,sender,app_data,user_data):
        for id,_ in self.selected:
            session.query(AtdTables_Model).filter(AtdTables_Model.id == id).delete()
        
        session.commit()
        self.selected = []
        dpg.set_value(self.category_input,'')
        self.show_values()
        self.default_btn()

    def edit_value(self,sender,app_data,user_data):
        updated_value = deal_with_decimal(float(dpg.get_value(self.category_input)))
        target_row = session.scalars(select(AtdTables_Model).filter(AtdTables_Model.id == self.selected[-1][0])).first()
        target_row.value = str(updated_value)

        session.commit()
        self.selected = []

        self.show_values()
        self.default_btn()
    
    def default_btn(self):
        self.hidden_btn(add=True,delete_all=True,edit=False,delete=False,default=False)
        for id,_ in self.selected:
            dpg.configure_item(item = f"{self.category}_{id}", default_value = False)
        self.selected = []
        dpg.set_value(self.category_input,'')

    def hidden_btn(self, add:bool,delete_all:bool,edit:bool,delete:bool,default:bool) -> None:
        dpg.configure_item(f'{self.category}_add' , show = add)
        dpg.configure_item(f'{self.category}_deleteAll', show = delete_all)
        dpg.configure_item(f'{self.category}_edit', show = edit)
        dpg.configure_item(f'{self.category}_delete', show = delete)
        dpg.configure_item(f'{self.category}_default', show = delete)

    def select_item(self,sender,app_data,user_data):
        
        if user_data in self.selected:
            self.selected.remove(user_data)
        else:
            self.selected.append(user_data)

        dpg.set_value(self.category_input,add_comma(int(user_data[1])/1000).replace(',',''))
        self.hidden_btn(add=False,delete_all=False,edit=True,delete=True,default = True)
        if len(self.selected) == 0:
            self.default_btn()
    
    def initial_setup(self):
        exist_df = DataFrame().get_exist_df(self.tag)
        all_counter,self.counter, self.values = DataFrame().get_counter_values(exist_df,self.tag)
        self.show_values(all_counter,self.values)

        self.hidden_btn(add=True,delete_all=True,edit=False,delete=False)
        self.selected = []
        dpg.set_value(self.input,'')

class AtdTables:
    def __init__(self):
        red_theme = btnHovered_theme(colorHov = (244, 122, 122))
        blue_theme = btnHovered_theme(colorHov = (122, 154, 247))
        green_theme = btnHovered_theme(colorHov = (5, 245, 85))

        with dpg.tab_bar():
            with dpg.tab(label="Card"):
                TableTab('card','atd_tables', themes=[red_theme,blue_theme,green_theme,'corner_radius'])

            with dpg.tab(label="Homecredit"):
                TableTab('homeCredit','atd_tables', themes=[red_theme,blue_theme,green_theme,'corner_radius'])

            with dpg.tab(label="Billease"):
                TableTab('billease','atd_tables', themes=[red_theme,blue_theme,green_theme,'corner_radius'])

            with dpg.tab(label="Form 2307"):
                TableTab('form','atd_tables', themes=[red_theme,blue_theme,green_theme,'corner_radius'])
                
            with dpg.tab(label="Bank Transfer"):
                TableTab('bankTrans','atd_tables', themes=[red_theme,blue_theme,green_theme,'corner_radius'])

            with dpg.tab(label="Expenses"):
                TableTab('expenses','atd_tables', themes=[red_theme,blue_theme,green_theme,'corner_radius'])
