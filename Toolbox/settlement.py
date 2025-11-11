import customtkinter as custom
from tkinter import ttk
from PIL import Image
from CTkMessagebox import CTkMessagebox
import math
import pandas as pd
from idlelib.tooltip import Hovertip

# custom.set_appearance_mode("Dark")
# root  = custom.CTk()
# root.title("ToolBox")
# root.geometry("1020x650")
# root.iconbitmap("images/tool-box.ico")
 
CASH_ALL_INPUT_ENTRIES = []
CASH_PRODUCT_RESULTS_LBL = []
EXPONENT = 2
VALUE_DEALS_FLOAT = math.pow(10,EXPONENT)
cashBillsBgColor = "#9B3922"
cashQtyBgColor = "#481E14"
cashTotalBgColor = "#F2613F"
textColor = "#ECDFCC"
cashCountWidth = 75


class Tabview_Window():
    def __init__(self, oddColor,evenColor):
        super().__init__()

        self.oddColor = oddColor
        self.evenColor = evenColor

    def window(self,tab):
        treeViewHeight = 15
        tabViewFrame= custom.CTkFrame(tab,fg_color="transparent")
        tabViewFrame.pack()
        
        self.add_image = custom.CTkImage(light_image=Image.open("images/add_dark.png"),
                                    dark_image=Image.open("images/add_dark.png"),
                                    size=(24, 24))
        self.delete_image = custom.CTkImage(light_image=Image.open("images/delete_dark.png"),
                                    dark_image=Image.open("images/delete_dark.png"),
                                    size=(24, 24))
        self.update_image = custom.CTkImage(light_image=Image.open("images/update.png"),
                                    dark_image=Image.open("images/update.png"),
                                    size=(24, 24))
        self.deleteAll_image = custom.CTkImage(light_image=Image.open("images/delete_all_dark.png"),
                                    dark_image=Image.open("images/delete_all_dark.png"),
                                    size=(24, 24))
        
        self.treeView = ttk.Treeview(tabViewFrame,style="settlement.Treeview",height=treeViewHeight,show='tree')
        self.treeView.tag_configure("odd",background=self.oddColor)
        self.treeView.tag_configure("even",background=self.evenColor)

        self.inputValueEntry = custom.CTkEntry(tabViewFrame, font=('Halvetica', 20),width=165)
        self.inputValueEntry.grid(row = 0,column = 0, padx = (5,5),pady=(5,0))
        self.inputValueEntry.bind("<KeyRelease>",self.keyReleaseAdd)

        self.addValueButton = custom.CTkButton(tabViewFrame,hover_color="#7a9af7",fg_color="white",width = 1,image=self.add_image,text="",command=self.addData) #
        self.addValueButton.grid(row = 0,column = 1, padx = (0,5),pady=(5,0))

        self.deleteValueButton = custom.CTkButton(tabViewFrame,hover_color="#f47a7a",fg_color="white",text="",width = 1,image=self.deleteAll_image, command=self.deleteAllData)#
        self.deleteValueButton.grid(row = 0,column = 2, padx = (0,5),pady=(5,0))

        self.treeView.bind("<ButtonRelease-1>",self.clickTreeView)
        self.treeView.bind("<ButtonRelease-3>",self.unClicktreeView)
        self.treeView.grid(row = 1,column=0,columnspan=3,padx=5,pady=5)
        self.treeView['columns']= ('Column1')

        self.treeView.column("#0",width=0,stretch='no')
        self.treeView.column("Column1",width=250,anchor='center')
        self.treeView.grid(row = 1,column = 0, columnspan=3)

    def keyReleaseAdd(self,e):
        if str(e.keysym) == "Return" or str(e.keysym) == "plus":
            self.addData()
            self.inputValueEntry.delete(0,'end')
        else:
            pass
    def unClicktreeView(self,e):
        try:
            self.inputValueEntry.delete(0,'end')
            self.addValueButton.configure(image = self.add_image,command=self.addData)#
            self.deleteValueButton.configure(image = self.deleteAll_image, command=self.deleteAllData)#
        except:
            pass
    def clickTreeView(self,e):
        try:
            newData = self.treeView.item(self.treeView.focus()).get('values')[0]
            self.inputValueEntry.delete(0,'end')
            self.inputValueEntry.insert(0,str(newData))
        
            self.addValueButton.configure(image = self.update_image,command= self.updateSelectData)#
            self.deleteValueButton.configure(image = self.delete_image,command= self.deleteSelectedData)#

        except:
            pass
    
    def get_tree_items(self):
        newData = []
        for lists in self.treeView.get_children():
            for data in self.treeView.item(lists)['values']:
                newData.append(removeCommaNumber(data))

        return newData
    
    def insert_tree_items(self,newData):
        count = 0
        for item in self.treeView.get_children():
            self.treeView.delete(item)
        
        for item in newData:
            if item == "0" or item == "" :
                pass
            else:
                if count%2 ==1:
                    self.treeView.insert(parent='',index=count+1,values=(str(addCommaNumber(convertFloatOrInt(item)))),tags=("odd",))
                else:
                    self.treeView.insert(parent='',index=count+1,values=(str(addCommaNumber(convertFloatOrInt(item)))),tags=("even",))
                count+=1

    def populateTree(self):
        newData= []
        count = 0
        newData=self.get_tree_items()
        for item in self.treeView.get_children():
            self.treeView.delete(item)

        for item in newData:
            if item == "0" or item == "" :
                pass
            else:
                if count%2 ==1:
                    self.treeView.insert(parent='',index=count+1,values=(str(addCommaNumber(convertFloatOrInt(item)))),tags=("odd",))
                else:
                    self.treeView.insert(parent='',index=count+1,values=(str(addCommaNumber(convertFloatOrInt(item)))),tags=("even",))
                count+=1

    def addData(self):
        print(f"{convertFloatOrInt(self.inputValueEntry.get().rstrip("+"))} .. add data")
        value = str(addCommaNumber(convertFloatOrInt(self.inputValueEntry.get().rstrip("+"))))
        self.treeView.insert(parent='',index=len(self.treeView.get_children()),values=value)
        self.inputValueEntry.delete(0,'end')
        self.populateTree()
        overOrLacking()
        save_data(manual_click = False)
        

    def deleteAllData(self):
        for item in self.treeView.get_children():
            self.treeView.delete(item)
        self.inputValueEntry.delete(0,'end')
        self.populateTree()
        #save_data(manual_click = False)
        overOrLacking()
        

        
    def deleteSelectedData(self):
        for item in self.treeView.selection():
            self.treeView.delete(item)
        self.inputValueEntry.delete(0,'end')
        self.populateTree()
        overOrLacking()
        save_data(manual_click = False)
   
     
    def updateSelectData(self):
        self.treeView.item(self.treeView.focus(),text ='', values = (self.inputValueEntry.get()))
        self.inputValueEntry.delete(0,'end')
        self.populateTree()
        overOrLacking()
        save_data(manual_click = False)

    def total(self):
        total = 0.0
        for lists in self.treeView.get_children():
            for data in self.treeView.item(lists)['values']:
                total = total+(float(removeCommaNumber(data))*VALUE_DEALS_FLOAT)
        
        return total

