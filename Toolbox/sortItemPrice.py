
import customtkinter as custom
from tkinter import ttk
import pandas as pd
from tkinter.filedialog import askopenfile

global dataTreeview,TOP_LEVEL_ENTRIES,TOP_LEVEL_WIDGETS
TOP_LEVEL_ENTRIES = []
TOP_LEVEL_WIDGETS = []
def convertText_Dict():
    conversionText = {
        'Item ID':'Item_ID',
        'Item Name':'Item_Name',
        'Total_Qty':'T_Qty',
        'Total_Retail Price':'Retail_Price',
        'Total_Price 4':'Price_4',
        'DAVAO GMALL_Qty':'Gmall_Qty',
        'Joyo Davao SM LANANG_Qty':'SML_Qty',
        'Maxsun Gempesaw Davao_Qty':'Main_Qty',
        'Joyo SM ECOLAND_Qty':'SME_Qty',
        'Davao Lanang Warehouse_Qty':'Warehouse_Qty'
    }
    
    return conversionText

def convert_dtypes(dataFrame):
    converDtypes = {
        'Item_ID':'category',
        'Item_Name':'category',
        'T_Qty':'int16',
        'Retail_Price':'float32',
        'Price_4':'float32',
        'Gmall_Qty':'int16',
        'SML_Qty':'int16',
        'Main_Qty':'int16',
        'SME_Qty':'int16',
        'Warehouse_Qty':'int16'
    }
    for column in dataFrame.columns.to_list():
        if column in converDtypes:
            dataFrame[column] = dataFrame[column].astype(converDtypes[column])
    
    return dataFrame

def typeSearchAutoComplete(e):
    checkBoxClicked("")
    
def removed_convert_column(column_header):
    column_container = []
    convert_container = {}
    for column in column_header:
        if column not in convertText_Dict():
            column_container.append(column)
        else:
            convert_container.update({column:convertText_Dict()[column]})

    return column_container,convert_container

def show_checkbox(csvHeaders):
    global gmall_checkbox,sml_checkbox,sme_checkbox,main_checkbox,warehouse_checkbox
    
    gmall_checkbox.pack(side = 'right',padx = (10,0)) if 'Gmall_Qty' in csvHeaders else gmall_checkbox.pack_forget()
    sml_checkbox.pack(side = 'right',padx = (10,0)) if 'SML_Qty' in csvHeaders else sml_checkbox.pack_forget()
    sme_checkbox.pack(side = 'right',padx = (10,0)) if 'SME_Qty' in csvHeaders else sme_checkbox.pack_forget()
    main_checkbox.pack(side = 'right',padx = (10,0)) if 'Main_Qty' in csvHeaders else main_checkbox.pack_forget()
    warehouse_checkbox.pack(side = 'right',padx = 10) if 'Warehouse_Qty' in csvHeaders else warehouse_checkbox.pack_forget()

def check_if_decimal(value):
    try:
        cut = str(value).split('.')
    
        if len(cut)==1:
            return value
        else:
            if cut[1] =="0":
                return int(value)
            else:
                return value
    except Exception as e:
        return value
    
def populate_tree(data_list):
    global showZero_var
    count=0
    dataTreeview.tag_configure("even",background="#8BD9E1")
    dataTreeview.tag_configure("odd",background="#C8ECF0")
    dataTreeview.tag_configure("zero",background="#fd1d1d")
    for item in dataTreeview.get_children():
        dataTreeview.delete(item)

    for data in data_list:
        try:
            value = [r for r in data[0:2] ]+["{:,}".format(check_if_decimal(n)) for n in data[2:]]
        except:
            value = [r for r in data]
            
        if count%2 ==1:
            if str(data[2]) == "0" or str(data[2]) == '' or str(data[2]) == '0.0':
                if showZero_var.get() != '1':
                    dataTreeview.insert(parent='',index=len(dataTreeview.get_children()),tags=("zero",),values=value)
                else:
                    continue
            else:
                dataTreeview.insert(parent='',index=len(dataTreeview.get_children()),tags=("even",),values=value)
        else:
            if str(data[2]) == "0" or str(data[2]) == ''or str(data[2]) == '0.0':
                if showZero_var.get() != '1':
                    dataTreeview.insert(parent='',index=len(dataTreeview.get_children()),tags=("zero",),values=value)
                else:
                    continue
            else:
                dataTreeview.insert(parent='',index=len(dataTreeview.get_children()),tags=("odd",),values=value)
        
        count+=1

