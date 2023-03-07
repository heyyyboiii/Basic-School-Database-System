import pymongo
import tkinter as tk
from tkinter import *
from tkinter import messagebox

def teachStart():

    #Connects to the MongoDB database
    myClient = pymongo.MongoClient("localhost", 27017)
    myDatabase = myClient["enrollmentsystem"]
    myCollection = myDatabase["teachers"]

    #Formats the grid accordingly (ID, Name, Email, Course)
    teachList = [["ID", "Teacher", "Department", "Contact"]]

    def callback(event):
        li=[]
        li=event.widget._values
        tID.set(teachList[li[1]][0])
        tName.set(teachList[li[1]][1])
        tDepartment.set(teachList[li[1]][2])
        tContact.set(teachList[li[1]][3])

    def filter():
        for label in window3.grid_slaves():
            if int(label.grid_info()["row"]) > 7:
                label.grid_forget()

        filterID = int(fID.get())
        idOption = str()
        teachList.clear()
        teachList.append(["ID", "Teacher", "Department", "Contact"])

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
        nameStart = f"^{startN.get()}"
        nameEnd = f"^{endN.get()}"
        mailStart = f"^{startD.get()}"
        courseStart = f"^{startC.get()}"
        teacherCursor = myCollection.aggregate(
            [
                {
                    "$match": {
                        "teachID": {idOption: filterID},
                        "$and": [
                            {"teachName": {"$regex": nameStart}},
                            {"teachName": {"$regex": nameEnd}},
                        ],
                        "teachDepartment": {"$regex": mailStart},
                        "teachContact": {"$regex": courseStart},
                    }
                }
            ]
        )

        for text_fromDB in teacherCursor:
            teachID = str(text_fromDB["teachID"])
            teachName = str(text_fromDB["teachName"].encode("utf-8").decode("utf-8"))
            teachDepartment = str(text_fromDB["teachDepartment"].encode("utf-8").decode("utf-8"))
            teachContact = str(text_fromDB["teachContact"].encode("utf-8").decode("utf-8"))
            teachList.append([teachID, teachName, teachDepartment, teachContact])
        
        for i in range(len(teachList)):
            for j in range(len(teachList[0])):
                studGrid = tk.Entry(window3, width = 20)
                studGrid.insert(tk.END, teachList[i][j])
                studGrid._values = studGrid.get(), i
                studGrid.grid(row = i + 8, column = j + 5)
                studGrid.bind("<Button-1>", callback)        


    #Creates the grid with all the entries in the database
    def createRecords(n):
        teachList.clear()
        teachList.append(["ID", "Teacher", "Department", "Contact"])
        cursor = myCollection.find({})
        for text_fromDB in cursor:
            teachID = str(text_fromDB["teachID"])
            teachName = str(text_fromDB["teachName"].encode("utf-8").decode("utf-8"))
            teachDepartment = str(text_fromDB["teachDepartment"].encode("utf-8").decode("utf-8"))
            teachContact = str(text_fromDB["teachContact"].encode("utf-8").decode("utf-8"))
            teachList.append([teachID, teachName, teachDepartment, teachContact])
        
        for i in range(len(teachList)):
            for j in range(len(teachList[0])):
                studGrid = tk.Entry(window3, width = 20)
                studGrid.insert(tk.END, teachList[i][j])
                studGrid._values = studGrid.get(), i
                studGrid.grid(row = i + 8, column = j + 5)
                studGrid.bind("<Button-1>", callback)
        
        if n==1:
            for label in window3.grid_slaves():
                if int(label.grid_info()["row"]) > 7:
                        label.grid_forget()

    #Message box that acts as confirmation for saving, updating, and deleting
    def messageBox(msg, titlebar):
        result = messagebox.askokcancel(title = titlebar, message = msg)
        return result

    #Function of the save button, saves the entries
    def save():
        x = messageBox("Save Record", "Record")
        if x == True:
            newID = myCollection.count_documents({})
        if newID != 0:
            newID = myCollection.find_one(sort = [("teachID", -1)])["teachID"]
        ID=newID+1
        tID.set(ID)
        myDictionary = {"teachID": ID, "teachName": teacherName.get(), "teachDepartment": teacherDepartment.get(), "teachContact": teacherContact.get()}
        myCollection.insert_one(myDictionary)
        createRecords(1)
        createRecords(0)

    #Function of the delete button, deletes the entries
    def delete():
        x = messageBox("Delete?", "Record")
        if x == True:
            deleteFunction = {"teachID": int(float(teacherID.get()))}
            myCollection.delete_one(deleteFunction)
            createRecords(1)
            createRecords(0)
    
    #Function of the update button, updates the entries
    def update():
        x = messageBox("Update?", "Record")
        if x == True:
            updateFunction = {"teachID": int(float(teacherID.get()))}
            newValues = {"$set": {"teachName": teacherName.get()}}
            myCollection.update_one(updateFunction, newValues)
            newValues = {"$set": {"teachDepartment": teacherDepartment.get()}}
            myCollection.update_one(updateFunction, newValues)
            newValues = {"$set": {"teachContact": teacherContact.get()}}
            myCollection.update_one(updateFunction, newValues)  
            createRecords(1)
            createRecords(0)      

    #Starts the tkinter GUI
    window3 = tk.Tk()
    window3.title("Teachers Form")
    window3.geometry("1050x400")
    window3.configure(bg = "#EDE9E8")

    #The labels and entries of the GUI 
    label = tk.Label(window3, text = "Teachers Enrollment Form", width = 30, height = 1, bg = "gray", anchor = "center")
    label.config(font=("Montserrat, 14"))
    label.grid(column=2, row=1)

    label = tk.Label(window3, text="Teacher ID:", width = 15, height=1, bg="gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 2)
    tID = tk.IntVar(window3)
    teacherID = tk.Entry(window3, textvariable = tID)
    teacherID.grid(column = 2, row = 2)
    teacherID.configure(state=tk.DISABLED)

    label = tk.Label(window3, text = "Teacher Name:", width = 20, height = 1, bg = "gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 3)
    tName = tk.StringVar(window3)
    teacherName = tk.Entry(window3, textvariable = tName)
    teacherName.grid(column = 2, row = 3)

    label = tk.Label(window3, text="Teacher Department", width = 20, height = 1, bg = "gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 4)
    tDepartment = tk.StringVar(window3)
    teacherDepartment = tk.Entry(window3, textvariable = tDepartment)
    teacherDepartment.grid(column = 2, row = 4)

    label = tk.Label(window3, text="Teacher Contact", width = 20, height = 1, bg = "gray")
    label.config(font = ("Montserrat, 10"))
    label.grid(column = 1, row = 5)
    tContact = tk.StringVar(window3)
    teacherContact = tk.Entry(window3, textvariable = tContact)
    teacherContact.grid(column = 2, row = 5)

    createRecords(0)

    #Save, Update, and Delete Buttons
    saveButton = tk.Button(master = window3, text = "Save", command = save)
    saveButton.grid(column = 1, row = 6)
    deleteButton = tk.Button(master = window3, text = "Delete", command = delete)
    deleteButton.grid(column = 2, row = 6)
    updateButton = tk.Button(master = window3, text = "Update", command = update)
    updateButton.grid(column = 3, row = 6)
    filterButton = tk.Button(master = window3, text = "Filter", command = filter)
    filterButton.grid(column = 4, row = 4)

    #Filter
    label = tk.Label(window3, text="ID Filter", width = 15, height = 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 5, row = 1)
    fID = tk.StringVar(window3)
    filterTeacherID = tk.Entry(window3, textvariable=fID)
    filterTeacherID.grid(column = 5, row = 2)
    selectedValue = tk.StringVar(window3)
    dropdownMenu = tk.OptionMenu(window3, selectedValue, '>', '>=', '<', '<=', '!=', '=')
    dropdownMenu.grid(column = 4, row = 2)
    selectedValue.set('>')

    label = tk.Label(window3, text="Name Start", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 6, row = 1)
    startN = tk.StringVar(window3)
    startName = tk.Entry(window3, textvariable=startN)
    startName.grid(column = 6, row = 2)

    label = tk.Label(window3, text="Name End", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 6, row = 3)
    endN = tk.StringVar(window3)
    endName = tk.Entry(window3, textvariable=endN)
    endName.grid(column = 6, row = 4)

    label = tk.Label(window3, text="Department", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 7, row = 1)
    startD = tk.StringVar(window3)
    startDepartment = tk.Entry(window3, textvariable=startD)
    startDepartment.grid(column = 7, row = 2)

    label = tk.Label(window3, text="Contact", width = 15, height= 1, bg = "gray")
    label.config(font= ("Montserrat, 10"))
    label.grid(column = 8, row = 1)
    startC = tk.StringVar(window3)
    fContact = tk.Entry(window3, textvariable=startC)
    fContact.grid(column = 8, row = 2)

    #Makes it that the GUI work
    window3 = mainloop()