def convert_dtypes(dataFrame):
    converDtypes = {
        'Card':'category',
        'HomeCredit':'category',
        'BillEase':'category',
        'Form':'category',
        'BankTransfer':'category',
        'Expenses':'category',
        'QtyCashValues':'category',
        'TotalSales':'category',
    }

    for column in dataFrame.columns.to_list():
        if column in converDtypes:
            dataFrame[column] = dataFrame[column].astype(converDtypes[column])
    
    return dataFrame

def save_dataframe(card,homeCredit,billEase,form,bankTransfer,expenses,qty_values,totalSales):
    df = convert_dtypes(pd.DataFrame(dataFrame_Structure(card,homeCredit,billEase,form,bankTransfer,expenses,qty_values,totalSales)))
    df.to_feather("SETTLEMENT_VALUES.feather")

def dataFrame_Structure(card,homeCredit,billEase,form,bankTransfer,expenses,qty_values,totalSales):

    key_value = {
        'Card':[",".join(card)],
        'HomeCredit':[",".join(homeCredit)],
        'BillEase':[",".join(billEase)],
        'Form':[",".join(form)],
        'BankTransfer':[",".join(bankTransfer)],
        'Expenses':[",".join(expenses)],
        'QtyCashValues':[",".join(qty_values)],
        'TotalSales':[totalSales],
        }
    return key_value

