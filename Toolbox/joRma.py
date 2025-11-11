import customtkinter as custom
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image
import joRmaHelper as helper
import insertExcelWorkBook as insertExcel
import datetime
from idlelib.tooltip import Hovertip
from CTkMessagebox import CTkMessagebox
import search

# root = custom.CTk()
# root.geometry("1020x650")
df = helper.initialValue_feather()
global ITEM_LABELS,ITEM_ENTRIES,CONSTANT_ENTRIES,ALL_ITEM_FRAMES,rmaFrame
global joItemCodeEntry,rmaItemNameEntry
global main_Frame,constantFrame,itemFrame
CONSTANT_ENTRIES = []

ALL_ITEM_FRAMES = []
ITEM_LABELS = []
ITEM_ENTRIES = []

# style = ttk.Style()
# style.configure('my.DateEntry')

lbl_color = '#0366fc'
conerRadius = 5
labelWidth = 145
entryWidth = 250
dateWidth = int(25/1.8)
padding = (5,0)

def toolTip(widget,balloonMsg):
    toolTip = Hovertip(widget,balloonMsg,hover_delay = 100)


def joRmaMain(tabview):
    global const_itemFrame
    style = ttk.Style()
    style.configure('my.DateEntry')

    labelFont = custom.CTkFont(family="Halvetica", size=13,weight="bold")
    year =str(datetime.datetime.now().strftime("%Y"))
    helper.make_path(year,"Data")
    helper.make_path(year,"JO_RMA",save_to_desktop=True)

    main_Frame = custom.CTkScrollableFrame(tabview)
    main_Frame.pack(fill="both", expand=True)

    const_itemFrame = custom.CTkFrame(main_Frame,width = 0)
    const_itemFrame.pack(fill = "both")
    constantLayout(const_itemFrame)
    
    generateCopyButton = custom.CTkButton(main_Frame, text="GENERATE COPY", width=1010,height=40, font=labelFont,command=generateCopy) #,command=generateCopy
    generateCopyButton.pack(pady = 5)

def generateCopy():
    global branchCombo,dateEntry,jobOrderEntry,referenceNumberEntry,drNumberEntry,warrantyStartDate,warrantyEndDate,remainingWarrantyEntry,contactNumberEntry,clientNameEntry,techNameEntry
    try:
        id = drNumberEntry.get()+referenceNumberEntry.get()+jobOrderEntry.get()
        constant_list = [branchCombo.get(),helper.formatDate("-","mm/dd/yyyy",dateEntry.get_date()),jobOrderEntry.get(),referenceNumberEntry.get(),drNumberEntry.get(),helper.formatDate("-","mm/dd/yyyy",warrantyStartDate.get_date()),helper.formatDate("-","mm/dd/yyyy",warrantyEndDate.get_date()),remainingWarrantyEntry.get(),contactNumberEntry.get(),clientNameEntry.get(),techNameEntry.get(),id]
        constant_list_to_excel = [branchCombo.get(),dateEntry.get_date(),clientNameEntry.get(),contactNumberEntry.get(),referenceNumberEntry.get(),jobOrderEntry.get(),warrantyStartDate.get_date(),warrantyEndDate.get_date(),remainingWarrantyEntry.get(),techNameEntry.get(),drNumberEntry.get()]

        item_value_list = []

        for index,per_itemEntry in zip(range(len(ITEM_ENTRIES)),ITEM_ENTRIES):
            item_value_list.append([])
            for itemEntry in per_itemEntry:
                item_value_list[index].append(itemEntry.get())
        
        helper.save_dataframe(constant_list,item_value_list)
        df = helper.initialValue_feather()

        insertExcel.insertToExcelRMA(constant_list_to_excel,ITEM_ENTRIES)
        insertExcel.insertToExcelJO(constant_list_to_excel,ITEM_ENTRIES)

        referenceNumberEntry.delete(0,'end')
        referenceNumberEntry.insert(0,str(int(df['Ref_Number'].iloc[-1])+1))
        jobOrderEntry.delete(0,'end')
        jobOrderEntry.insert(0,helper.jobOrder_generator(branchCombo.get(),dateEntry.get_date()))
        contactNumberEntry.delete(0,'end') 
        clientNameEntry.delete(0,'end')
        techNameEntry.delete(0,'end')
        drNumberEntry.delete(0,'end')
        remainingWarrantyEntry.delete(0,'end')
        remove_item()
        filename = helper.read_txt("filename.txt","r")
        
        helper.app_open_spreadsheet(filename)
        search.refresh()

    except IndexError:
        CTkMessagebox(title="Info", message="Add item first...")
    
