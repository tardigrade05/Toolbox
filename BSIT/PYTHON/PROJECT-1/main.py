from tkinter import *

#Set to global to use inside and outside other functions
global PICK_CHANCE,ARRAY_SIZE,COUNTER,ARRAY_ELEMENTS

#Set to Initial Value
PICK_CHANCE = 1
ARRAY_SIZE = 0
COUNTER = 0
ARRAY_ELEMENTS = []

#Set Main Window
root = Tk()
root.title('Project-1')

#Add Funtionality
def add_func(arraySize_entry,arrayIndex_entry):
    #Set to global to use inside and outside other functions
    global PICK_CHANCE,ARRAY_SIZE,COUNTER,ARRAY_ELEMENTS

    #To Just pick ARRAY_SIZE ONCE....
    if PICK_CHANCE>0:
        ARRAY_SIZE = int(arraySize_entry.get())
        PICK_CHANCE = PICK_CHANCE-1

    #Adding element/s depends on set ARRAY_SIZE
    if COUNTER<ARRAY_SIZE:
        ARRAY_ELEMENTS.append(arrayIndex_entry.get())
        COUNTER = COUNTER+1

        #Configuring text every index
        if COUNTER !=ARRAY_SIZE:
            arrayIndex_lbl.configure(text=f'Enter array[{COUNTER}]')
        
    #print(ARRAY_ELEMENTS)
    arraySize_entry.delete(0,'end')
    arraySize_entry.insert(0,str(ARRAY_SIZE))
    arrayIndex_entry.delete(0,'end')

#Show Funtionality
def show_func():
    global ARRAY_ELEMENTS
    text = ''

    #Loop Through items inside the array then add comma, e.g. 1,2,3,4,5,
    for item in ARRAY_ELEMENTS:
        text = text+item+","

    #Removing comma on the last element
    text = text[0:-1]

    result_lbl.configure(text=f'Results: [{text}]')

#Clear Funtionality
def clear_fields(arraySize_entry,arrayIndex_entry):
    #Return to the default values
    global PICK_CHANCE,ARRAY_SIZE,COUNTER,ARRAY_ELEMENTS
    PICK_CHANCE = 1
    ARRAY_SIZE = 0
    COUNTER = 0
    ARRAY_ELEMENTS = []

    arrayIndex_lbl.configure(text=f'Enter array[0]')
    arraySize_entry.delete(0, 'end')
    arrayIndex_entry.delete(0, 'end')
    


#Labels
Label(root, text='Enter array size').grid(row=0,column=0)

arrayIndex_lbl = Label(root, text=f'Enter array[{COUNTER}]')
arrayIndex_lbl.grid(row=1,column=0)

#Entries
arraySize_entry = Entry(root, width=15)
arraySize_entry.grid(row=0,column=1, padx=10)

arrayIndex_entry = Entry(root, width=15)
arrayIndex_entry.grid(row=1,column=1, padx=10)

#Buttons
add_btn = Button(root,text='Add', command=lambda:add_func(arraySize_entry,arrayIndex_entry))
add_btn.grid(row=2,column=0, pady=10)

show_btn = Button(root,text='Show', command= show_func)
show_btn.grid(row=2,column=1, pady=10)

exit_btn = Button(root,text='Exit', command=root.destroy)
exit_btn.grid(row=3,column=0)

clear_btn = Button(root,text='Clear', command= lambda:clear_fields(arraySize_entry,arrayIndex_entry))
clear_btn.grid(row=3,column=1)

result_lbl = Label(root, text="")
result_lbl.grid(row = 4, column=0, pady=5, columnspan=3)

root.mainloop()