def populate_entry(data_list):
    pass

def extractData(importEntry):
    global treeFrame
    try:
        df= pd.read_excel(importEntry).fillna(0)[2:].to_csv('whole_csv.csv', encoding = 'utf-8',header = False,index = None)
        df = pd.read_csv('whole_csv.csv')
        df = df.drop(removed_convert_column(df.columns.to_list())[0],axis = 1)
        df = df.rename(columns=removed_convert_column(df.columns.to_list())[1], errors="raise")
        convert_dtypes(df).to_feather('original_copy.feather')
        df = pd.read_feather('original_copy.feather')
        if len(df.columns.to_list()) == 5:
            df['T_Qty']= df[df.columns.to_list()[-1]]

        df['T_Qty']= df.iloc[:,5:].sum(axis = 1)

        show_checkbox(df.columns.to_list())
        viewGenerator(treeFrame,df.columns.to_list(),df.values.tolist())
        
        import_entry.delete(0,'end')
        import_entry.configure(text_color = "green")
        import_entry.insert(0,'Extraction Success')
        
        import_btn.configure(text = "Import",command=openFile)

    except Exception as e:
        print(e)
        import_entry.delete(0,'end')
        import_entry.insert(0,'Error Extracting File')
        
def openFile():
    global import_entry
    try:
        import_entry.configure(text_color = "#ECDFCC")
        import_entry.delete(0,'end')
        file = askopenfile(mode='r',filetypes=[("Excel File","*.*")])
        import_entry.insert(0,file.name)
        import_btn.configure(text = "Extract", command = lambda:extractData(import_entry.get()))
    except Exception as e:
        import_entry.delete(0,'end')
        import_entry.insert(0,'Error Opening File')

def comboSelect(e):
    checkBoxClicked("")

def checkBoxClicked(checkBox_variable):
    global search_entry,sortWithComboBox
    try:
        remove_branch = checkList('0',gmall_var.get(),sml_var.get(),sme_var.get(),main_var.get(),warehouse_var.get())
        #new_df = df.drop(remove_branch, axis = 1)
        df = pd.read_feather('original_copy.feather').drop(remove_branch, axis = 1)
        if len(df.columns.to_list()) == 5:
            df['T_Qty']= df[df.columns.to_list()[-1]]

        df['T_Qty']= df.iloc[:,5:].sum(axis = 1)
        df  = df.loc[df[sortWithComboBox.get()].str.contains(search_entry.get(),case=False)]
        viewGenerator(treeFrame,df.columns.to_list(),df.values.tolist())

    except Exception as e:
        print(e)
        import_entry.delete(0,'end')
        import_entry.insert(0,"Can't Execute Command")

def checkList(condition,gmall,sml,sme,main,warehouse):
    branch_list = [gmall,sml,sme,main,warehouse]
    remove_branch = []

    for branch in branch_list:
        if branch is not condition:
            remove_branch.append(branch)
    return remove_branch

