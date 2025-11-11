import customtkinter as custom
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from idlelib.tooltip import Hovertip
from PIL import Image
import pandas as pd
import joRmaHelper as helper
import shutil
import os
import subprocess
import joRma

# root = custom.CTk()
# root.geometry("1020x650")
def refresh():
    try:
        df =helper.initialValue_feather()
        treeviewGenerator(treeFrame,filter_dataframe(df[1:],df[1:].columns.to_list()).values.tolist())
    except:
        CTkMessagebox(title="Error", message="No saved file exits.", icon="cancel")
        return

def export_csv_file():
    df =pd.read_feather("JO_RMA_VALUES.feather")
    csv_file = df.to_csv("Data/VALUES.csv",index=False)
    shutil.copy(f"Data/VALUES.csv",f"{helper.targetPath("Desktop")}/JO_RMA/")
    CTkMessagebox(title = "Info",message = "Export CVS Completed")

def removeString(value,replace_by,replace_to):
    value = value.replace(replace_by,replace_to)
    return value

def open_rma_jo_file(e,treeview):
    #6 , ref num
    #7 , jo num
    uniqueCode= ""
    selected = treeview.selection()
    date = removeString(treeview.item(selected[0])['values'][0],"\n","")
    ref_num = removeString(str(treeview.item(selected[0])['values'][6]),"\n","")
    jo_num = removeString(treeview.item(selected[0])['values'][7],"\n","")[-1]
    dr_number = removeString(str(treeview.item(selected[0])['values'][9]),"\n","")
    name = removeString(treeview.item(selected[0])['values'][1],"\n","").upper()

    if openFile_ComboBox.get() == "RMA":
        uniqueCode = f"{date}_{dr_number}{ref_num}"
    elif openFile_ComboBox.get() == "JO":
        uniqueCode = f"{date}_{dr_number}{jo_num}"
        
    filename = f"{helper.targetPath("Desktop")}/JO_RMA/Data/{openFile_ComboBox.get()}/{date.split("-")[-1]}/{name}-{openFile_ComboBox.get()} {uniqueCode}.xlsx"
    helper.app_open_spreadsheet(filename)

def searchWindow(searchTab,root):

    global sortValue,searchTreeview,treeFrame,openFile_ComboBox,openFileLocation_btn,deleteForm_btn, main_root
    main_root = root
    treeViewStyleHeading = ttk.Style()
    treeViewStyleHeading.configure('search.Treeview',rowheight=60,font=('Arial',8, 'bold'))
    refresh_image = custom.CTkImage(light_image=Image.open("images/refresh.png"),
                                    dark_image=Image.open("images/refresh.png"),
                                    size=(24, 24))
    exportCsv_image = custom.CTkImage(light_image=Image.open("images/csv.png"),
                                    dark_image=Image.open("images/csv.png"),
                                    size=(24, 24))

    sortValue = [
        "Client_Name",
        "Contact_Number",
        "Description",
        "Serial_Number",
        "Tech_Finding",
        "Ref_Number",
        "JO_Number",
        "Tech_Name"]
    
    searchFrame  = custom.CTkFrame(searchTab)
    searchFrame.pack()
    treeFrame  = custom.CTkFrame(searchTab)
    treeFrame.pack(fill = 'both', expand  = True,padx = (0,10), pady = (0,10))
    searchTreeview = ttk.Treeview(treeFrame,style='search.Treeview',height=5)

    sortWithComboBox = custom.CTkComboBox(searchFrame,values=sortValue,width=150)
    sortWithComboBox.grid(row = 0, column = 0)
    toolTip(sortWithComboBox,"Pick to filter")

    typeSearchEntry = custom.CTkEntry(searchFrame, placeholder_text="Search Here...", font=("Halvetica",20,"italic"), width=400)
    typeSearchEntry.grid(row = 0,column = 1, pady = 10,padx = 10)
    typeSearchEntry.bind("<KeyRelease>", lambda e : typesearch(e,sortWithComboBox,typeSearchEntry))
    toolTip(typeSearchEntry,"Search")

    openFile_ComboBox = custom.CTkComboBox(searchFrame,values=["RMA", "JO"],width=100)
    openFile_ComboBox.grid(row = 0, column = 2)
    toolTip(openFile_ComboBox,"Set what to open")

    export_csv = custom.CTkButton(searchFrame,text = "",hover_color="#7a9af7",fg_color = "white",image = exportCsv_image,width=1, command = export_csv_file)
    export_csv.grid(row = 0, column = 3, padx = (10,0))
    toolTip(export_csv,"Export values to csv \n(Desktop/JO_RMA/Data/VALUES.csv)")

    refresh_btn = custom.CTkButton(searchFrame,text = "",hover_color="#7a9af7",fg_color = "white",image = refresh_image,width=1, command = refresh)
    refresh_btn.grid(row = 0, column = 4, padx = (10,0))
    toolTip(refresh_btn,"Refresh")

    openFileLocation_btn = custom.CTkButton(searchFrame, text="Open Location", width=100)
    openFileLocation_btn.grid_forget()

    deleteForm_btn = custom.CTkButton(searchFrame, text="Delete", width=100)
    deleteForm_btn.grid_forget()

    df =helper.initialValue_feather()
    
    treeviewGenerator(treeFrame,filter_dataframe(df[1:],df[1:].columns.to_list()).values.tolist())

