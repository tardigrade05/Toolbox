import dearpygui.dearpygui as dpg

def changeTextColor_theme(color:tuple[int]):
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text,color , category=dpg.mvThemeCat_Core)
    
    return theme


def corner_radius_theme():
    with dpg.theme(tag = 'corner_radius'):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,10 , category=dpg.mvThemeCat_Core)
    

def btnHovered_theme(colorHov:tuple[int],colorInit:tuple[int]= (255, 255, 255)):
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,colorHov , category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button,colorInit , category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,10 , category=dpg.mvThemeCat_Core)
        
    return theme

def fontstyle() -> None:
    with dpg.font_registry():
        #bold
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 13, tag = 'small_x_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 15, tag = 'small_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 24, tag = 'medium_y_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 27, tag = 'medium_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf',30, tag = 'large_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 35, tag = 'large_x_bold')

        #normal
        dpg.add_font('toolbox/font/Helvetica.ttf', 13, tag = 'small_x')
        dpg.add_font('toolbox/font/Helvetica.ttf', 15, tag = 'small')
        dpg.add_font('toolbox/font/Helvetica.ttf', 24, tag = 'medium_y')
        dpg.add_font('toolbox/font/Helvetica.ttf', 27, tag = 'medium')
        dpg.add_font('toolbox/font/Helvetica.ttf',30, tag = 'large')
        dpg.add_font('toolbox/font/Helvetica.ttf', 35, tag = 'large_x')

        #combo
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 15, tag = 'combo_font')

def img_stack():
    add_w, add_h, _, add = dpg.load_image("toolbox/images/add.png") # Replace with your image loading logic
    delete_all_w, delete_all_h, _, delete_all = dpg.load_image("toolbox/images/delete_all.png") 
    edit_w, edit_h, _, edit = dpg.load_image("toolbox/images/edit.png") 
    delete_w, delete_h, _, delete = dpg.load_image("toolbox/images/delete.png") 
    default_w, default_h, _, default = dpg.load_image("toolbox/images/default.png") 
    folder_w, folder_h, _, folder = dpg.load_image("toolbox/images/pick_folder.png") 
    clear_w, clear_h, _, clear = dpg.load_image("toolbox/images/clear.png")
    settings_w, settings_h, _, settings = dpg.load_image("toolbox/images/settings.png")
    settings_small_w, settings_small_h, _, settings_small = dpg.load_image("toolbox/images/settings_small.png")
    calendar_w, calendar_h, _, calendar = dpg.load_image("toolbox/images/calendar.png")
    show_w, show_h, _, show = dpg.load_image("toolbox/images/show.png")


    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=add_w, height=add_h, default_value=add, tag = 'add_img')
        dpg.add_static_texture(width=delete_all_w, height=delete_all_h, default_value=delete_all,tag = 'delete_all_img')
        dpg.add_static_texture(width=edit_w, height=edit_h, default_value=edit,tag = 'edit_img')
        dpg.add_static_texture(width=delete_w, height=delete_h, default_value=delete,tag = 'delete_img')
        dpg.add_static_texture(width=default_w, height=default_h, default_value=default,tag = 'default_img')
        dpg.add_static_texture(width=folder_w, height=folder_h, default_value=folder,tag = 'pick_folder_img')
        dpg.add_static_texture(width=clear_w, height=clear_h, default_value=clear,tag = 'clear_img')
        dpg.add_static_texture(width=settings_w, height=settings_h, default_value=settings,tag = 'settings_img')
        dpg.add_static_texture(width=settings_small_w, height=settings_small_h, default_value=settings_small,tag = 'settings_small_img')
        dpg.add_static_texture(width=calendar_w, height=calendar_h, default_value=calendar,tag = 'calendar_img')
        dpg.add_static_texture(width=show_w, height=show_h, default_value=show,tag = 'show_img')