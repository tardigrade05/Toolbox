import customtkinter as custom
import settlement as SM
#import helperFunctions as help
from CTkMessagebox import CTkMessagebox
from idlelib.tooltip import Hovertip
import math

# root = custom.CTk()
# root.geometry("1020x650")

EXPONENT = 3
VALUE_DEALS_FLOAT = math.pow(10,EXPONENT)

def toolTip(widget,balloonMsg):
    toolTip = Hovertip(widget,balloonMsg,hover_delay = 100)

def roundFunction(value):
    valueSplit = str(value).split(".")
    try:
        if int(valueSplit[1][2])>=5:
            return math.ceil(value *100)/100
        else:
            return math.floor(value *100)/100
    except Exception as e:
        return value

def clearData():
    global totalSales_entry,lessVat_entry,netVal_entry,lessPwd_entry,totalDue_entry,lessWithHolding_entry,totalAmountDue_entry,vatable_entry,vatExempt_entry,zeroRated_entry,vat_lbl_entry,total_entry
    lessVat_entry.delete(0,"end")
    netVal_entry.delete(0,"end")
    lessPwd_entry.delete(0,"end")
    totalDue_entry.delete(0,"end")
    lessWithHolding_entry.delete(0,"end")
    totalAmountDue_entry.delete(0,"end")
    vatable_entry.delete(0,"end")
    vatExempt_entry.delete(0,"end")
    zeroRated_entry.delete(0,"end")
    vat_lbl_entry.delete(0,"end")
    total_entry.delete(0,"end")

def calculate(value):
    global optionPublicOrPrivate,lessWithHolding_lbl
    global totalSales_entry,lessVat_entry,netVal_entry,lessPwd_entry,totalDue_entry,lessWithHolding_entry,totalAmountDue_entry,vatable_entry,vatExempt_entry,zeroRated_entry,vat_lbl_entry,total_entry
    menu = {'Private':.01*VALUE_DEALS_FLOAT,'Public':.06*VALUE_DEALS_FLOAT,'NetVat':1.12*VALUE_DEALS_FLOAT,"LessVat":.12*VALUE_DEALS_FLOAT}

    clearData()
    toolTip(lessWithHolding_lbl,"(NET OF VAT/TOTAL)*(1%)") if optionPublicOrPrivate.get() == "Private" else toolTip(lessWithHolding_lbl,"(NET OF VAT/TOTAL)*(6%)")
    toolTip(lessWithHolding_entry,"(NET OF VAT/TOTAL)*(1%)") if optionPublicOrPrivate.get() == "Private" else toolTip(lessWithHolding_entry,"(NET OF VAT/TOTAL)*(6%)")

    netVal = (value/menu["NetVat"])*VALUE_DEALS_FLOAT
    lessVat = (netVal*menu["LessVat"])/VALUE_DEALS_FLOAT
    totalDue = value
    lessWithHolding = (netVal *menu[optionPublicOrPrivate.get()])/VALUE_DEALS_FLOAT
    totalAmountDue = value-lessWithHolding

    # print(f"{value} ... value before")
    # print(f"{lessVat} ... lessVat before")
    # print(f"{netVal} ... netVal before")

    # print(f"{value} ... value before")
    # print(f"{lessWithHolding} ... lessWithHolding before")
    # print(f"{totalAmountDue} ... totalAmountDue before")
    # print(f"{value} ... value before")

    netVal = roundFunction(netVal)
    lessWithHolding = roundFunction(lessWithHolding)

    lessVatShow = roundFunction(((value*VALUE_DEALS_FLOAT)-(netVal*VALUE_DEALS_FLOAT))/VALUE_DEALS_FLOAT)
    totalAmountDueShow = roundFunction(((value*VALUE_DEALS_FLOAT)-(lessWithHolding*VALUE_DEALS_FLOAT))/VALUE_DEALS_FLOAT)
    # #totalSales_entry.delete(0,"end")
    # #totalSales_entry.insert(0,str(help.addCommaNumber(SM.checkIfIntOrFloat(value))))

    lessVat_entry.insert(0,addComma(lessVatShow))
    
    netVal_entry.insert(0,addComma(netVal))

    # #lessPwd_entry.insert(0,roundValue(totalSales,2))

    totalDue_entry.insert(0,addComma(totalDue))
    lessWithHolding_entry.insert(0,addComma(lessWithHolding))
    totalAmountDue_entry.insert(0,addComma(totalAmountDueShow))

    # #vatable_entry.insert(0,roundValue(totalSales,2))
    # #vatExempt_entry.insert(0,roundValue(totalSales,2))
    # #zeroRated_entry.insert(0,roundValue(totalSales,2))
    # #vat_lbl_entry.insert(0,roundValue(totalSales,2))

    total_entry.insert(0,addComma(totalDue))

def keyPressReleased(e,totalSales_entry):
    container = 0
    print("Click")
    try:
        container=float(totalSales_entry.get())
    except ValueError:
        print("ValuError")
        if totalSales_entry.get() == "":
            container =0
        elif len(totalSales_entry.get())>=1 and totalSales_entry.get() != "":
            container = totalSales_entry.get()[0:-1].rstrip(" ")
            totalSales_entry.delete(0,"end")
            totalSales_entry.insert(0,container)
    
    calculate(float(container))

