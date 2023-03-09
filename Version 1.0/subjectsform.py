import pymongo
import tkinter as tk
from tkinter import *
from tkinter import messagebox

def subStart():

    #Connects to the MongoDB database
    myClient = pymongo.MongoClient("localhost", 27017)
    myDatabase = myClient["enrollmentsystem"]
    myCollection = myDatabase["subjects"]
    
    #Formats the grid accordingly (ID, Name, Email, Course)
    subList = [["ID", "Code", "Description", "Unit", "Schedule"]]

    def callback(event):
        li=list()
        li=event.widget._values
        suID.set(subList[li[1]][0])
        sCode.set(subList[li[1]][1])
        sDescription.set(subList[li[1]][2])
        sUnits.set(subList[li[1]][3])
        sSchedule.set(subList[li[1]][4])

    def filter():
        for label in window2.grid_slaves():
            if int(label.grid_info()["row"]) > 7:
                label.grid_forget()

        filterID = fID.get()
        idOption = str()
        unitOption = str()
        subList.clear()
        subList.append(["ID", "Code", "Description", "Unit", "Schedule"])

        if selectedValue.get() == ">":
            idOption = "$gt"
        elif selectedValue.get() == ">=":
            idOption = "$gte"
        elif selectedValue.get() == "<":
            idOption = "$lt"
        elif selectedValue.get() == "<=":
            idOption = "$lte"
        elif selectedValue.get() == "!=":
            idOption = "$ne"
        elif selectedValue.get() == "=":
            idOption = "$eq"

        if startU.get() == 0:
            unitOption = "$gt"
        elif startU.get() > 0:
            unitOption = "$eq"
        Code = f"^{startC.get()}"
        Desc = f"^{startD.get()}"
        Unit = startU.get()
        Sched = f"^{startS.get()}"  
        print(filterID)
        print(Code)
        print(Desc)
        print(Unit)
        print(Sched)
        subjectsCursor = myCollection.aggregate(
            [
                {
                    "$match": {
                        "subID": {idOption: filterID},
                        "subCode": {"$regex": Code},
                        "subDescription": {"$regex": Desc},
                        "subUnit": {unitOption: Unit},
                        "subSchedule": {"$regex": Sched},
                    }
                }
            ]
        )

        for text_fromDB in subjectsCursor:
            subID = str(text_fromDB["subID"])
            subCode = str(text_fromDB["subCode"].encode("utf-8").decode("utf-8"))
            subDescription = str(text_fromDB["subDescription"].encode("utf-8").decode("utf-8"))
            subUnit = str(text_fromDB["subUnit"])
            subSchedule = str(text_fromDB["subSchedule"].encode("utf-8").decode("utf-8"))
            subList.append([subID, subCode, subDescription, subUnit, subSchedule])
            print(text_fromDB)

        for i in range(len(subList)):
            for j in range(len(subList[0])):
                subGrid = tk.Entry(window2, width = 20)
                subGrid.insert(tk.END, subList[i][j])
                subGrid._values = subGrid.get(), i
                subGrid.grid(row = i + 9, column = j + 5)
                subGrid.bind("<Button-1>", callback)  



    #Creates the grid with all the entries in the database
    def createRecords(n):
        subList.clear()
        subList.append(["ID", "Code", "Description", "Unit", "Schedule"])
        cursorSub = myCollection.find({})
        for text_fromDB in cursorSub:
            subID = str(text_fromDB["subID"])
            subCode = str(text_fromDB["subCode"].encode("utf-8").decode("utf-8"))
            subDescription = str(text_fromDB["subDescription"].encode("utf-8").decode("utf-8"))
            subUnit = str(text_fromDB["subUnit"])
            subSchedule = str(text_fromDB["subSchedule"].encode("utf-8").decode("utf-8"))
            subList.append([subID, subCode, subDescription, subUnit, subSchedule])
        
        for i in range(len(subList)):
            for j in range(len(subList[0])):
                subGrid = tk.Entry(window2, width = 20)
                subGrid.insert(tk.END, subList[i][j])
                subGrid._values = subGrid.get(), i
                subGrid.grid(row = i + 9, column = j + 5)
                subGrid.bind("<Button-1>", callback)
        
        if n==1:
            for label in window2.grid_slaves():
                if int(label.grid_info()["row"]) > 7:
                    label.grid_forget()

    #Message box that acts as confirmation for saving, updating, and deleting
    def messageBox(msg, titlebar):
        result=messagebox.askokcancel(title=titlebar, message=msg)
        return result
    
    #Function of the save button, saves the entries
    def save():
        x = messageBox("Save Record", "Record")
        if x==True:
            newid = myCollection.count_documents({})
        if newid > 0:
            newid = myCollection.find_one(sort = [("subID", -1)])["subID"]
        id = newid + 1
        suID.set(id)
        myDictionary = {"subID": id, "subCode": subjectCode.get(), "subDescription": subjectDescription.get(), "subUnit": int(subjectUnit.get()), "subSchedule": subjectSchedule.get()}
        myCollection.insert_one(myDictionary)
        createRecords(1)
        createRecords(0)

    #Function of the delete button, deletes the entries
    def delete():
        x = messageBox("Delete?", "Record")
        if x == True:
            deleteFunction = {"subID": int(subjectID.get())}
            myCollection.delete_one(deleteFunction)
        createRecords(1)
        createRecords(0)

    #Function of the update button, updates the entries
    def update():
        x = messageBox("Update?", "Record")
        if x == True:
            updateFunction = {"subID": int(subjectID.get())}
            newValues = {"$set": {"subCode": subjectCode.get()}}
            myCollection.update_one(updateFunction, newValues)
            newValues = {"$set": {"subDescription": subjectDescription.get()}}
            myCollection.update_one(updateFunction, newValues)
            newValues = {"$set": {"subUnit": int(float(subjectUnit.get()))}}
            myCollection.update_one(updateFunction, newValues)
            newValues = {"$set": {"subSchedule": subjectSchedule.get()}}
            myCollection.update_one(updateFunction, newValues)  
            createRecords(1)
            createRecords(0)

    #Starts the tkinter GUI
    window2 = tk.Tk()
    window2.title("Subjects Form")
    window2.geometry("1050x400")
    window2.configure(bg="#EDE9E8")

    #The labels and entries of the GUI 
    label = tk.Label(window2, text="Subjects Enrollment Form", width=30, height=1, bg="gray", anchor="center")
    label.config(font=("Montserrat", 14))
    label.grid(column=2, row=1)

    label = tk.Label(window2, text="Subject ID:", width = 10, height=1, bg="gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 2)
    suID = tk.IntVar(window2)
    subjectID = tk.Entry(window2, textvariable = suID)
    subjectID.grid(column = 2, row = 2)
    subjectID.configure(state=tk.DISABLED)

    label = tk.Label(window2, text = "Subject Code:", width = 15, height = 1, bg = "gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 3)
    sCode = tk.StringVar(window2)
    subjectCode = tk.Entry(window2, textvariable = sCode)
    subjectCode.grid(column = 2, row = 3)

    label = tk.Label(window2, text="Subject Description:", width = 15, height = 1, bg = "gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 4)
    sDescription = tk.StringVar(window2)
    subjectDescription = tk.Entry(window2, textvariable = sDescription)
    subjectDescription.grid(column = 2, row = 4)

    label = tk.Label(window2, text="Subject Unit:", width = 15, height = 1, bg = "gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 5)
    sUnits = tk.StringVar(window2)
    subjectUnit = tk.Entry(window2, textvariable = sUnits)
    subjectUnit.grid(column = 2, row = 5)

    label = tk.Label(window2, text="Subject Schedule:", width = 15, height = 1, bg = "gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 6)
    sSchedule = tk.StringVar(window2)
    subjectSchedule = tk.Entry(window2, textvariable = sSchedule)
    subjectSchedule.grid(column = 2, row = 6)

    createRecords(0)    

    #Save, Update, and Delete Buttons
    saveButton = tk.Button(master = window2, text = "Save", command = save)
    saveButton.grid(column = 1, row = 7)
    deleteButton = tk.Button(master = window2, text = "Delete", command = delete)
    deleteButton.grid(column = 2, row = 7)
    updateButton = tk.Button(master = window2, text = "Update", command = update)
    updateButton.grid(column = 3, row = 7)
    filterButton = tk.Button(master = window2, text = "Filter", command = filter)
    filterButton.grid(column = 4, row = 4)

    #Filter
    label = tk.Label(window2, text="ID Filter", width = 15, height = 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 5, row = 1)
    fID = tk.IntVar(window2)
    filterSubjectID = tk.Entry(window2, textvariable=fID)
    filterSubjectID.grid(column = 5, row = 2)
    selectedValue = tk.StringVar(window2)
    dropdownMenu = tk.OptionMenu(window2, selectedValue, '>', '>=', '<', '<=', '!=', '=')
    dropdownMenu.grid(column = 4, row = 2)
    selectedValue.set('>')

    label = tk.Label(window2, text="Code", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 6, row = 1)
    startC = tk.StringVar(window2)
    startCode = tk.Entry(window2, textvariable=startC)
    startCode.grid(column = 6, row = 2)

    label = tk.Label(window2, text="Description", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 7, row = 1)
    startD = tk.StringVar(window2)
    startDescription = tk.Entry(window2, textvariable=startD)
    startDescription.grid(column = 7, row = 2)

    label = tk.Label(window2, text="Unit", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 8, row = 1)
    startU = tk.IntVar(window2)
    startUnit = tk.Entry(window2, textvariable=startU)
    startUnit.grid(column = 8, row = 2)

    label = tk.Label(window2, text="Schedule", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 9, row = 1)
    startS = tk.StringVar(window2)
    startSchedule = tk.Entry(window2, textvariable=startS)
    startSchedule.grid(column = 9, row = 2)

    #Makes it that the GUI work
    window2 = mainloop()
