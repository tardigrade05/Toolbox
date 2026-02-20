import dearpygui.dearpygui as dpg
from toolbox.customWidget.DatePicker import DatePicker
from toolbox.utilities.colorstyles import btnHovered_theme
from toolbox.utilities.helper import generate_jobOrder, generate_refNumber
from toolbox import session
from sqlalchemy import select
from toolbox.models import Personal,Item,Settings_Model
from . import settings, show_records


from datetime import date
import math
import datetime


class JoRma:
    def __init__(self):
        self.input_indent = 110
        self.input_width = 140
        self.personal_title = [
            'Branch','Date','Job Order #','Reference #',
            'DR #','Warranty Start','Warranty End','Warranty Remaining',
            'Contact #','Customer Name','Technician Name'

        ]
        self.personal = ['joRma_drNum','joRma_contactNum','joRma_customerName','joRma_techName']

        self.bool_dict = {'1':True,'0':False}
        self.jo = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'jo_order_checkbox')).first()
        self.rma = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'reference_checkbox')).first()

        if self.jo is None:
            self.jo = Settings_Model(category = 'jor_ma', tag = 'jo_order_checkbox',value = True)
            session.add(self.jo)

        if self.rma is None:
            self.rma = Settings_Model(category = 'jor_ma', tag = 'reference_checkbox',value = True)
            session.add(self.rma)
        
        session.commit()

        with dpg.group(tag='main'):
            with dpg.child_window(label="", width=-1, height=168, border=True):
                with dpg.group(horizontal=True):
                    dpg.add_text("Personal Details", tag= 'personal_title')

                    dpg.add_image_button(texture_tag='add_img', tag = 'add_joRma', callback = self.add)
                    dpg.add_image_button(texture_tag='delete_img', tag = 'delete_joRma', callback = self.delete)

                    dpg.add_spacer(width = 20)
                    dpg.add_image_button(texture_tag='show_img', tag = 'show_joRma', callback = self.show_records)
                    dpg.add_image_button(texture_tag='settings_img', tag = 'settings_joRma', callback = self.settings)

                dpg.add_spacer(height = 5)
                with dpg.group():
                    with dpg.group(horizontal=True):
                        self.titles_lbl(titles=['Branch','Date','Job Order #','Reference #'],font='small_bold', theme= 'corner_padding')

                        with dpg.group(tag= 'personal_col_1'):
                            dpg.add_combo(tag='branch', items=['GMALL','SME','SML','MAIN'],default_value='GMALL', width = self.input_width, callback= generate_jobOrder)
                            DatePicker(tag='joRma_date', theme= 'date_theme', input_width= self.input_width,function_call=generate_jobOrder)
                            dpg.add_input_text(tag= 'joRma_jobOrder', width = self.input_width, readonly=self.bool_dict[self.jo.value])
                            dpg.add_input_text(tag= 'joRma_refNum', width = self.input_width, readonly=self.bool_dict[self.rma.value])
                        
                        self.titles_lbl(titles=['DR #','Warranty Start','Warranty End','Warranty Remaining'],font='small_bold', theme= 'corner_padding')

                        with dpg.group(tag= 'personal_col_2'):
                            dpg.add_input_text(tag= 'joRma_drNum', width = self.input_width)
                            DatePicker(tag='joRma_warrantyStart', theme= 'date_theme', input_width= self.input_width)
                            DatePicker(tag='joRma_warrantyEnd', theme= 'date_theme', input_width= self.input_width, function_call= self.generate_remainingDays)
                            dpg.add_input_text(tag= 'joRma_warrantyRemain', width = self.input_width, readonly= True)

                        self.titles_lbl(titles=['Contact #','Customer Name','Technician Name'],font='small_bold', theme= 'corner_padding')

                        with dpg.group(tag= 'personal_col_3'):
                            dpg.add_input_text(tag= 'joRma_contactNum', width = self.input_width)
                            dpg.add_input_text(tag= 'joRma_customerName', width = self.input_width*2)
                            dpg.add_input_text(tag= 'joRma_techName', width = self.input_width*2)

            with dpg.child_window(tag = 'Item',label="", width=-1,resizable_y=True,height=350, border=True):
                pass
        
        
        dpg.add_button(label='Generate Copy', width= 986, height= 40, callback= self.generate_copy)

        generate_jobOrder()
        generate_refNumber()
        self.generate_remainingDays()

        dpg.bind_item_theme('personal_col_1','corner_padding')
        dpg.bind_item_theme('personal_col_2','corner_padding')
        dpg.bind_item_theme('personal_col_3','corner_padding')

        dpg.bind_item_theme('add_joRma',btnHovered_theme(colorHov=(122, 154, 247)))
        dpg.bind_item_theme('delete_joRma',btnHovered_theme(colorHov=(244, 122, 122)))
        dpg.bind_item_theme('show_joRma',btnHovered_theme(colorHov=(122, 154, 247)))
        dpg.bind_item_theme('settings_joRma',btnHovered_theme(colorHov=(104, 102, 97)))

        dpg.bind_item_font('personal_title','medium_y_bold')
        dpg.bind_item_font('personal_col_1','small')
        dpg.bind_item_font('personal_col_2','small')
        dpg.bind_item_font('personal_col_3','small')

    def generate_copy(self):
        if self.validate_fillIn():

            person = Personal(
                branch = str(dpg.get_value('branch')).strip(),
                date = str(dpg.get_value('joRma_date_input')).strip(),
                job_order = str(dpg.get_value('joRma_jobOrder')).strip(),
                reference = str(dpg.get_value('joRma_refNum')).strip(),
                dr_number = str(dpg.get_value('joRma_drNum')).strip(),
                
                warranty_start = str(dpg.get_value('joRma_warrantyStart_input')).strip(),
                warranty_end = str(dpg.get_value('joRma_warrantyEnd_input')).strip(),
                remaining = str(dpg.get_value('joRma_warrantyRemain')).strip(),
                contact_number = str(dpg.get_value('joRma_contactNum')).strip(),
                customer_name = str(dpg.get_value('joRma_customerName')).strip(),
                
                tech_name = str(dpg.get_value('joRma_techName')).strip()

            )

            # print(len(Item_Details.instances) , 'generate copy length')
           
            for instance in Item_Details.instances:
                new_item = Item(
                    name  = str(dpg.get_value(instance.name)).strip(),
                    description  = str(dpg.get_value(instance.description)).strip(),
                    serial  = str(dpg.get_value(instance.serial)).strip(),
                    customer_issues  = str(dpg.get_value(instance.customer_issues)).strip(),
                    tech_finding  = str(dpg.get_value(instance.tech_finding)).strip()

                )
                person.items.append(new_item)
            session.add(person)
            session.commit()
            print("Add Successfully")

            for index in range(len(Item_Widget.instances)):
                dpg.delete_item(f'Item_{index}')
            Item_Widget.instances.clear()
            Item_Details.instances.clear()
            generate_jobOrder()
            generate_refNumber()
            # self.generate_remainingDays()

            for detail in self.personal:
                dpg.set_value(detail,'')
            
            dpg.set_value('joRma_warrantyRemain','0')

    def titles_lbl(self,titles:list[str],font,theme):
        with dpg.group() as container:
            for item in titles:
                dpg.add_text(default_value=item)
        
        dpg.bind_item_font(container,font)
        dpg.bind_item_theme(container,theme)
    
    

    def generate_remainingDays(self) -> None:
        initial_date = str(dpg.get_value('joRma_date_input')).split('/')
        initial_warraty_end_date = str(dpg.get_value('joRma_warrantyEnd_input')).split('/')

        f_date = datetime.date(int(initial_date[2]),int(initial_date[0]),int(initial_date[1]))
        f_warraty_end_date = datetime.date(int(initial_warraty_end_date[2]),int(initial_warraty_end_date[0]),int(initial_warraty_end_date[1]))

        remaining_days = str(f_warraty_end_date - f_date).split(' ')[0]
        if remaining_days == '0:00:00':
            remaining_days = '0'

        dpg.set_value('joRma_warrantyRemain',remaining_days)

    def validate_fillIn(self) -> bool:
        

        if len(Item_Details.instances) >0:
            for detail in self.personal:
                if str(dpg.get_value(detail)).strip() == "":
                    print('fill all boxes')
                    return False
                
            for items in Item_Details.instances:
                for detail in items.get_all_details():
                    if str(dpg.get_value(detail)).strip() == "":
                        print('fill all boxes')
                        return False
        else:
            print('add  atleast 1 item')
            return False

        return True

    def add(self):
        Item_Widget(counter= len(Item_Widget.instances),input_theme='corner_padding', title_show_func = self.titles_lbl)
    
    def delete(self):
        dpg.delete_item(f'Item_{len(Item_Widget.instances)-1}')
        Item_Widget.instances.pop()
        Item_Details.instances.pop()

    def show_records(self):
        show_records.ShowRecords()
       
    def settings(self):
        settings.Settings()

