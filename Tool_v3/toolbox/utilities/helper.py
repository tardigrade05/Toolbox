# import pandas as pd
import dearpygui.dearpygui as dpg
import time
# from toolbox.utilities.DataClass import Color
from toolbox.utilities.colorstyles import changeTextColor_theme
from toolbox.models import AtdTables_Model,CashCount_Model
from toolbox import session
from sqlalchemy import select


def add_comma(value):
    res = ""
    if value != "":
        try:
            try_split = str(value).split(".")

            if len(try_split[1]) == 1 and try_split[1] == "0":
                res = ('{:,}'.format(int(f"{try_split[0]}")))
            else:
                res = ('{:,}'.format(float(value)))
        
        except IndexError:
            res = ('{:,}'.format(int(value)))

        except ValueError:
            return res
    else:
        return res

    return str(res)


def mod_round(value):
    mod = ""
    prev_round = round(value,2) #4.56

    splitter = str(prev_round).split(".")

    if len(splitter[1]) == 2: #4.56
        mod = f"{splitter[0]}{splitter[1][0]}{splitter[1][1]}0" #4_560
    if len(splitter[1]) == 1: #4.5
        mod = f"{splitter[0]}{splitter[1][0]}00" #4_500

    return int(mod)
       

def deal_with_decimal(value, float_values = 1000):
    total = 0

    try:
        act_val = str(value).split(".")

        if len(act_val[1]) >= 3:
            if int(act_val[1][2])==9:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{int(act_val[1][2])}")

            elif int(act_val[1][2])>=5:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{int(act_val[1][2])+1}")
               
            elif int(act_val[1][2])<5:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{act_val[1][2]}")

            total = mod_round(init_val)

        elif len(act_val[1]) < 3:
            total = int(float((f"{act_val[0]}.{act_val[1]}"))*float_values)

    except Exception as e:
        total = int(value*float_values)
    
    return total

def max_char(tag_name:str,data:str,number:int):
    try:
        if len(data) > number:
            dpg.configure_item(tag_name, readonly = True)
            dpg.set_value(tag_name, data[:number])
            time.sleep(.1)
            dpg.configure_item(tag_name, readonly = False)
            return True
    except:
        pass

def clean_data(value):
    try:
        initial = value.replace(',','')
        final = deal_with_decimal(float(initial))/1000
        return final
    
    except ValueError:
        return 0/1000

    except:
        final = deal_with_decimal(initial)/1000
        return final


def realtime():
    cashcount = session.scalars(select(CashCount_Model)).all()
    total_sales = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'total_sales')).first()
    if total_sales is None or total_sales.value == '':
        total_sales_val = '0'
    else:
        total_sales_val = total_sales.value

    card_values = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'card_atd_tables')).all() 
    homeCredit_values = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'homeCredit_atd_tables')).all() 
    billEase_values = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'billease_atd_tables')).all() 
    form_values = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'form_atd_tables')).all() 
    bankTrans_values = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'bankTrans_atd_tables')).all() 
    expenses_values = session.scalars(select(AtdTables_Model).where(AtdTables_Model.category == 'expenses_atd_tables')).all() 


    cashcount_total = sum([int(value.product) for value in cashcount])#/1000
    card_total = sum([int(value.value) for value in card_values])#/1000
    homeCredit_total = sum([int(value.value) for value in homeCredit_values])#/1000
    billEase_total = sum([int(value.value) for value in billEase_values])#/1000
    form_total = sum([int(value.value) for value in form_values])#/1000
    bankTrans_total = sum([int(value.value) for value in bankTrans_values])#/1000
    expenses_total = sum([int(value.value) for value in expenses_values])#/1000

    total_subtract = card_total + homeCredit_total + billEase_total + form_total +bankTrans_total + expenses_total
    amountToDeposit = int(total_sales_val)*1_000 - total_subtract
    over_or_lacking = cashcount_total*10 - amountToDeposit


    dpg.set_value('total_cashcount',add_comma(cashcount_total/100))

    dpg.set_value('card_atd_input',add_comma(card_total/1000))
    dpg.set_value('homeCredit_atd_input',add_comma(homeCredit_total/1000))
    dpg.set_value('billease_atd_input',add_comma(billEase_total/1000))
    dpg.set_value('form_atd_input',add_comma(form_total/1000))
    dpg.set_value('bankTrans_atd_input',add_comma(bankTrans_total/1000))
    dpg.set_value('expenses_atd_input',add_comma(expenses_total/1000))

    
    dpg.set_value('amount_to_deposit_atd_input',add_comma(amountToDeposit/1000))

    if over_or_lacking/1000>0:
        dpg.set_value('normal_atd_lbl', value = 'OVER KA BOI!')
        dpg.bind_item_theme('normal_atd_input',changeTextColor_theme((5, 245, 85)))
        
    elif over_or_lacking/1000<0:
        over_or_lacking = abs(over_or_lacking)
        dpg.set_value('normal_atd_lbl', value = 'LUH GG OYY!')
        dpg.bind_item_theme('normal_atd_input',changeTextColor_theme((244, 122, 122)))
        
    elif over_or_lacking/1000 == 0:
        dpg.set_value('normal_atd_lbl', value = 'PAYTS RA!')
        dpg.bind_item_theme('normal_atd_input',changeTextColor_theme((255,255,255)))

    dpg.set_value('normal_atd_input',add_comma(over_or_lacking/1000))
        


