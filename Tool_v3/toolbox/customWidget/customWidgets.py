import dearpygui.dearpygui as dpg
from toolbox.utilities.helper import clean_data,add_comma


class LabelInput:
    def __init__(
        self,
        unique:str,
        label_name:str,
        tag:str,
        input_width:int,
        input_indent:int,
        group_indent:int,
        fonts: list[str],
        input_readonly:bool = True,
        input_decimal:bool = True,
        default_input_val:str = '',
        theme = None

    ):
        self.label_tag = f'{tag}_{unique}_lbl'
        self.input_tag = f'{tag}_{unique}_input'
        
        with dpg.group(horizontal=True, indent=group_indent) as group_labelInput:
            dpg.add_text(default_value = label_name, tag= self.label_tag)
            dpg.add_input_text(tag=self.input_tag,indent=input_indent, width=input_width, decimal=input_decimal,readonly = input_readonly,default_value=default_input_val,auto_select_all = True)

            for tag,font in zip([self.label_tag,self.input_tag],fonts):
                dpg.bind_item_font(tag,font)

        dpg.bind_item_theme(group_labelInput,theme)

class LabelInputLabel:
    def __init__(
        self,
        unique:str,
        label_name:str,
        tag:str,
        input_width:int,
        input_indent:int,
        group_indent:int,
        fonts: list[str],
        input_default_value:str = '',
        input_readonly:bool = True,
        input_decimal:bool = True,
        theme = None

    ):  
        self.label_name = label_name
        self.label_tag = f'{tag}_{unique}_lbl'
        self.input_tag = f'{tag}_{unique}_input'  
        self.label_product_tag = f'{tag}_{unique}_product'
        fonts.append(fonts[0])

        if input_default_value != '':
            product = clean_data(label_name) * clean_data(input_default_value)
            final_product = add_comma(product)
        else:
            final_product = '0'
        
        with dpg.group(horizontal=True, indent=group_indent) as group_labelInputLabel:
            dpg.add_text(default_value = label_name, tag= self.label_tag)
            dpg.add_input_text(tag=self.input_tag,default_value = input_default_value,indent=input_indent, width=input_width, decimal=input_decimal,readonly = input_readonly) #,callback = self.press
            dpg.add_text(default_value = final_product, tag= self.label_product_tag)

            for tag,font in zip([self.label_tag,self.input_tag,self.label_product_tag],fonts):
                dpg.bind_item_font(tag,font)

        dpg.bind_item_theme(group_labelInputLabel,theme)