def import_data():

    global cardTab,homeCreditTab,billEaseTab,formTab,bankTransferTab,expensesTab, totalSalesEntry,cash_finalResultFrame
    clear()
    all_total = 0.0
    multiplier = [1000*VALUE_DEALS_FLOAT,500*VALUE_DEALS_FLOAT,200*VALUE_DEALS_FLOAT,100*VALUE_DEALS_FLOAT,50*VALUE_DEALS_FLOAT,20*VALUE_DEALS_FLOAT,10*VALUE_DEALS_FLOAT,5*VALUE_DEALS_FLOAT,1*VALUE_DEALS_FLOAT,.5*VALUE_DEALS_FLOAT,.25*VALUE_DEALS_FLOAT,.1*VALUE_DEALS_FLOAT,.05*VALUE_DEALS_FLOAT]

    try:
        df = pd.read_feather("SETTLEMENT_VALUES.feather").values.tolist()[0]
    except:
        CTkMessagebox(title="Error", message="No saved file exits.", icon="cancel")
        return

    for number,entry,label,value in zip(multiplier,CASH_ALL_INPUT_ENTRIES,CASH_PRODUCT_RESULTS_LBL,df[6].split(",")):
        
        try:
            entry.insert(0,value)
            value_text = float(number)*float(value)
            all_total = all_total+value_text
            label.configure(text =addCommaNumber(convertFloatOrInt(round(value_text/VALUE_DEALS_FLOAT,EXPONENT))))
        except Exception as e:
            pass
    totalSalesEntry.delete(0,"end")    
    totalcashCountEntry.delete(0,"end")
    totalcashCountEntry.insert(0,addCommaNumber(convertFloatOrInt(round(all_total/VALUE_DEALS_FLOAT,EXPONENT))))
    cardTab.insert_tree_items(df[0].split(","))
    homeCreditTab.insert_tree_items(df[1].split(","))
    billEaseTab.insert_tree_items(df[2].split(","))
    formTab.insert_tree_items(df[3].split(","))
    bankTransferTab.insert_tree_items(df[4].split(","))
    expensesTab.insert_tree_items(df[5].split(","))

    totalSalesEntry.insert(0,df[7])
    overOrLacking()
    
def save_data(manual_click = True):
    global tabview,cardTab,homeCreditTab,billEaseTab,formTab,bankTransferTab,expensesTab, totalSalesEntry
    qty_values = []
    for entry in CASH_ALL_INPUT_ENTRIES:
        qty_values.append(entry.get())

    card = cardTab.get_tree_items()
    homeCredit = homeCreditTab.get_tree_items()
    billEase = billEaseTab.get_tree_items()
    form = formTab.get_tree_items()
    bankTransfer= bankTransferTab.get_tree_items()
    expenses= expensesTab.get_tree_items()
    totalSales = totalSalesEntry.get()

    save_dataframe(card,homeCredit,billEase,form,bankTransfer,expenses,qty_values,totalSales)

    if manual_click:
        CTkMessagebox(title="Info", message="Save Successfully")


