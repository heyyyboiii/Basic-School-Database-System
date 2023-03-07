import pymongo
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from subjectsform import subStart
from teachersform import teachStart

#Connects to the MongoDB database
myClient = pymongo.MongoClient("mongodb://localhost:27017/")
myDatabase = myClient["enrollmentsystem"]
myCollection = myDatabase["students"]

#Formats the grid accordingly (ID, Name, Email, Course)
studList = [["ID", "Name", "Email", "Course"]]

def callback(event):
    li=[]
    li=event.widget._values
    sID.set(studList[li[1]][0])
    sName.set(studList[li[1]][1])
    sEmail.set(studList[li[1]][2])
    sCourse.set(studList[li[1]][3])

def filter():
    for label in window.grid_slaves():
        if int(label.grid_info()["row"]) > 7:
            label.grid_forget()

    filterID = int(fID.get())
    idOption = str()
    studList.clear()
    studList.append(["ID", "Name", "Email", "Course"])

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
    mailStart = f"^{startE.get()}"
    courseStart = f"^{startC.get()}"
    studentsCursor = myCollection.aggregate(
        [
            {
                "$match": {
                    "studID": {idOption: filterID},
                    "$and": [
                        {"studName": {"$regex": nameStart}},
                        {"studName": {"$regex": nameEnd}},
                    ],
                    "studEmail": {"$regex": mailStart},
                    "studCourse": {"$regex": courseStart},
                }
            }
        ]
    )

    for text_fromDB in studentsCursor:
        studID = str(text_fromDB["studID"])
        studName = str(text_fromDB["studName"].encode("utf-8").decode("utf-8"))
        studEmail = str(text_fromDB["studEmail"].encode("utf-8").decode("utf-8"))
        studCourse = str(text_fromDB["studCourse"].encode("utf-8").decode("utf-8"))
        studList.append([studID, studName, studEmail, studCourse])
    
    for i in range(len(studList)):
        for j in range(len(studList[0])):
            studGrid = tk.Entry(window, width = 20)
            studGrid.insert(tk.END, studList[i][j])
            studGrid._values = studGrid.get(), i
            studGrid.grid(row = i + 8, column = j + 5)
            studGrid.bind("<Button-1>", callback)    

#Creates the grid with all the entries in the database
def createRecords(n):
    studList.clear()
    studList.append(["ID", "Name", "Email", "Course"])
    cursor = myCollection.find({})
    for text_fromDB in cursor:
        studID = str(text_fromDB["studID"])
        studName = str(text_fromDB["studName"].encode("utf-8").decode("utf-8"))
        studEmail = str(text_fromDB["studEmail"].encode("utf-8").decode("utf-8"))
        studCourse = str(text_fromDB["studCourse"].encode("utf-8").decode("utf-8"))
        studList.append([studID, studName, studEmail, studCourse])
    
    for i in range(len(studList)):
        for j in range(len(studList[0])):
            studGrid = tk.Entry(window, width = 20)
            studGrid.insert(tk.END, studList[i][j])
            studGrid._values = studGrid.get(), i
            studGrid.grid(row = i + 8, column = j + 5)
            studGrid.bind("<Button-1>", callback)
    
    if n==1:
        for label in window.grid_slaves():
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
            newID = myCollection.find_one(sort = [("studID", -1)])["studID"]
        ID = newID+1
        sID.set(ID)
        myDictionary = {"studID": int(float(studentID.get())), "studName": studentName.get(), "studEmail": studentEmail.get(), "studCourse": studentCourse.get()}
        myCollection.insert_one(myDictionary)
        createRecords(1)
        createRecords(0)

#Function of the delete button, deletes the entries
def delete():
    x = messageBox("Delete?", "Record")
    if x == True:
        deleteFunction = {"studID": int(float(studentID.get()))}
        myCollection.delete_one(deleteFunction)
        createRecords(1)
        createRecords(0)

#Function of the update button, updates the entries
def update():
    x = messageBox("Update?", "Record")
    if x == True:
        updateFunction = {"studID": int(float(studentID.get()))}
        newValues = {"$set": {"studName": studentName.get()}}
        myCollection.update_one(updateFunction, newValues)
        newValues = {"$set": {"studEmail": studentEmail.get()}}
        myCollection.update_one(updateFunction, newValues)
        newValues = {"$set": {"studCourse": studentCourse.get()}}
        myCollection.update_one(updateFunction, newValues)  
        createRecords(1)
        createRecords(0)  

#Starts the tkinter GUI
window = tk.Tk()
window.title("Students Form")
window.geometry("1920x1080")
window.configure(bg = "#EDE9E8")