def calVatWindow(calVatTab):
    global privatePublicText,lessWithHolding_lbl
    global totalSales_entry,lessVat_entry,netVal_entry,lessPwd_entry,totalDue_entry,lessWithHolding_entry,totalAmountDue_entry,vatable_entry,vatExempt_entry,zeroRated_entry,vat_lbl_entry,total_entry
    global optionPublicOrPrivate,lessWithHolding_lbl
    paddingY = (5,0)
    labelFont = custom.CTkFont('Times',32,'bold')
    entryFont = custom.CTkFont('Halvetica',32)

    mainFrame = custom.CTkFrame(calVatTab)
    mainFrame.pack()
    
    totalSales_lbl=custom.CTkLabel(mainFrame,text="TOTAL SALES", font = labelFont,anchor="e", width = 300)
    totalSales_lbl.grid(row = 0, column = 0, padx=10, pady=paddingY)
    totalSales_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    totalSales_entry.grid(row = 0, column = 1, padx=10, pady=paddingY)
    totalSales_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))
    toolTip(totalSales_lbl,"Total Sales")
    toolTip(totalSales_entry,"Total Sales")

    optionPublicOrPrivate = custom.CTkComboBox(mainFrame,values=["Private",'Public'],width=100,command=lambda e:keyPressReleased(e,totalSales_entry))
    optionPublicOrPrivate.place(x=0,y = 12)
    
    lessVat_lbl=custom.CTkLabel(mainFrame,text="LESS: 12% VAT", font = labelFont)
    lessVat_lbl.grid(row = 1, column = 0, padx=10, pady = paddingY)
    lessVat_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    lessVat_entry.grid(row = 1, column = 1, padx=10, pady = paddingY)
    lessVat_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))
    toolTip(lessVat_lbl,"(TOTAL SALES) / (NET OF VAT/TOTAL)")
    toolTip(lessVat_entry,"(TOTAL SALES) / (NET OF VAT/TOTAL)")

    netVal_lbl=custom.CTkLabel(mainFrame,text="NET OF VAT/TOTAL", font = labelFont)
    netVal_lbl.grid(row = 2, column = 0, padx=10, pady=paddingY)
    netVal_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    netVal_entry.grid(row = 2, column = 1, padx=10, pady= paddingY)
    netVal_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))
    toolTip(netVal_lbl,"(TOTAL SALES) /(1.12)")
    toolTip(netVal_entry,"(TOTAL SALES) /(1.12)")

    lessPwd_lbl=custom.CTkLabel(mainFrame,text="LESS:SC/PWD DISC.", font = labelFont)
    lessPwd_lbl.grid(row = 3, column = 0, padx=10, pady=paddingY)
    lessPwd_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    lessPwd_entry.grid(row = 3, column = 1, padx=10, pady=paddingY)

    totalDue_lbl=custom.CTkLabel(mainFrame,text="TOTAL DUE", font = labelFont)
    totalDue_lbl.grid(row = 4, column = 0, padx=10, pady=paddingY)
    totalDue_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    totalDue_entry.grid(row = 4, column = 1, padx=10, pady=paddingY)
    totalDue_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))


    lessWithHolding_lbl=custom.CTkLabel(mainFrame,text="LESS: WITHHOLDING", font = labelFont)
    lessWithHolding_lbl.grid(row = 5, column = 0, padx=10, pady=paddingY)
    lessWithHolding_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    lessWithHolding_entry.grid(row = 5, column = 1, padx=10, pady=paddingY)
    lessWithHolding_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))

    totalAmountDue_lbl=custom.CTkLabel(mainFrame,text="TOTAL AMOUNT DUE", font = labelFont)
    totalAmountDue_lbl.grid(row = 6, column = 0, padx=10, pady=paddingY)
    totalAmountDue_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    totalAmountDue_entry.grid(row = 6, column = 1, padx=10, pady=paddingY)
    totalAmountDue_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))
    toolTip(totalAmountDue_lbl,"(TOTAL SALES)-(LESS: WITHHOLDING)")
    toolTip(totalAmountDue_entry,"(TOTAL SALES)-(LESS: WITHHOLDING)")

    vatable_lbl=custom.CTkLabel(mainFrame,text="VATABLE(V)", font = labelFont)
    vatable_lbl.grid(row = 7, column = 0, padx=10, pady=paddingY)
    vatable_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    vatable_entry.grid(row = 7, column = 1, padx=10, pady=paddingY)

    vatExempt_lbl=custom.CTkLabel(mainFrame,text="VAT-EXEMPT(E)", font = labelFont)
    vatExempt_lbl.grid(row = 8, column = 0, padx=10, pady=paddingY)
    vatExempt_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    vatExempt_entry.grid(row = 8, column = 1, padx=10, pady=paddingY)

    zeroRated_lbl=custom.CTkLabel(mainFrame,text="ZERO RATED(Z)", font = labelFont)
    zeroRated_lbl.grid(row = 9, column = 0, padx=10, pady=paddingY)
    zeroRated_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    zeroRated_entry.grid(row = 9, column = 1, padx=10, pady=paddingY)

    vat_lbl=custom.CTkLabel(mainFrame,text="VAT(12%)", font = labelFont)
    vat_lbl.grid(row = 10, column = 0, padx=10, pady=paddingY)
    vat_lbl_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    vat_lbl_entry.grid(row = 10, column = 1, padx=10, pady=paddingY) 

    total_lbl=custom.CTkLabel(mainFrame,text="TOTAL", font = labelFont)
    total_lbl.grid(row = 11, column = 0, padx=10, pady=(15,5))
    total_entry=custom.CTkEntry(mainFrame, font = entryFont , width = 300)
    total_entry.grid(row = 11, column = 1, padx=10, pady=(15,5))
    total_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))
    total_entry.bind("<KeyRelease>",lambda e:keyPressReleased(e,totalSales_entry))

    #disableState()

def addComma(value):
    return str(SM.addCommaNumber(SM.convertFloatOrInt(value)))
# calVatWindow(root)
# root.mainloop()