class Item_Details:

    instances = []
    def __init__(
            self,
            name:str,
            description:str,
            serial:str,
            customer_issues:str,
            tech_finding:str):
        
        self.name = name
        self.description = description
        self.serial = serial
        self.customer_issues = customer_issues
        self.tech_finding = tech_finding

        Item_Details.instances.append(self)

    def get_all_details(self) -> list[str]:
        return [self.name,self.description,self.serial,self.customer_issues,self.tech_finding]

             
class Item_Widget:
    instances = []
    def __init__(self,counter, input_theme,title_show_func):
        self.counter = counter
        self.input_indent = 110
        self.input_width = 180
        
        with dpg.group( tag = f'Item_{self.counter}',parent='Item'):
            with dpg.group(horizontal=True):
                dpg.add_text(default_value=f"--Item {self.counter+1} Details--",tag=f'item_title_{self.counter}')

            with dpg.group():
                with dpg.group(horizontal=True):
                    title_show_func(titles=['Item Name','Description','Serial #'],font='small_bold', theme= input_theme)

                    with dpg.group(tag= f'item_col_{self.counter}1'):
                        dpg.add_input_text(tag= f'joRma_itemName_{self.counter}', width = self.input_width*2)
                        dpg.add_input_text(tag= f'joRma_description_{self.counter}', width = self.input_width*2)
                        dpg.add_input_text(tag= f'joRma_serialNum_{self.counter}', width = self.input_width*2)

                    title_show_func(titles=['Customer Issues','Tech Finding'],font='small_bold', theme= input_theme)

                    with dpg.group(tag= f'item_col_{self.counter}2'):
                        dpg.add_input_text(tag= f'joRma_customerIssues_{self.counter}', width = self.input_width*2)
                        dpg.add_input_text(tag= f'joRma_techFinding_{self.counter}', width = self.input_width*2)
                       
        
        dpg.bind_item_theme(f'item_col_{self.counter}1',input_theme)
        dpg.bind_item_theme(f'item_col_{self.counter}2',input_theme)

        dpg.bind_item_font(f'item_title_{self.counter}','medium_y_bold')
        dpg.bind_item_font(f'item_col_{self.counter}1','small')
        dpg.bind_item_font(f'item_col_{self.counter}2','small')   

        Item_Widget.instances.append(self)
     
        Item_Details(
        name= f'joRma_itemName_{self.counter}',
        description= f'joRma_description_{self.counter}',
        serial= f'joRma_serialNum_{self.counter}',
        customer_issues= f'joRma_customerIssues_{self.counter}',
        tech_finding= f'joRma_techFinding_{self.counter}'
        )