def remove_item(hint = "remove_all"):
    try:
        if hint !="remove_all":
            ALL_ITEM_FRAMES[-1].destroy()
            ALL_ITEM_FRAMES.pop()

            for labels,entry in zip(ITEM_LABELS[-1],ITEM_ENTRIES[-1]):
                labels.destroy()
                entry.destroy()
            ITEM_LABELS.pop()
            ITEM_ENTRIES.pop()

        else:
            for frame in ALL_ITEM_FRAMES:
                frame.destroy()
            ALL_ITEM_FRAMES.clear()
           
            for per_itemLabel,per_itemEntry in zip(ITEM_LABELS,ITEM_ENTRIES):
                for label,entry in zip(per_itemLabel,per_itemEntry):
                    label.destroy()
                    entry.destroy()

            ITEM_LABELS.clear()
            ITEM_ENTRIES.clear()

    except Exception as e:
        print(f'{e} this is the error comming')
        return

def add_item():
    global const_itemFrame
    itemLayout(const_itemFrame)

def dateKeyRelease(e,rmaCombo,date):
    jobOrderEntry.delete(0,'end')
    jobOrderEntry.insert(0,helper.jobOrder_generator(rmaCombo,date))

def remainingWarrantyResult(e,end,start):
    filter_date = str(end-start).split(' ')
    remainingWarrantyEntry.delete(0,'end')
    remainingWarrantyEntry.insert(0,filter_date[0])

def ref_number_generator(referenceNumberEntry,df):
    referenceNumberEntry.delete(0,'end')
    referenceNumberEntry.insert(0,str(int(df['Ref_Number'].iloc[-1])+1))

def jo_number_generator(jobOrderEntry,branchCombo,dateEntry):
    jobOrderEntry.delete(0,'end')
    jobOrderEntry.insert(0,helper.jobOrder_generator(branchCombo.get(),dateEntry.get_date()))