#File Menu bar
menuBar = tk.Menu(window)
filemenu = tk.Menu(menuBar, tearoff = 0)
menuBar.add_cascade(label = "File", menu=filemenu)
filemenu.add_command(label = "Subjects", command = subStart)
filemenu.add_command(label = "Teachers", command = teachStart)
filemenu.add_separator()
filemenu.add_command(label = "Close", command = window.quit)

#Edit Menu bar
# editmenu = tk.Menu(menuBar, tearoff = 0)
# menuBar.add_cascade(label="Edit", menu=editmenu)
# editmenu.add_command(label="Undo", command=asf)
# editmenu.add_separator()
# editmenu.add_command(label="Cut", command=sdf)

window.config(menu = menuBar)

#The labels and entries of the GUI 
label = tk.Label(window, text = "Students Enrollment Form", width = 30, height = 1, bg = "gray", anchor = "center")
label.config(font=("Montserrat, 14"))
label.grid(column=2, row=1)

label = tk.Label(window, text="Student ID:", width = 10, height=1, bg="gray")
label.config(font = ("Montserrat, 10"))
label.grid(column = 1, row = 2)
sID = tk.StringVar()
studentID = tk.Entry(window, textvariable = sID)
studentID.grid(column = 2, row = 2)
studentID.configure(state=tk.DISABLED)

label = tk.Label(window, text = "Student Name:", width = 15, height = 1, bg = "gray")
label.config(font = ("Montserrat, 10"))
label.grid(column = 1, row = 3)
sName = tk.StringVar()
studentName = tk.Entry(window, textvariable = sName)
studentName.grid(column = 2, row = 3)

label = tk.Label(window, text="Student Email", width = 15, height = 1, bg = "gray")
label.config(font = ("Montserrat, 10"))
label.grid(column = 1, row = 4)
sEmail = tk.StringVar()
studentEmail = tk.Entry(window, textvariable = sEmail)
studentEmail.grid(column = 2, row = 4)

label = tk.Label(window, text="Student Course", width = 15, height = 1, bg = "gray")
label.config(font = ("Montserrat, 10"))
label.grid(column = 1, row = 5)
sCourse = tk.StringVar()
studentCourse = tk.Entry(window, textvariable = sCourse)
studentCourse.grid(column = 2, row = 5)

createRecords(0)

#Save, Update, and Delete Buttons
saveButton = tk.Button(text = "Save", command = save)
saveButton.grid(column = 1, row = 6)
deleteButton = tk.Button(text = "Delete", command = delete)
deleteButton.grid(column = 2, row = 6)
updateButton = tk.Button(text = "Update", command = update)
updateButton.grid(column = 3, row = 6)
filterButton = tk.Button(text = "Filter", command = filter)
filterButton.grid(column = 4, row = 4)

#Filter
label = tk.Label(window, text="ID Filter", width = 15, height = 1, bg = "gray")
label.config(font= ("Montserrat, 10"))
label.grid(column = 5, row = 1)
fID = tk.StringVar()
filterStudentID = tk.Entry(window, textvariable=fID)
filterStudentID.grid(column = 5, row = 2)
selectedValue = tk.StringVar()
dropdownMenu = tk.OptionMenu(window, selectedValue, '>', '>=', '<', '<=', '!=', '=')
dropdownMenu.grid(column = 4, row = 2)
selectedValue.set('>')

label = tk.Label(window, text="Name Start", width = 15, height= 1, bg = "gray")
label.config(font= ("Montserrat, 10"))
label.grid(column = 6, row = 1)
startN = tk.StringVar()
startName = tk.Entry(window, textvariable=startN)
startName.grid(column = 6, row = 2)

label = tk.Label(window, text="Name End", width = 15, height= 1, bg = "gray")
label.config(font= ("Montserrat, 10"))
label.grid(column = 6, row = 3)
endN = tk.StringVar()
endName = tk.Entry(window, textvariable=endN)
endName.grid(column = 6, row = 4)

label = tk.Label(window, text="Email", width = 15, height= 1, bg = "gray")
label.config(font= ("Montserrat, 10"))
label.grid(column = 7, row = 1)
startE = tk.StringVar()
startEmail = tk.Entry(window, textvariable=startE)
startEmail.grid(column = 7, row = 2)

label = tk.Label(window, text="Course", width = 15, height= 1, bg = "gray")
label.config(font= ("Montserrat, 10"))
label.grid(column = 8, row = 1)
startC = tk.StringVar()
fCourses = tk.Entry(window, textvariable=startC)
fCourses.grid(column = 8, row = 2)

#Makes it that the GUI work
window = mainloop()