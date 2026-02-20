import dearpygui.dearpygui as dpg
from toolbox.models import Settings_Model
from toolbox import session
from sqlalchemy import select

class Settings:
    def __init__(self):
        self.bool_dict = {'1':True,'0':False}
        self.jo = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'jo_order_checkbox')).first()
        self.rma = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'reference_checkbox')).first()


        with dpg.window(label = 'Settings',tag = 'jorma_setting_window', height = 550, width = 550, no_scroll_with_mouse = True, no_scrollbar = True, no_collapse = True, no_move = True, on_close = dpg.delete_item('jorma_setting_window')):
            dpg.add_checkbox(label= 'JO Order # (readonly) ',tag='jo_order_checkbox',default_value= self.bool_dict[self.jo.value], callback= lambda s,a,u:self.jo_check_cliked(s,a,u))
            dpg.add_checkbox(label= 'Reference # (readonly) ',tag='reference_checkbox',default_value= self.bool_dict[self.rma.value], callback= lambda s,a,u:self.reference_check_cliked(s,a,u))

    def jo_check_cliked(self,sender,app_data,user_data):
   
        self.jo.value = False if not app_data else True
        session.commit()

        dpg.configure_item('joRma_jobOrder', readonly = self.bool_dict[self.jo.value])

    def reference_check_cliked(self,sender,app_data,user_data):
        self.rma.value = False if not app_data else True
        session.commit()

        dpg.configure_item('joRma_refNum', readonly = self.bool_dict[self.rma.value])




