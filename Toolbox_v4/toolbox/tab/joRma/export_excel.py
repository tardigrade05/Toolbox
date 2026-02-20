from openpyxl import load_workbook
from copy import copy
import time
import subprocess
from toolbox.models import Personal,Settings_Model
from toolbox import session
from sqlalchemy import select

def insertToExcelRMA(person:Personal):
    ITEMS = person.items
    ITEM_LENGTH = len(person.items)
    ITEM_ROW_START = 9
    ITEM_ADD_ROWS = ITEM_LENGTH-1
    ITEM_LAST_ROW =  (ITEM_LENGTH + ITEM_ROW_START)-1
    path_to_save = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'pick_records_default_path')).first()

    try:
        path = "toolbox/Source/RMA/RMAForm.xlsx"
        ref_workBook = load_workbook(path)
        sheet=ref_workBook.active


        sheet['C4'].value = person.branch
        sheet['C5'].value = person.customer_name
        sheet['C6'].value = person.contact_number
        sheet['G5'].value = person.reference
        sheet['G6'].value = person.date
        
        if ITEM_LENGTH != 1:
            sheet.insert_rows(ITEM_ROW_START ,ITEM_ADD_ROWS)

        for index,item in enumerate(ITEMS):
            copy_row_format(sheet, ITEM_LAST_ROW, ITEM_ROW_START + index)
            sheet[f'B{ITEM_ROW_START+index}'].value = index + 1
            sheet[f'C{ITEM_ROW_START+index}'].value = item.name
            sheet[f'D{ITEM_ROW_START+index}'].value = item.description
            sheet[f'E{ITEM_ROW_START+index}'].value = 1
            sheet[f'F{ITEM_ROW_START+index}'].value = item.serial
            sheet[f'G{ITEM_ROW_START+index}'].value = item.tech_finding
            sheet[f'H{ITEM_ROW_START+index}'].value = person.warranty_start
            sheet[f'I{ITEM_ROW_START+index}'].value = person.dr_number
        
        sheet[f'D{11 + ITEM_ADD_ROWS}'].value = person.tech_name
        sheet[f'H{11 + ITEM_ADD_ROWS}'].value = person.tech_name
        sheet[f'D{12 + ITEM_ADD_ROWS}'].value = person.date
        sheet[f'H{12 + ITEM_ADD_ROWS}'].value = person.date

        TIME_MILLISECONDS = int(time.time())
        file_name = f'{path_to_save.value}/{person.customer_name}-RMA_{TIME_MILLISECONDS}.xlsx'
        ref_workBook.save(filename= file_name)
        app_open_spreadsheet(filename=file_name)
        subprocess.run(rf'explorer /select,{file_name}')

    except Exception as e:
        print(f'Rma Error {e}')
        return

def copy_row_format(ws, source_row, new_row):
    for col in range(1, ws.max_column + 1):

        source_cell = ws.cell(row=source_row, column=col)
        new_cell = ws.cell(row=new_row, column=col)

        new_cell.font = copy(source_cell.font)
        new_cell.border = copy(source_cell.border)
        new_cell.fill= copy(source_cell.fill)
        new_cell.alignment = copy(source_cell.alignment)
        new_cell.number_format = copy(source_cell.number_format)
        new_cell.protection = copy(source_cell.protection)

    
def insertToExcelJO(person:Personal):
    ITEMS = person.items
    ITEM_LENGTH = len(person.items)
    ITEM_ROW_START = 24
    ITEM_ADD_ROWS = ITEM_LENGTH-1
    ITEM_LAST_ROW =  (ITEM_LENGTH + ITEM_ROW_START)-1
    path_to_save = session.scalars(select(Settings_Model).where(Settings_Model.tag == 'pick_records_default_path')).first()

    
    try:
        path = "toolbox/Source/JO/JobOrderForm.xlsx"
        ref_workBook = load_workbook(path)
        sheet=ref_workBook.active

        sheet['D8'].value = person.dr_number
        sheet['D9'].value = person.customer_name
        sheet['D10'].value = "JOYO MARKETING"
        sheet['H6'].value = person.job_order
        sheet['H7'].value = person.date
        sheet['H8'].value = person.warranty_start
        sheet['H9'].value = person.warranty_end
        sheet['H10'].value = person.remaining
        sheet['F19'].value = person.customer_name
      
        if ITEM_LENGTH != 1:
            sheet.insert_rows(ITEM_ROW_START ,ITEM_ADD_ROWS)

        for index,item in enumerate(ITEMS):
            copy_row_format(sheet, ITEM_LAST_ROW, ITEM_ROW_START + index)

            sheet[f'C{ITEM_ROW_START+index}'].value = index + 1
            sheet[f'D{ITEM_ROW_START+index}'].value = item.name
            sheet[f'E{ITEM_ROW_START+index}'].value = item.description
            sheet[f'F{ITEM_ROW_START+index}'].value = item.serial
            sheet[f'G{ITEM_ROW_START+index}'].value = item.customer_issues
            sheet[f'H{ITEM_ROW_START+index}'].value = item.tech_finding
            changeRowColumnCell(sheet,"E",f"{ITEM_ROW_START+index}",item.description)

        sheet[f'E{26 + ITEM_ADD_ROWS}'].value = person.tech_name

        merge_cell(sheet,ITEM_ADD_ROWS,3,8)

        TIME_MILLISECONDS = int(time.time())
        file_name = f'{path_to_save.value}/{person.customer_name}-JO_{TIME_MILLISECONDS}.xlsx'
        ref_workBook.save(filename= file_name)
        app_open_spreadsheet(filename=file_name)
        subprocess.run(rf'explorer /select,{file_name}')

    except Exception as e:
        print(f'JO Error {e}')
        return


def changeRowColumnCell(sheet,column,row,value):
    textLength = len(str(value))
    heightTimes = int(textLength/20)
    if heightTimes < 1:
        sheet.row_dimensions[int(row)].height = 20
        sheet.column_dimensions[column].width = 30
    else:
        sheet.row_dimensions[int(row)].height = 20*(heightTimes+1)
        sheet.column_dimensions[column].width = 30
    # save the file 

def merge_cell(ws,item_length,c_from,c_end):
    row_list = [29,36,43,49]
    for value in row_list:
        ws.merge_cells(start_row=item_length+value, start_column=c_from, end_row=item_length+value, end_column=c_end)

def app_open_spreadsheet(filename):
    subprocess.Popen(['start','/WAIT','excel',filename],shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.Popen(['start','/WAIT','WPS Office',filename],shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.Popen(['start','/WAIT','LibreOffice Calc',filename],shell=True,creationflags=subprocess.CREATE_NO_WINDOW)