def clear_data():
    msg = CTkMessagebox(title="Clear", message="Are you sure you wanted to clear fields?",
                        icon="question", option_1="Cancel", option_2="No", option_3="Yes")
    response = msg.get()
    
    if response == "Yes":
        clear()
    else:
        return
     
def clear():
    global totalcashCountEntry,totalSalesEntry
    global cardTab,homeCreditTab,billEaseTab,formTab,bankTransferTab,expensesTab
    cardTab.deleteAllData()
    homeCreditTab.deleteAllData()
    billEaseTab.deleteAllData()
    bankTransferTab.deleteAllData()
    formTab.deleteAllData()
    expensesTab.deleteAllData()

    for entry,lbl in zip(CASH_ALL_INPUT_ENTRIES,CASH_PRODUCT_RESULTS_LBL):
        entry.delete(0,"end")
        entry.insert(0,"")
        lbl.configure(text = "0")
    
    totalSalesEntry.delete(0,'end')
    #totalSalesEntry.insert(0,'0')

    totalcashCountEntry.delete(0,'end')
    totalcashCountEntry.insert(0,'0')
    overOrLacking()   
    
def overOrLacking():
    global tabview,cardTab,homeCreditTab,billEaseTab,formTab,bankTransferTab,expensesTab
    global totalCardEntry,totalHomeCreditEntry,totalBillEaseEntry,totalBankTransferEntry,formEntry,totalExpensesEntry,totalSalesEntry,totalcashCountEntry,overOrLackingEntry,overOrLackingLabel,amountToDepositEntry
    
    total = cardTab.total()+homeCreditTab.total()+billEaseTab.total()+bankTransferTab.total()+formTab.total()+expensesTab.total()
    amountToDepositValue = (float(filterTotalSales(totalSalesEntry))*VALUE_DEALS_FLOAT)-total
    
    overLackingValue = (float(removeCommaNumber(totalcashCountEntry.get()))*VALUE_DEALS_FLOAT)-amountToDepositValue

    if overLackingValue<0:
        overOrLackingEntry.configure(border_color ="red",text_color = "red")
        overOrLackingLabel.configure(fg_color = "red", text = "LACKING")
    elif overLackingValue>0:
        overOrLackingEntry.configure(border_color ="green",text_color = "green")
        overOrLackingLabel.configure(fg_color = "green", text = "OVER")
    else:
        overOrLackingEntry.configure(border_color ="#565a5f",text_color = '#d6d7d7')
        overOrLackingLabel.configure(fg_color = '#202021', text = "NORMAL")

    totalCardEntry.delete(0,"end")
    totalHomeCreditEntry.delete(0,"end")
    totalBillEaseEntry.delete(0,"end")
    totalBankTransferEntry.delete(0,"end")
    formEntry.delete(0,"end")
    totalExpensesEntry.delete(0,"end")
    overOrLackingEntry.delete(0,"end")
    amountToDepositEntry.delete(0,"end")
 
    totalCardEntry.insert(0,covertedShowValues(cardTab.total()))
    totalHomeCreditEntry.insert(0,covertedShowValues(homeCreditTab.total()))
    totalBillEaseEntry.insert(0,covertedShowValues(billEaseTab.total()))
    totalBankTransferEntry.insert(0,covertedShowValues(bankTransferTab.total()))
    formEntry.insert(0,covertedShowValues(formTab.total()))
    totalExpensesEntry.insert(0,covertedShowValues(expensesTab.total()))
    overOrLackingEntry.insert(0,covertedShowValues(overLackingValue))
    amountToDepositEntry.insert(0,covertedShowValues(amountToDepositValue))
    
def covertedShowValues(value, VALUE_DEALS_FLOAT=math.pow(10,EXPONENT), EXPONENT =2):
    return str(addCommaNumber(convertFloatOrInt(round(value/VALUE_DEALS_FLOAT,EXPONENT))))

def noInputNeeded(e):
    overOrLacking()