def typesearch(e,sortWithComboBox,typeSearchEntry):
    df =pd.read_feather("JO_RMA_VALUES.feather")
    new_df  = filter_dataframe(df[1:],df[1:].columns.to_list())
    new_df  = new_df.loc[new_df[sortWithComboBox.get()].str.contains(typeSearchEntry.get(),case=False)]
    treeviewGenerator(treeFrame,new_df.values.tolist())

def treeviewGenerator(treeFrame,data_list):
    
    column_names = [
        "Date",
        "Client_Name",
        "Contact_Number",
        "Description",
        "Serial_Number",
        "Tech_Finding",
        "Ref_Number",
        "JO_Number",
        "Tech_Name",
        "Dr_Number",
    ]

    column_width = [65,65,65,395,100,145,30,88,65,30]
    
    global searchTreeview,search_entry,sortWithComboBox
    searchTreeview.destroy()
    searchTreeview = ttk.Treeview(treeFrame,style='search.Treeview',columns=column_names,height=5)
    searchTreeview.bind("<Double-Button-1>",lambda e :open_rma_jo_file(e,searchTreeview))
    searchTreeview.bind("<Button-1>", lambda e :show_button_functions(e,searchTreeview))
    searchTreeview.pack(fill = "both", expand = True)#fill = 'both'
    toolTip(searchTreeview,"Double click item to open Excel file")

    searchTreeview.heading("#0")
    searchTreeview.column("#0", width = 0, stretch = "no")
    
    for column, width_index in zip(column_names,column_width):
        if column !="Dr_Number":
            searchTreeview.heading(column, text=column)
            searchTreeview.column(column, width = width_index,anchor="center", stretch = "no")
        else:
            searchTreeview.heading(column)
            searchTreeview.column(column, width = -1, stretch = "no")

    populate_tree(data_list)

def show_button_functions(e,searchTreeview):
    global openFileLocation_btn,deleteForm_btn
    openFileLocation_btn.grid(row = 0, column = 5, padx = (10,0))
    deleteForm_btn.grid(row = 0, column = 6, padx = 10)

    openFileLocation_btn.configure(command = lambda:openFileLocation(openFileLocation_btn,deleteForm_btn,searchTreeview))
    deleteForm_btn.configure(command = lambda:deleteForm(openFileLocation_btn,deleteForm_btn,searchTreeview))


def deleteForm(openFileLocation_btn,deleteForm_btn,searchTreeview):
    global main_root
    msg = CTkMessagebox(title="Delete Form", message="Are you sure?",
                        icon="question", option_1="Cancel", option_2="No", option_3="Yes")
    response = msg.get()
    
    if response=="Yes":
        try:
            selected = searchTreeview.selection()
            date = removeString(searchTreeview.item(selected[0])['values'][0],"\n","")
            ref_num = removeString(str(searchTreeview.item(selected[0])['values'][6]),"\n","")
            jo_num = removeString(searchTreeview.item(selected[0])['values'][7],"\n","")
            dr_number = removeString(str(searchTreeview.item(selected[0])['values'][9]),"\n","")
            name = removeString(searchTreeview.item(selected[0])['values'][1],"\n","").upper()

            jo_filename = f"Data/JO/{date.split("-")[-1]}/{name}-JO {date}_{dr_number}{jo_num[-1]}.xlsx"
            rma_filename = f"Data/RMA/{date.split("-")[-1]}/{name}-RMA {date}_{dr_number}{ref_num}.xlsx"
        
            helper.make_path(date[6:],"JO_RMA",True)

            if os.path.exists(jo_filename) and os.path.exists(rma_filename):
                os.remove(jo_filename)
                os.remove(rma_filename)
                print(f"All Files deleted successfully.")
            else:
                print(f"File does not exist.")

            helper.make_path(date[6:],"JO_RMA",True)
            
            
            df =pd.read_feather("JO_RMA_VALUES.feather")
            df.reset_index()
            
            drop_item = df[df['id'] == f'{dr_number}{ref_num}{jo_num}'].index
            
            new = df.drop(drop_item)
            new = new.reset_index(drop=True)
            new.to_feather("JO_RMA_VALUES.feather")

            new_df = helper.initialValue_feather()
          
            joRma.ref_number_generator(joRma.referenceNumberEntry,new_df)
            joRma.jo_number_generator(joRma.jobOrderEntry,joRma.branchCombo,joRma.dateEntry)

                  
            treeviewGenerator(treeFrame,filter_dataframe(new_df[1:],new_df[1:].columns.to_list()).values.tolist())
            hideButtons(openFileLocation_btn,deleteForm_btn,searchTreeview,False)
            
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message="Error Occurs , Try closing connected files...", icon="cancel")


