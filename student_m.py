from tkinter import * 
from tkinter import messagebox
import sqlite3

conn=sqlite3.connect("students_database")
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student(
    name TEXT,
    roll INT PRIMARY KEY,
    course TEXT)

""")

conn.commit()


def Add_student():
    if name_var.get()=="" or roll_var.get()=="" or course_var.get()=="":
        messagebox.showerror("Error","All Fields Must Be Filled")
        return
    if not roll_var.get().isdigit():
        messagebox.showerror("Error","Roll number must be an integer")
        return

    conn= sqlite3.connect("students_database")
    cursor=conn.cursor()

    cursor.execute("INSERT INTO student(name,roll,course) VALUES(?,?,?)",
                   (
                       name_var.get(),
                       roll_var.get(),
                       course_var.get()
                   )
                   )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success","Successfully Inserted")
    clear_fields()
    show_students()

def show_students():
    student_list.delete(0,END)

    conn=sqlite3.connect("students_database")
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM student")

    row= cursor.fetchall()

    for rows in row:
        student_list.insert(END,rows)

    conn.close()

def update_student():
    try:
        selected = student_list.get(student_list.curselection())
        student_roll = selected[1]

        conn= sqlite3.connect("students_database")
        cursor= conn.cursor()

        cursor.execute("""UPDATE student Set name=?, roll=?, course=? WHERE roll=?""",( name_var.get(), roll_var.get(),course_var.get(),student_roll))

        conn.commit()
        conn.close()

        messagebox.showinfo("success","your data is updated") 


        clear_fields()
        show_students()

    except Exception as e:
        messagebox.showerror("Error",str(e))

def delete_student():
    try:
        selected = student_list.get(student_list.curselection())
        student_roll=selected[1]

        conn = sqlite3.connect("students_database")
        cursor= conn.cursor()

        cursor.execute("DELETE FROM student WHERE roll=?",(student_roll,))

        conn.commit()
        conn.close()

        messagebox.showinfo("success","student data deleted successfully")
        show_students()

    except:
        messagebox.showerror("error","select student first")




        
def clear_fields():
    name_var.set("")
    roll_var.set("")
    course_var.set("")


def select_students(event):
    try:
        selected =student_list.get(student_list.curselection())

        name_var.set(selected[0])
        roll_var.set(selected[1])
        course_var.set(selected[2])

    except Exception as e:
        messagebox.showerror("Error",str(e) )

 
root= Tk()
root.title("student management table")
root.geometry("700x600")

name_var=StringVar()
roll_var=StringVar()   
course_var=StringVar()

title= Label(
    root,
    text="student management system",
    font=("arial",20)
)

title.pack()

Label(root,text="student name",font=("arial",20)).pack()
Entry(root,width=30,textvariable=name_var).pack()

Label(root,text="Roll number",font=("arial",20)).pack()
Entry(root,width=30,textvariable=roll_var).pack()

Label(root,text="course",font=("arial",20)).pack()
Entry(root,width=30,textvariable=course_var).pack()

Frame1= Frame(root)
Frame1.pack()

Button(Frame1,text="Add student",command=Add_student).grid(row=0,column=0)
Button(Frame1,text="Clear Fields",command=clear_fields).grid(row=0,column=1)
Button(Frame1,text="Update Data",command=update_student).grid(row=0,column=2)
Button(Frame1,text="Delete student",command=delete_student).grid(row=0,column=3)

student_list= Listbox(root,width=90,height=30)
student_list.pack()

student_list.bind("<<ListboxSelect>>", select_students)

show_students()

root.mainloop()