def sortItemPriceWindow(tabview):
    global import_entry,search_entry,dataTreeview,sortWithComboBox,sortValue,import_btn,treeFrame,df,read_copy_var
    global gmall_var,sml_var,sme_var,main_var,warehouse_var,showZero_var
    global gmall_checkbox,sml_checkbox,sme_checkbox,main_checkbox,warehouse_checkbox,showZero_checkbox
    
    headerCheckFrame = custom.CTkFrame(tabview,fg_color = "transparent")
    headerCheckFrame.pack()

    headerFrame = custom.CTkFrame(headerCheckFrame,fg_color = "transparent")
    headerFrame.pack(pady = 5,side = 'left')
    checkFrame = custom.CTkFrame(headerCheckFrame,fg_color = "transparent", height=28, width=400)
    checkFrame.pack(pady = 5,side = 'left')

    treeFrame = custom.CTkFrame(tabview)
    treeFrame.pack( padx = 10, fill = "both", expand = True)

    #headerFrame
    sortValue = ["Item_ID","Item_Name"]
    sortWithComboBox = custom.CTkComboBox(headerFrame,values=sortValue,width=105)
    sortWithComboBox.bind('<<ComboboxSelected>>', comboSelect)
    sortWithComboBox.grid(row = 0, column = 0,padx = (0,5))

    search_entry = custom.CTkEntry(headerFrame, placeholder_text="Search....",font=("Halvetica",20,"italic"),width= 300)
    search_entry.grid(row = 0,column = 1)
    search_entry.bind("<KeyRelease>", typeSearchAutoComplete)

    import_btn = custom.CTkButton(headerFrame,text="Import", width=50,command=openFile)#, command=openFile
    import_btn.grid(row = 0,column = 2,padx = 5)

    import_entry = custom.CTkEntry(headerFrame,font=("Calibri",10,"italic"), width=50)
    import_entry.grid(row = 0,column = 3)

    #headerFrame
    showZero_var = custom.StringVar()
    gmall_var = custom.StringVar()
    sml_var = custom.StringVar()
    sme_var = custom.StringVar()
    main_var = custom.StringVar()
    warehouse_var = custom.StringVar()

    #CheckBox

    gmall_checkbox = custom.CTkCheckBox(checkFrame,text="Gmall",onvalue = '0',offvalue = "Gmall_Qty",variable =gmall_var ,checkbox_width = 15,checkbox_height = 15,height = 0,width = 0,corner_radius = 20,command=lambda:checkBoxClicked(gmall_checkbox))
    sml_checkbox = custom.CTkCheckBox(checkFrame,text="SML",onvalue = '0',offvalue = "SML_Qty",variable =sml_var,checkbox_width = 15,checkbox_height = 15,height = 0,width = 0,corner_radius = 20, command=lambda:checkBoxClicked(sml_checkbox))
    sme_checkbox = custom.CTkCheckBox(checkFrame,text="SME",onvalue = '0',offvalue = "SME_Qty",variable =sme_var,checkbox_width = 15,checkbox_height = 15,height = 0,width = 0,corner_radius = 20, command=lambda:checkBoxClicked(sme_checkbox))
    main_checkbox = custom.CTkCheckBox(checkFrame,text="Main",onvalue = '0',offvalue = "Main_Qty",variable =main_var,checkbox_width = 15,checkbox_height = 15,height = 0,width = 0,corner_radius = 20, command=lambda:checkBoxClicked(main_checkbox))
    warehouse_checkbox = custom.CTkCheckBox(checkFrame,text="Warehouse",onvalue = '0',offvalue = "Warehouse_Qty",variable =warehouse_var,checkbox_width = 15,checkbox_height = 15,height = 0,width = 0,corner_radius = 20, command=lambda:checkBoxClicked(warehouse_checkbox))

    gmall_checkbox.select()
    sml_checkbox.select()
    sme_checkbox.select()
    main_checkbox.select()
    warehouse_checkbox.select()

    try:
        df = pd.read_feather('original_copy.feather')
        column_names = df.columns.to_list()
        data_values = df.values.tolist()
        show_checkbox(df.columns.to_list())
    
    except Exception as e:
        column_names = ["null","null","null","null","null"]
        data_values = [["No","Data","Available","..."],["Import","First","To","Stored"],["Try","Again","Later","...."]]
    
    showZero_checkbox = custom.CTkCheckBox(checkFrame,text="Zero",onvalue = '1',offvalue = "0",variable =showZero_var ,checkbox_width = 15,checkbox_height = 15,height = 0,width = 0,corner_radius = 20,command=lambda:checkBoxClicked(''))
    showZero_checkbox.pack(side = 'left',padx = 10)
    dataTreeview = ttk.Treeview(treeFrame,columns=column_names)
    viewGenerator(treeFrame,column_names,data_values)
    