def constantLayout(const_itemFrame):
    labelFont = custom.CTkFont(family="Halvetica", size=13,weight="bold")
    entryFont = custom.CTkFont(family="Halvetica", size=15,slant="italic")
    titleFont = custom.CTkFont(family="Arial Black", size=25,weight="bold")
    add_image = custom.CTkImage(light_image=Image.open("images/add_dark.png"),
                                    dark_image=Image.open("images/add_dark.png"),
                                    size=(24, 24))
    remove_image = custom.CTkImage(light_image=Image.open("images/remove.png"),
                                    dark_image=Image.open("images/remove.png"),
                                    size=(24, 24))

    global branchCombo,dateEntry,jobOrderEntry,referenceNumberEntry,drNumberEntry,dateOfPurchaseEntry,warrantyStartDate,warrantyEndDate,remainingWarrantyEntry,contactNumberEntry,clientNameEntry,techNameEntry
    constantFrame = custom.CTkFrame(const_itemFrame, border_color="#FFD700",border_width=2)
    constantFrame.pack()

    constant_titleLabel = custom.CTkLabel(constantFrame, text="Personal Details", font=titleFont, fg_color='transparent')
    constant_titleLabel.grid(row = 0, column = 0, columnspan = 6, padx = 10, pady = 10)
    addItem_btn = custom.CTkButton(constantFrame, text = '',image = add_image,hover_color="#7a9af7",fg_color="white",width = 1,command= add_item)
    addItem_btn.place(relx =.9,rely = .05)
    toolTip(addItem_btn,"Add Item")
    removeItem_btn = custom.CTkButton(constantFrame, text = '',image = remove_image,hover_color="#f47a7a",fg_color="white",width = 1,command= lambda: remove_item(""))
    removeItem_btn.place(relx =.945,rely = .05)
    toolTip(removeItem_btn,"Remove Item")
    
    #Label
    branchComboLabel = custom.CTkLabel(constantFrame, text="Branch",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    branchComboLabel.grid(row = 1, column = 0,padx = padding,pady = padding)
    
    dateLabel = custom.CTkLabel(constantFrame, text="Date",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    dateLabel.grid(row = 2, column = 0,padx = padding,pady = padding)

    jobOrderLabel = custom.CTkLabel(constantFrame, text="Job Order #",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    jobOrderLabel.grid(row = 3,column = 0,padx = padding,pady = padding)

    referenceNumberLabel = custom.CTkLabel(constantFrame, text="Reference #",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    referenceNumberLabel.grid(row = 4, column = 0,padx = padding,pady = padding[0])
#------------------
    drNumberLabel = custom.CTkLabel(constantFrame, text="DR #",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    drNumberLabel.grid(row = 1, column = 2,padx = padding,pady = padding)

    warrantyStartLabel = custom.CTkLabel(constantFrame, text="Warranty Start",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    warrantyStartLabel.grid(row = 2, column = 2,padx = padding,pady = padding)

    warrantyEndLabel = custom.CTkLabel(constantFrame, text="Warranty End",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    warrantyEndLabel.grid(row = 3, column = 2,padx = padding,pady = padding)

    remainingWarrantyLabel = custom.CTkLabel(constantFrame, text="Remaining Warranty",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    remainingWarrantyLabel.grid(row = 4, column = 2,padx = padding,pady = padding[0])
#------------------
    contactNumberLabel = custom.CTkLabel(constantFrame, text="Contact #",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    contactNumberLabel.grid(row = 1, column = 4,padx = padding,pady = padding)

    clientNameLabel = custom.CTkLabel(constantFrame, text="Customer Name",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    clientNameLabel.grid(row = 2, column = 4,padx = padding,pady = padding)

    techNameLabel = custom.CTkLabel(constantFrame, text="Techician Name",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    techNameLabel.grid(row = 3, column = 4,padx = padding,pady = padding)
    
    #InputFields
    branchCombo = custom.CTkComboBox(constantFrame, values= ["SML", "SME","GMALL","MAIN"],font=entryFont,width=entryWidth//1.67)
    branchCombo.grid(row = 1, column =1,padx = padding,pady = padding)
    branchCombo.set(str(df['Branch'].iloc[-1]))

    dateEntry =DateEntry(constantFrame,width = dateWidth, font = ("Halvetica",13,"italic"),selectmode="day",date_pattern="MM/DD/YYYY")
    dateEntry.bind("<<DateEntrySelected>>",lambda event: dateKeyRelease(event,branchCombo.get(),dateEntry.get_date()))
    dateEntry.bind("<KeyRelease>",lambda event: dateKeyRelease(event,branchCombo.get(),dateEntry.get_date()))
    dateEntry.grid(row = 2, column = 1,padx = padding,pady = padding)

    jobOrderEntry = custom.CTkEntry(constantFrame,font=entryFont,width=entryWidth//1.7)
    jobOrderEntry.grid(row = 3, column = 1,padx = padding,pady = padding)
    #print(helper.jobOrder_generator(rmaBranchCombo.get(),rmaDateEntry.get_date()))
    #jobOrderEntry.insert(0,helper.jobOrder_generator(branchCombo.get(),dateEntry.get_date()))
    jo_number_generator(jobOrderEntry,branchCombo,dateEntry)
    
    referenceNumberEntry = custom.CTkEntry(constantFrame,font=entryFont,width=entryWidth//1.7)
    referenceNumberEntry.grid(row = 4, column = 1,padx = padding,pady = padding[0])
    #referenceNumberEntry.insert(0,str(int(df['Ref_Number'].iloc[-1])+1))
    ref_number_generator(referenceNumberEntry,df)
#------------------
    drNumberEntry = custom.CTkEntry(constantFrame,font=entryFont,width=entryWidth//1.7)
    drNumberEntry.grid(row = 1, column = 3,padx = padding,pady = padding)

    warrantyStartDate=DateEntry(constantFrame,width = dateWidth, font = ("Halvetica",13,"italic"),selectmode="day",date_pattern="mm/dd/yyy")
    warrantyStartDate.grid(row = 2, column = 3,padx = padding,pady = padding)

    warrantyEndDate = DateEntry(constantFrame,width = dateWidth, font = ("Halvetica",13,"italic"),selectmode="day",date_pattern="mm/dd/yyy")
    warrantyEndDate.bind("<<DateEntrySelected>>",lambda event:remainingWarrantyResult(event,warrantyEndDate.get_date(),dateEntry.get_date()))
    warrantyEndDate.bind("<KeyRelease>",lambda event:remainingWarrantyResult(event,warrantyEndDate.get_date(),dateEntry.get_date()))
    warrantyEndDate.grid(row = 3, column = 3,padx = padding,pady = padding)

    remainingWarrantyEntry = custom.CTkEntry(constantFrame,font=entryFont,width=entryWidth//1.7)
    remainingWarrantyEntry.grid(row = 4, column = 3,padx = padding,pady=padding[0])
#------------------
    contactNumberEntry = custom.CTkEntry(constantFrame,font=entryFont,width=entryWidth)
    contactNumberEntry.grid(row = 1, column = 5,padx = padding[0],pady = padding)

    clientNameEntry = custom.CTkEntry(constantFrame,font=entryFont,width=entryWidth)
    clientNameEntry.grid(row = 2, column = 5,padx = padding[0],pady = padding)

    techNameEntry = custom.CTkEntry(constantFrame,font=entryFont,width=entryWidth)
    techNameEntry.grid(row = 3, column = 5,padx = padding[0],pady = padding)

def itemLayout(itemFrame):
    labelFont = custom.CTkFont(family="Halvetica", size=13,weight="bold")
    entryFont = custom.CTkFont(family="Halvetica", size=15,slant="italic")
    titleFont = custom.CTkFont(family="Arial Black", size=25,weight="bold")

    per_itemFrame = custom.CTkFrame(itemFrame,bg_color='transparent', border_color="#DC143C",border_width=2)
    per_itemFrame.pack(pady = padding, fill = "both")

    #labels
    itemNameLabel = custom.CTkLabel(per_itemFrame, text="Item Name",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    itemNameLabel.grid(row = 0, column = 0,padx = padding,pady = padding)

    descriptionLabel = custom.CTkLabel(per_itemFrame, text="Description",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    descriptionLabel.grid(row = 1, column = 0,padx = padding,pady = padding)

    serialNumberLabel = custom.CTkLabel(per_itemFrame, text="Serial #",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    serialNumberLabel.grid(row = 2, column = 0,padx = padding,pady = padding[0])
#------------------
    remarksLabel = custom.CTkLabel(per_itemFrame, text="Customer Issues",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    remarksLabel.grid(row = 0, column = 2,padx = padding,pady = padding)

    branchTechFindingLabel = custom.CTkLabel(per_itemFrame, text="Tech Finding",font=labelFont,width=labelWidth, fg_color=lbl_color,corner_radius=conerRadius)
    branchTechFindingLabel.grid(row = 1, column = 2,padx = padding,pady = padding)

    #InputFields
    itemNameEntry = custom.CTkEntry(per_itemFrame,font=entryFont,width=int(entryWidth*1.40))
    itemNameEntry.grid(row = 0, column = 1,padx = padding,pady = padding)

    descriptionEntry = custom.CTkEntry(per_itemFrame,font=entryFont,width=int(entryWidth*1.40))
    descriptionEntry.grid(row = 1, column =1,padx = padding,pady = padding)

    serialNumberEntry = custom.CTkEntry(per_itemFrame,font=entryFont,width=int(entryWidth*1.40))
    serialNumberEntry.grid(row = 2, column = 1,padx = padding,pady = padding[0])
#------------------
    remarksEntry = custom.CTkEntry(per_itemFrame,font=entryFont,width=int(entryWidth*1.40))
    remarksEntry.grid(row = 0, column = 3,padx = padding[0],pady = padding)

    branchTechFindingEntry = custom.CTkEntry(per_itemFrame,font=entryFont,width=int(entryWidth*1.40))
    branchTechFindingEntry.grid(row = 1, column = 3,padx = padding[0],pady = padding)

    ALL_ITEM_FRAMES.append(per_itemFrame)
    ITEM_ENTRIES.append([itemNameEntry,descriptionEntry,serialNumberEntry,remarksEntry,branchTechFindingEntry])
    ITEM_LABELS.append([itemNameLabel,descriptionLabel,serialNumberLabel,remarksLabel,branchTechFindingLabel])


# joRmaMain(root)

# root.mainloop()