def addCommaNumber(value):
    try:
        return ('{:,}'.format(value)) 
    except:
        print("Error Add Comma")
        
def removeCommaNumber(value):
    return str(value).replace(",", "")

def convertFloatOrInt(value):
    if value !="":
        try:
            if "." in str(float(value)) and str(float(removeCommaNumber(value))).split(".")[-1][-1]!="0":
                return float(value)
            else:
                return int(float(value))
        except:
            return 0
    else:
        return 0
def totalSalesPress(e):
    overOrLacking()
    save_data(manual_click = False)

def filterTotalSales(value):
    container = 0
    try:
        container=float(value.get())
    except ValueError:
        if value.get() == "":
            container =0
        elif len(value.get())>=1 and value.get() != "":
            container = value.get()[0:-1].rstrip(" ")
            value.delete(0,"end")
            value.insert(0,container)
    
    return float(container)

def cashKeyPressed(e,cashFrame,multiplier):
    global totalcashCountEntry
    all_total = 0.0
    if e.keysym =="Down":
        cashFrame.event_generate('<Tab>')
    if e.keysym =="Up":
        cashFrame.event_generate('<Control-Shift-KeyPress-Tab>')

    for number,entry,label in zip(multiplier,CASH_ALL_INPUT_ENTRIES,CASH_PRODUCT_RESULTS_LBL):
        try:
            value_text = float(entry.get())*float(number)
            all_total = all_total+value_text
            label.configure(text =addCommaNumber(convertFloatOrInt(round(value_text/VALUE_DEALS_FLOAT,EXPONENT))))
    
#str(addCommaNumber(convertFloatOrInt((value_text/VALUE_DEALS_FLOAT):.2f)))        
        except:
            label.configure(text = "0")
    totalcashCountEntry.delete(0,'end')
    totalcashCountEntry.insert(0,str(addCommaNumber(convertFloatOrInt(round(all_total/VALUE_DEALS_FLOAT,EXPONENT)))))
    overOrLacking()
    save_data(manual_click = False)
        
def cash_Frame(cashFinalFrame):
    global totalcashCountEntry
    cashCountLabelFont = custom.CTkFont('Halvetica',28)
    cashCountEntryFont = custom.CTkFont('Halvetica',25)
    finalResultEntryFont = custom.CTkFont('Halvetica',25)
    multiplier = [1000*VALUE_DEALS_FLOAT,500*VALUE_DEALS_FLOAT,200*VALUE_DEALS_FLOAT,100*VALUE_DEALS_FLOAT,50*VALUE_DEALS_FLOAT,20*VALUE_DEALS_FLOAT,10*VALUE_DEALS_FLOAT,5*VALUE_DEALS_FLOAT,1*VALUE_DEALS_FLOAT,.5*VALUE_DEALS_FLOAT,.25*VALUE_DEALS_FLOAT,.1*VALUE_DEALS_FLOAT,.05*VALUE_DEALS_FLOAT]
    frame = custom.CTkFrame(cashFinalFrame,fg_color="transparent")
    frame.pack(side = custom.TOP)

    for index,number in zip(range(0,len(multiplier)),multiplier):
        denomination_lbl =custom.CTkLabel(frame,text_color = textColor,text=str(convertFloatOrInt(round(number/VALUE_DEALS_FLOAT,EXPONENT))),width = cashCountWidth,font=cashCountLabelFont, fg_color=cashBillsBgColor)
        qty_entry = custom.CTkEntry(frame,text_color = textColor,width = cashCountWidth,font=cashCountEntryFont,fg_color=cashQtyBgColor,justify="center")
        qty_entry.bind("<KeyRelease>",lambda e :cashKeyPressed(e,frame,multiplier))
        qty_entry.bind("<ButtonRelease-1>",lambda e :cashKeyPressed(e,frame,multiplier))
        product_results = custom.CTkLabel(frame,text_color = textColor,text="0",width = cashCountWidth+60,font=cashCountLabelFont, bg_color=cashTotalBgColor)

        if index >= 9:
            denomination_lbl.grid(row=index-4,column=3,padx = (5,0))
            qty_entry.grid(row=index-4,column=4)
            product_results.grid(row=index-4,column=5)
        else:
            denomination_lbl.grid(row=index,column=0)
            qty_entry.grid(row=index,column=1)
            product_results.grid(row=index,column=2)

        CASH_ALL_INPUT_ENTRIES.append(qty_entry)
        CASH_PRODUCT_RESULTS_LBL.append(product_results)
    totalcashCountEntry = custom.CTkEntry(frame,text_color = textColor,width=200,font=finalResultEntryFont,placeholder_text="CASH COUNT",justify = "center")
    totalcashCountEntry.grid(row = 13,column= 0,pady=(10,5), columnspan = 6)
    totalcashCountEntry.insert(0,"0")