def viewGenerator(treeFrame,column_names,data_list):
    read_only_container(treeFrame,column_names,data_list)# if read_copy_var.get()!= "read" else can_copy_container(treeFrame,column_names,data_list)

def keyReleaseTopLevel(e, topLevel,values,width_entry):
    if e.keysym == "Escape":
        topLevel.destroy()
    if e.keysym == "Left":
        topLevel.event_generate('<Tab>')
    if e.keysym == "Right":
        topLevel.event_generate('<Control-Shift-KeyPress-Tab>')
    if e.keysym == "BackSpace":
        destroy_all_items(TOP_LEVEL_ENTRIES)
        retainData(topLevel,values,width_entry)

def openTopLevel(e,dataTreeview,treeFrame):
    # 0 ,1 , 4
    if len(TOP_LEVEL_WIDGETS) !=0:
        destroy_all_items(TOP_LEVEL_WIDGETS)

    x = (treeFrame.winfo_width()//2) - 395
    y = (treeFrame.winfo_height()//2) + 60

    selected = dataTreeview.item(dataTreeview.selection())['values']
    values = [selected[0],selected[1],selected[4]]
    width_entry = [150,750,70]

    topLevel = custom.CTkToplevel()
    topLevel.title("Clipboard")
    topLevel.resizable(False,False)
    topLevel.geometry(f"{x}+{y}")
    topLevel.bind("<KeyRelease>",lambda e : keyReleaseTopLevel(e,topLevel,values,width_entry))
    
    retainData(topLevel,values,width_entry)
    TOP_LEVEL_WIDGETS.append(topLevel)
    
def retainData(topLevel,values,width_entry):
    
    for column,value,width in zip(range(len(values)),values,width_entry):
        entry=custom.CTkEntry(topLevel, width = width)
        entry.grid(row = 0,column = column, padx = 5,pady = 5)
        entry.bind("<KeyRelease>",lambda e : keyReleaseTopLevel(e,topLevel,values,width_entry))
        entry.insert(0,value)
        TOP_LEVEL_ENTRIES.append(entry)

def destroy_all_items(list_container):
    for value in list_container:
        value.destroy()
                      
def read_only_container(treeFrame,column_names,data_list):
    global dataTreeview,search_entry,sortWithComboBox
    dataTreeview.destroy()
    WHOLE_WIDTH = 1060-350
    dataTreeview = ttk.Treeview(treeFrame,columns=column_names, height=26)
    dataTreeview.bind("<Double-Button-1>",lambda e :openTopLevel(e,dataTreeview,treeFrame))
    dataTreeview.pack(fill = 'both')
    treeFrame.pack()

    dataTreeview.heading("#0")
    for head in column_names:
        dataTreeview.heading(head, text=head)
    for column in column_names:
        qty = f"{column[-3]}{column[-2]}{column[-1]}"
        if qty=="Qty" :
            WHOLE_WIDTH = WHOLE_WIDTH-50

    dataTreeview.column("#0", width = 0, stretch = "no")
    for column in column_names:
        qty = f"{column[-3]}{column[-2]}{column[-1]}"
        if column == "Item_ID":
            dataTreeview.column(column, width = 150)
        elif column == "Item_Name":
            dataTreeview.column(column, width = WHOLE_WIDTH)
        elif column == "Retail_Price" or column == "Price_4":
            dataTreeview.column(column, width = 75,anchor="center", stretch = "no")
        elif qty=="Qty":
            dataTreeview.column(column, width =50,anchor="center", stretch = "no")
        else:
            dataTreeview.column(column, width = 210,anchor="center", stretch = "no")
    
    populate_tree(data_list)