def openFileLocation(openFileLocation_btn,deleteForm_btn,searchTreeview):
    selected = searchTreeview.selection()
    uniqueCode= ""
    selected = searchTreeview.selection()
    date = removeString(searchTreeview.item(selected[0])['values'][0],"\n","")
    ref_num = removeString(str(searchTreeview.item(selected[0])['values'][6]),"\n","")
    jo_num = removeString(searchTreeview.item(selected[0])['values'][7],"\n","")[-1]
    dr_number = removeString(str(searchTreeview.item(selected[0])['values'][9]),"\n","")
    name = removeString(searchTreeview.item(selected[0])['values'][1],"\n","").upper()

    if openFile_ComboBox.get() == "RMA":
        uniqueCode = f"{date}_{dr_number}{ref_num}"
    elif openFile_ComboBox.get() == "JO":
        uniqueCode = f"{date}_{dr_number}{jo_num}"
    date = removeString(searchTreeview.item(selected[0])['values'][0],"\n","")

    filename = f"{helper.targetPath("Desktop")}/JO_RMA/Data/{openFile_ComboBox.get()}/{date.split("-")[-1]}/{name}-{openFile_ComboBox.get()} {uniqueCode}.xlsx".replace("/","\\")
    try:
        subprocess.run(rf'explorer /select,{filename}')
    except Exception as e:
        CTkMessagebox(title="Error", message="File not found", icon="cancel")
    
    hideButtons(openFileLocation_btn,deleteForm_btn,searchTreeview)

def hideButtons(openFileLocation_btn,deleteForm_btn,searchTreeview,open_file = True):
    openFileLocation_btn.grid_forget()
    deleteForm_btn.grid_forget()
    if open_file:
        searchTreeview.selection_remove(searchTreeview.focus())
    else:
        return


def populate_tree(data_list):
    count=0
    searchTreeview.tag_configure("even",background="#8BD9E1")
    searchTreeview.tag_configure("odd",background="#C8ECF0")
    column_width = [65,65,65,395,100,145,30,88,65,30]
    for item in searchTreeview.get_children():
        searchTreeview.delete(item)
    
    for data in data_list:
        value = [newline(str(r),int(width*.16)) for r,width in zip(data,column_width)]
            
        if count%2 ==1:
            searchTreeview.insert(parent='',index=len(searchTreeview.get_children()),tags=("even",),values=value)
        else:
            searchTreeview.insert(parent='',index=len(searchTreeview.get_children()),tags=("odd",),values=value)

        count+=1

def filter_dataframe(df,header_list):
    remove = []
    column_names = [
        "Date",
        "Client_Name",
        "Contact_Number",
        "Description",
        "Serial_Number",
        "Tech_Finding",
        "Ref_Number",
        "JO_Number",
        "Tech_Name",
        "Dr_Number"
    ]

    for column in header_list:
        if column not in column_names:
            remove.append(column)

    new = df.drop(remove,axis=1)
    new = df[column_names]
    return new

def newline(string,width):
    finalText = ""
    text_list = []

    newLineTimes = (len(string)//width)+1

    if newLineTimes ==1:
        return string

    for x in range(0,newLineTimes):
        try:
            text_list.append(string[width*x:width*(x+1)])
        except:
            text_list.append(string[width*x:0])

    for text in text_list:
        finalText = finalText + text+"\n"

    return finalText

def toolTip(widget,balloonMsg):
    toolTip = Hovertip(widget,balloonMsg,hover_delay = 100)

# searchWindow(root)
# root.mainloop()

