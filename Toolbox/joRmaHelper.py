from CTkMessagebox import CTkMessagebox
import pandas as pd
import os
import shutil
import subprocess

def formatDate(separator,pattern,date):
    new_date = str(date).split("-")
    if pattern == "mm/dd/yyyy":
        return f'{new_date[1]}{separator}{new_date[2]}{separator}{new_date[0]}'
    elif pattern == "dd/mm/yyyy":
        return f'{new_date[2]}{separator}{new_date[1]}{separator}{new_date[0]}'

def jobOrder_generator(rmaCombo,date):
    df = pd.read_feather('JO_RMA_VALUES.feather')
    #print(f'{df} ... dataframe')
    letter = str(chr(65)) if ord(str(df['JO_Number'].iloc[-1])[-1])+1 >90  else str(chr(ord(str(df['JO_Number'].iloc[-1])[-1])+1))
    jo_number = f'{rmaCombo.upper()}{formatDate("","mm/dd/yyyy",date)}{letter}'
    return jo_number

def convert_dtypes(dataFrame):
    converDtypes = {
        'Branch':'category',
        'Date':'category',
        'Client_Name':'category',
        'Contact_Number':'category',
        'Item_Name':'category',
        'Description':'category',
        'Serial_Number':'category',
        'Customer_Complaint':'category',
        'Tech_Finding':'category',

        'Ref_Number':'category',
        'JO_Number':'category',
        'Warranty_Start':'category',
        'Warranty_End':'category',
        'Warranty_Remaining':'category',
        'Tech_Name':'category',
        'id':'category'

    }

    for column in dataFrame.columns.to_list():
        if column in converDtypes:
            dataFrame[column] = dataFrame[column].astype(converDtypes[column])
    
    return dataFrame


def initialValue_feather():
    try:
        df = pd.read_feather('JO_RMA_VALUES.feather')
        return df
    
    except:
        data = dataFrame_Structure(["SML","","0000000000Z","0","","","","","","","",""],[["","","","",""]])

        df = pd.DataFrame(data)
        convert_dtypes(df).to_feather('JO_RMA_VALUES.feather')
        df = pd.read_feather('JO_RMA_VALUES.feather')

        return df

def list_to_string(list_value):
    return ",".join(list_value)


def dataFrame_Structure(constant_list,item_list):
    #print(f'{constant_list}... dataframe_structure')
    reverse_df = pd.DataFrame(item_list).transpose().astype('category').values.tolist()
    #print(reverse_df)

    key_value = {
        'Branch':[constant_list[0]],
        'Date':[constant_list[1]],
        'JO_Number':[constant_list[2]],
        'Ref_Number':[constant_list[3]],
        'Dr_Number':[constant_list[4]],
        'Warranty_Start':[constant_list[5]],
        'Warranty_End':[constant_list[6]],
        'Warranty_Remaining':[constant_list[7]],
        'Contact_Number':[constant_list[8]],
        'Client_Name':[constant_list[9]],
        'Tech_Name':[constant_list[10]],
        'id':[constant_list[11]],
        
        'Item_Name':[list_to_string(reverse_df[0])],
        'Description':[list_to_string(reverse_df[1])],
        'Serial_Number':[list_to_string(reverse_df[2])],
        'Customer_Complaint':[list_to_string(reverse_df[3])],
        'Tech_Finding':[list_to_string(reverse_df[4])],

        }
    return key_value


def save_dataframe(constant_list,item_list):
    #print(f'{constant_list}... save_dataframe')
    #print(dataFrame_Structure(constant_list,item_list))
    try:
        df_feather = pd.read_feather('JO_RMA_VALUES.feather')
        add_new = pd.DataFrame(dataFrame_Structure(constant_list,item_list))

        df_feather = pd.concat([convert_dtypes(df_feather),convert_dtypes(add_new)],ignore_index = True)
        df_feather.to_feather("JO_RMA_VALUES.feather")
        
# convert_dtypes(df).to_feather('JO_RMA_VALUES.feather')
# df = pd.read_feather('JO_RMA_VALUES.feather')

    except:
        print("No Dataframe found")
        add_new = pd.DataFrame(dataFrame_Structure(constant_list,item_list))
        convert_dtypes(add_new).to_feather('JO_RMA_VALUES.feather')

    #print(f'{constant_list} constant value')
    #print(f'{item_list} item value')


def targetPath(hint):
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['USERPROFILE'], hint).replace("\\","/")
    elif os.name == 'posix':  # macOS or Linux
        return os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        return None  # Unsupported operating system
#shutil.copy(f"Data/RMA/{str(year)}/{str(constant_list[2]).upper()}-RMA {fileName}.xlsx",f"{targetPath("Desktop")}/JO_RMA/Data/RMA/{str(year)}/")

def make_path(year,hint,save_to_desktop = False):
    if save_to_desktop:

        desktop_path = f"{targetPath("Desktop")}/{hint}"
        print(desktop_path+"  ..path")
        try:
            shutil.rmtree(desktop_path)
            print("Delete Finished")
        except:
            os.makedirs(f'{desktop_path}')
            print("Make path desktop success")
       
        shutil.copytree(f"Data",f"{desktop_path}/Data")
    else:
        rma_path = f"{hint}/RMA/{str(year)}"
        jo_path = f"{hint}/JO/{str(year)}"
        try:
            os.makedirs(rma_path)
            os.makedirs(jo_path)
        except:
            return
        
def read_txt(text_file,option):
    with open(text_file,option) as f:
        if option == "r":
            return f.read()
        
def write_txt(filename,text_file,option):
    with open(text_file,option) as f:
        if option == "w":
            f.write(filename)

def app_open_spreadsheet(filename):
    subprocess.Popen(['start','/WAIT','excel',filename],shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.Popen(['start','/WAIT','WPS Office',filename],shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.Popen(['start','/WAIT','LibreOffice Calc',filename],shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
    