def tabView_Frame(settlementFrame):
    global tabview,cardTab,homeCreditTab,billEaseTab,formTab,bankTransferTab,expensesTab
    tabViewFrame = custom.CTkFrame(settlementFrame)
    tabViewFrame.pack(side = custom.BOTTOM)#

    tabview = custom.CTkTabview(tabViewFrame)
    tabview.pack()

    mystyle = ttk.Style()
    mystyle.configure("settlement.Treeview",rowheight=30,font=('Arial', 19, 'bold'))
    mystyle.layout("settlement.Treeview", [('settlement.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

    
    card = tabview.add("Card")
    homeCredit = tabview.add("HCredit")
    billEase = tabview.add("BillEase")
    form = tabview.add("Form")
    bankTransfer = tabview.add("BTrans")
    expenses = tabview.add("Expens")

    cardTab = Tabview_Window("#FFE699","#FFF2CC")
    homeCreditTab = Tabview_Window("#BDD7EE","#DDEBF7")
    billEaseTab = Tabview_Window("#C6E0B4","#E2EFDA")
    formTab = Tabview_Window("#CC99FF","#CCCCFF")
    bankTransferTab = Tabview_Window("#B4D6E0","#E2EBEE")
    expensesTab = Tabview_Window("#8DDBBB","#BFE4D4")

    cardTab.window(card)
    homeCreditTab.window(homeCredit)
    billEaseTab.window(billEase)
    formTab.window(form)
    bankTransferTab.window(bankTransfer)
    expensesTab.window(expenses)
def setTabView(e,tabview,tabName):
    tabview.set(tabName)
def finalResult_Frame(cashFinalFrame):
    global totalCardEntry,totalHomeCreditEntry,totalBillEaseEntry,totalBankTransferEntry,formEntry,totalExpensesEntry,totalcashCountEntry,totalSalesEntry,overOrLackingEntry,overOrLackingLabel,amountToDepositEntry

    finalResultFrame = custom.CTkFrame(cashFinalFrame, fg_color="transparent")
    finalResultFrame.pack(side = custom.BOTTOM)
    finalResultLabelFont = custom.CTkFont('Halvetica',23,"bold")
    finalResultEntryFont = custom.CTkFont('Halvetica',25)
    finalResultEntryWidth = 170

    totalSalesLabel = custom.CTkLabel(finalResultFrame, text= "TOTAL SALES" ,font=finalResultLabelFont)
    totalSalesLabel.grid(row = 0,column= 0,padx=(10,0),pady=(5,0))

    totalCardLabel = custom.CTkLabel(finalResultFrame, text= "CARD" ,font=finalResultLabelFont)
    totalCardLabel.grid(row = 1,column= 0,padx=(5,0),pady=(5,0))

    totalHomeCreditLabel = custom.CTkLabel(finalResultFrame, text= "HOME CREDIT" ,font=finalResultLabelFont)
    totalHomeCreditLabel.grid(row = 2,column= 0,padx=(5,0),pady=(5,0))

    totalBillEaseLabel = custom.CTkLabel(finalResultFrame, text= "BILLEASE" ,font=finalResultLabelFont)
    totalBillEaseLabel.grid(row = 0,column= 2,padx=(5,0),pady=(5,0))

    formLabel = custom.CTkLabel(finalResultFrame, text= "FORM 2307" ,font=finalResultLabelFont)
    formLabel.grid(row = 1,column= 2,padx=(5,0),pady=(5,0))

    bankTranferLabel = custom.CTkLabel(finalResultFrame, text= "BANK TRANS" ,font=finalResultLabelFont)
    bankTranferLabel.grid(row = 2,column= 2,padx=(5,0),pady=(5,0))

    totalExpensesLabel = custom.CTkLabel(finalResultFrame, text= "EXPENSES" ,font=finalResultLabelFont)
    totalExpensesLabel.grid(row = 3,column= 2,padx=(5,0),pady=(5,0))

    overOrLackingLabel = custom.CTkLabel(finalResultFrame, text= "NORMAL" ,font=finalResultLabelFont)
    overOrLackingLabel.grid(row = 3,column= 0,padx=(5,0),pady=(5,0))
    toolTip(overOrLackingLabel,"(TOTAL CASHCOUNT)-(AMOUNT TO DEPOSIT)")

    #entry

    totalSalesEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    totalSalesEntry.grid(row = 0,column= 1,pady=(5,0))
    totalSalesEntry.bind("<KeyRelease>",totalSalesPress)
    #totalSalesEntry.insert(0,"0")

    totalCardEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    totalCardEntry.grid(row = 1,column= 1,pady=(5,0))
    totalCardEntry.bind("<FocusIn>",lambda e : setTabView(e,tabview,"Card"))
    totalCardEntry.bind("<KeyRelease>",noInputNeeded)
    totalCardEntry.insert(0,"0")
    
    totalHomeCreditEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    totalHomeCreditEntry.grid(row = 2,column= 1,pady=(5,0))
    totalHomeCreditEntry.bind("<FocusIn>",lambda e : setTabView(e,tabview,"HCredit"))
    totalHomeCreditEntry.bind("<KeyRelease>",noInputNeeded)
    totalHomeCreditEntry.insert(0,"0")

    totalBillEaseEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    totalBillEaseEntry.grid(row = 0,column= 3,pady=(5,0),padx = (0,5))
    totalBillEaseEntry.bind("<FocusIn>",lambda e : setTabView(e,tabview,"BillEase"))
    totalBillEaseEntry.bind("<KeyRelease>",noInputNeeded)
    totalBillEaseEntry.insert(0,"0")

    formEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    formEntry.grid(row = 1,column= 3,pady=(5,0),padx = (0,5))
    formEntry.bind("<FocusIn>",lambda e : setTabView(e,tabview,"Form"))
    formEntry.bind("<KeyRelease>",noInputNeeded)
    formEntry.insert(0,"0")

    totalBankTransferEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    totalBankTransferEntry.grid(row = 2,column= 3,pady=(5,0),padx = (0,5))
    totalBankTransferEntry.bind("<FocusIn>",lambda e : setTabView(e,tabview,"BTrans"))
    totalBankTransferEntry.bind("<KeyRelease>",noInputNeeded)
    totalBankTransferEntry.insert(0,"0")

    totalExpensesEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    totalExpensesEntry.grid(row = 3,column= 3,pady=(5,0),padx = (0,5))
    totalExpensesEntry.bind("<FocusIn>",lambda e : setTabView(e,tabview,"Expens"))
    totalExpensesEntry.bind("<KeyRelease>",noInputNeeded)
    totalExpensesEntry.insert(0,"0")

    overOrLackingEntry = custom.CTkEntry(finalResultFrame,width=finalResultEntryWidth,font=finalResultEntryFont)
    overOrLackingEntry.grid(row = 3,column= 1,pady=(5,0))
    overOrLackingEntry.bind("<KeyRelease>",noInputNeeded)
    overOrLackingEntry.insert(0,"0")
    toolTip(overOrLackingEntry,"(TOTAL CASHCOUNT)-(AMOUNT TO DEPOSIT)")

    amountToDepositLabel = custom.CTkLabel(finalResultFrame,height=60,bg_color="red", text= "AMOUNT TO DEPOSIT",width=350,font=custom.CTkFont('Halvetica',30,"bold"))
    amountToDepositLabel.grid(row = 7,column= 0,padx = (5,0),pady=5,columnspan = 2)
    toolTip(amountToDepositLabel,"(TOTAL SALES)-(CARD+HOMECREDIT+FORM2307+BANKTRANS+EXPENSES)")

    amountToDepositEntry = custom.CTkEntry(finalResultFrame,width = 330,border_color="red",fg_color="white",text_color="black",font=custom.CTkFont('Halvetica',35,"bold"))
    amountToDepositEntry.grid(row = 7,column= 2,padx = 5,pady=(5,0),columnspan = 6)
    amountToDepositEntry.bind("<KeyRelease>",noInputNeeded)
    amountToDepositEntry.insert(0,"0")
    toolTip(amountToDepositEntry,"(TOTAL SALES)-(CARD+HOMECREDIT+FORM2307+BANKTRANS+EXPENSES)")

def buttons_Frame(buttonsFrame):
    button_Frame = custom.CTkFrame(buttonsFrame,fg_color="transparent")
    button_Frame.pack(side = custom.BOTTOM)

    clear_image = custom.CTkImage(light_image=Image.open("images/clear.png"),
                                    dark_image=Image.open("images/clear.png"),
                                    size=(24, 24))
    
    save_image = custom.CTkImage(light_image=Image.open("images/save.png"),
                                    dark_image=Image.open("images/save.png"),
                                    size=(24, 24))
    
    import_image = custom.CTkImage(light_image=Image.open("images/import.png"),
                                    dark_image=Image.open("images/import.png"),
                                    size=(24, 24))

    clear_btn = custom.CTkButton(button_Frame,text="",hover_color="#7a9af7",fg_color="white",width=1,image=clear_image,command=clear_data)#
    clear_btn.grid(row = 0,column = 0,padx = (5,0),pady = 10) 
    toolTip(clear_btn,"Clear")

    save_btn = custom.CTkButton(button_Frame,text="",hover_color="#7a9af7",fg_color="white",width=1,image=save_image,command=save_data)#
    save_btn.grid(row = 0,column = 1,padx = (5,0),pady = 10)
    toolTip(save_btn,"Save")

    import_btn = custom.CTkButton(button_Frame,text="",hover_color="#7a9af7",fg_color="white",width=1,image=import_image,command=import_data)#
    import_btn.grid(row = 0,column = 2,padx = (5,0),pady = 10)
    toolTip(import_btn,"Import saved file")

def settlement(settle_tab):
    global cash_finalResultFrame
    settlementFrame = custom.CTkFrame(settle_tab)
    settlementFrame.pack(expand = custom.TRUE,fill = custom.BOTH)
    #print(str(settlementFrame.winfo_height()) + "Height")

    cash_finalResultFrame = custom.CTkFrame(settlementFrame)
    cash_finalResultFrame.pack(side = custom.LEFT,padx = 5)

    button_tab_Frame = custom.CTkFrame(settlementFrame,fg_color ="transparent")
    button_tab_Frame.pack(side = custom.RIGHT,padx = 5)


    cash_Frame(cash_finalResultFrame)
    finalResult_Frame(cash_finalResultFrame)
    tabView_Frame(button_tab_Frame)
    buttons_Frame(button_tab_Frame)
    
def toolTip(widget,balloonMsg):
    toolTip = Hovertip(widget,balloonMsg,hover_delay = 100)

# settlement(root)
# root.mainloop()