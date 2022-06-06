from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector 
import re
import main

class mainframe(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.sort_ch = StringVar()
        self.stud_num = StringVar()
        self.stud_name = StringVar()
        self.stud_course = StringVar()
        self.stud_year = StringVar()
        self.stud_data = []
        self.option = 1
        self.id_num = ''
        self.year_lvl = StringVar()
        self.substring = ''
        self.sort_option =''

    #Create Database if it does not exist
        mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000")
        mycursor = mysqldb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS attendance")
        mysqldb.close()

    #Create table for courses
        mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "attendance")
        mycursor = mysqldb.cursor()
        mycursor.execute("SHOW TABLES LIKE 'courses'")
        result = mycursor.fetchone()
        if result:
            # there is a table named "tableName"
            print('there are tables')
            pass
        else:
             # there are no tables named "tableName"
            mycursor.execute("CREATE TABLE courses(course_code CHAR(10) NOT NULL,course_name VARCHAR(50), PRIMARY KEY (course_code))")
            print('no tables')
            # populate table
            mycursor.execute("INSERT INTO courses (course_code, course_name) VALUES ('BSCS','BS Computer Science')")
            mycursor.execute("INSERT INTO courses (course_code, course_name) VALUES ('BSBIO','BS Biology')")
            mycursor.execute("INSERT INTO courses (course_code, course_name) VALUES ('BSEE','BS Electrical Engineering')")
            mycursor.execute("INSERT INTO courses (course_code, course_name) VALUES ('BSME','BS Mechanical Engineering')")
            mycursor.execute("INSERT INTO courses (course_code, course_name) VALUES ('BSSTAT','BS Statistics')")
            mysqldb.commit()
        mysqldb.close()

    #Create table for students
        mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "attendance")
        mycursor = mysqldb.cursor()
        mycursor.execute("SHOW TABLES LIKE 'student'")
        result = mycursor.fetchone()
        if result:
            # there is a table named "tableName"
            print('there are tables')
            pass
        else:
             # there are no tables named "tableName"
            mycursor.execute("CREATE TABLE student(id CHAR(10) NOT NULL,name VARCHAR(100) NOT NULL, course_code CHAR(10) NOT NULL, year CHAR(10) NOT NULL, PRIMARY KEY (id))")
            print('no tables')
        mysqldb.close()


    #Frame For student Information
        self.stud_form = Frame(master, width = 420, height = 485, highlightthickness = 2)
        self.stud_form.grid(row = 3 , column = 8, sticky = 'nEw', padx = 10, pady = 10, columnspan = 4)
        self.stud_form.grid_propagate(False)
        self.stud_form.config(background = 'slategray2', highlightbackground = 'white')

    #Scroll frame for student display
        self.sf = Frame(master, width=1200, height=480, bg = 'yellow')
        self.sf.grid(row = 3, rowspan = 6,column = 0, columnspan = 8, sticky = "nsew", padx = 15, pady = 7)
        self.sf.columnconfigure(0, weight = 1)

    #Treeview style
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=2, highlightbackground = 'Black', bd=0, font=('Segoe', 14))
        style.configure("mystyle.Treeview.Heading", font=('Segoe', 16,'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
    #Treeview for student display

        columns = ('ID number', 'Name', 'Course', 'Year level')
        self.tree = ttk.Treeview(self.sf, style = "mystyle.Treeview",columns = columns, show = 'headings')

        treescroll = Scrollbar(self.sf, orient = "vertical", command = self.tree.yview)
        treescroll.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = treescroll.set)
        self.tree.heading('ID number', text = 'ID number')
        self.tree.column('ID number', width = 130 )
        self.tree.heading('Name', text = 'Name')
        self.tree.column('Name', width = 300)
        self.tree.heading('Course', text = 'Course')
        self.tree.column('Course', width = 250  )
        self.tree.heading('Year level', text = 'Year')
        self.tree.column('Year level', width = 105)
        self.tree.bind('<<TreeviewSelect>>', self.GetValue)
        self.tree.pack(side = RIGHT, fill = BOTH)
        self.show()
        self.main()

    #Frame for options
        self.btn_frame = Frame(master, width = 600, height = 55, highlightthickness = 2)
        self.btn_frame.grid(row = 1, column = 4, sticky = 'Ew', padx = 30, pady = 10)
        self.btn_frame.grid_propagate(False)
        self.btn_frame.config(background = 'slategray2', highlightbackground = 'white')

    #Options
        sort_op = ["Alphabetical","Year"]
        self.sort_ch.set("Order by")
        self.sort_by = OptionMenu(self.btn_frame, self.sort_ch, *sort_op, command = self.sort)
        self.sort_by.grid(row=0, column = 5,pady =7,padx =7,sticky="e")   
        self.sort_by.config(width = 10)   
        Button(self.btn_frame, text='Clear Search', font = "Segoe 13", relief = GROOVE, bd = 0, command = self.show, fg ='black', height= 1, bg= 'white').grid(row = 0, column = 3,pady =7,padx =7,sticky="W")

    # Automatic clear entry in search box
        def on_click(event):
            event.widget.delete(0, END)
        default_text = StringVar()
        default_text.set('Enter ID# here(0000-0000)')

    #search in treeview in every input
        def treesearch(event):
            self.tv_search()

    #Search bar
        self.search_bar = Entry(self.btn_frame, font="Segoe 15", fg="Gray", bg="white", bd=0, justify=RIGHT, textvariable= default_text, width = 25,)
        self.search_bar.bind("<Button-1>", on_click)
        self.search_bar.bind("<KeyRelease>",treesearch)
        self.search_bar.grid(row = 0, column = 1, sticky = 'w',columnspan = 2) 
    #Labels and title
        self.disp_label = Label(self.btn_frame, text = 'Search:', font= 'Segoe 16', bg = 'slategray2', fg = 'white').grid(row = 0, column = 0,padx = 1, pady =5, sticky ='e')
        self.title_label = Label(master, text = 'Student Records', font = 'Segoe 35', bg = 'slategray2', fg = 'white').grid(row = 0, column = 1,sticky = 'ew', padx = 7, pady = 25, columnspan = 12)
        Button(master, text = "BACK", font = "Segoe 13", relief = RAISED, bd = 2, command = self.go_back, fg = 'Black', bg = "White", height = 1, width = 7).grid(row = 0, column = 0, pady = 5, padx = 10)

    def go_back(self):
        self.master.destroy()

    def main(self):
        for widgets in self.stud_form.winfo_children():
            widgets.destroy()
        Yrlvl_op = ["1",'2','3','4','5', 'Irregular']
        Courses = ["BSCS", "BSBIO","BSEE", "BSME","BSSTAT"]

        if self.option == 1:
            Button(self.stud_form, text="Save", font="Segoe 11", relief=GROOVE, bd=0, command=self.save_sql, fg="black", bg="white",height = 1, width = 5).grid(row=7, column = 1, pady =7,padx =2, sticky = 'e')      
            Button(self.stud_form, text="Cancel", font="Segoe 11", relief=GROOVE, bd=0, command=self.cancel, fg="black", bg="white",height = 1, width = 5).grid(row=7, column = 2, pady =7,padx =10)      

        if self.option == 2:
            Button(self.stud_form, text="Update", font="Segoe 11", relief=GROOVE, bd=0, command=self.update, fg="black", bg="white",height = 1, width = 5).grid(row=7, column = 1, pady =15,padx =2, sticky = 'nsew')      
            Button(self.stud_form, text="Cancel", font="Segoe 11", relief=GROOVE, bd=0, command=self.cancel, fg="black", bg="white",height = 1, width = 5).grid(row=7, column = 2, pady =15,padx =10 , sticky = 'nsew')  
            Button(self.stud_form, text="Delete", font="Segoe 11", relief=GROOVE, bd=0, command=self.delete, fg="black", bg="white",height = 1, width = 5).grid(row=7, column = 0, pady =15,padx =10, sticky = 'nsew')  

        #Labels and entry for Student Form
        self.label = Label(self.stud_form, text = '------------', fg= 'slategray2' , font =('Segoe 18'), bg = 'slategray2').grid(row= 0, column = 0, columnspan = 5, pady = 30, sticky = 'nsew')
        self.label = Label(self.stud_form, text = 'Student Information', fg= 'white' , font =('Segoe 18'), bg = 'slategray2').grid(row= 0, column = 1, columnspan = 5, pady = 30, sticky = 'nsw')
        self.id_lbl = Label(self.stud_form,text = 'ID number :', fg = 'white', font = 'Segoe 15', bg = 'slategray2').grid(row = 2, column = 0, sticky = 'sew', padx = 3, pady = 13)
        self.name_lbl = Label(self.stud_form,text = 'Name :', fg = 'white', font = 'Segoe 15', bg = 'slategray2').grid(row = 3, column = 0, sticky = 'sew', padx = 3, pady = 13)
        self.course_lbl = Label(self.stud_form,text = 'Course :', fg = 'white', font = 'Segoe 15', bg = 'slategray2').grid(row = 4, column = 0, sticky = 'sew', padx = 3, pady = 13) 
        self.year_lbl = Label(self.stud_form,text = 'Year :', fg = 'white', font = 'Segoe 15', bg = 'slategray2').grid(row = 5, column = 0, sticky = 'sew', padx = 3, pady = 13)
    
        self.id_bar = Entry (self.stud_form, textvariable = self.stud_num, font = 'Segoe 15', bg = 'white', justify = LEFT)       
        self.name_bar = Entry (self.stud_form,textvariable = self.stud_name, font = 'Segoe 15', bg = 'white', justify = LEFT)
        self.course_bar = OptionMenu(self.stud_form,self.stud_course,*Courses)
        self.year_bar = OptionMenu(self.stud_form, self.year_lvl, *Yrlvl_op)

        self.id_bar.grid(row=2, column = 1 , pady =13, padx = 3, sticky = 'sW', columnspan = 2)       
        self.name_bar.grid(row = 3, column= 1, pady= 13, padx = 3, sticky = 'sw',columnspan = 2)       
        self.course_bar.grid(row = 4, column= 1, pady= 13, padx = 3, sticky = 'sw',columnspan = 2) 
        self.course_bar.config(width = 10)
        self.year_bar.grid(row = 5, column= 1, pady= 13, padx = 3, sticky = 'sw',columnspan = 2)
        self.year_bar.config(width = 10)

    def GetValue(self,event):
        self.clear_entry()
        self.option = 2
        self.row_id = self.tree.selection()[0]
        select = self.tree.set(self.row_id)
        self.id_bar.insert(0, select['ID number'])
        temp_id = select['ID number']
        self.name_bar.insert(0, select['Name'])
        temp_course = select['Course']
        mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="attendance")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT course_code FROM courses WHERE course_name LIKE %s ",( "%" +temp_course+"%",))
        records = mycursor.fetchone()
        self.stud_course.set(records[0])
        print(records[0])
        self.year_lvl.set(select['Year level'])
        self.main()

    def clear_entry(self):
        if self.option == 3:
            self.option = 1
            self.main()
        else:
            self.id_bar.delete(0,END)
            self.name_bar.delete(0,END)
            self.stud_course.set(None)
            self.year_lvl.set(None)

    def cancel(self):
        self.id_num = ''
        self.clear_entry()
        self.clear_tree()
        self.show()
        self.search_bar.delete(0,END)
        for widgets in self.stud_form.winfo_children():
            widgets.destroy()
        self.option = 1
        self.main()

    def retrieve_data(self):
        self.num = self.stud_num.get()
        self.name = self.stud_name.get()
        self.course = self.stud_course.get()
        self.year = self.year_lvl.get()
        self.stud_data = [self.num, self.name, self.course, self.year]
        if not re.match('^[0-9]{4}-[0-9]{4}$', self.stud_data[0]):
            messagebox.showerror('Invalid Input','ID number is invalid. Must be in format 0000-0000')
            return False
        for data in self.stud_data:
            if len(data)==0 or data == 'None':
                messagebox.showerror('Missing Fields', "One of the required field is empty; please check your input" )
                return False

    def save_sql(self):
        
        if self.retrieve_data() == False:
            print ('False save')
            return
        mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="attendance")
        mycursor=mysqldb.cursor()

        try:
           sql = "INSERT INTO  student (id,name,year,course_code) VALUES (%s, %s, %s, %s)"
           val = (self.num, self.name,self.year, self.course)
           mycursor.execute(sql, val)
           mysqldb.commit()
           lastid = mycursor.lastrowid
           messagebox.showinfo("information", "Student Added successfully...")
           self.clear_entry()

        except Exception as e:
           print(e)
           messagebox.showinfo("Error" ,e)
           mysqldb.rollback()
           mysqldb.close()
        self.clear_tree()
        self.show()

    def update(self):
        
        if self.retrieve_data() == False:
            print ("False update")
            return
        mysqldb = mysql.connector.connect(host = "localhost", user = "root", password = "Beleta000", database = "attendance")
        mycursor = mysqldb.cursor()

        try:
           sql = "Update  student set name= %s,year= %s, course_code = %s where id= %s"
           val = (self.name, self.year, self.course,self.num )
           mycursor.execute(sql, val)
           mysqldb.commit()
           lastid = mycursor.lastrowid
           messagebox.showinfo("information", "Record Updated successfully...")
           self.clear_entry()
    
        except Exception as e:
           print(e)
           messagebox.showinfo("Error" ,e)
           mysqldb.rollback()
           mysqldb.close()
        self.clear_tree()
        self.show()

    def delete(self):
        answer = messagebox.askquestion("delete?", "Are you sure you want to remove student from the database?")
        if answer == 'yes':
            pass
        else:
            return

        self.num = self.stud_num.get()
        mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="attendance")
        mycursor=mysqldb.cursor()

        try:
           sql = "delete from student where id = %s"
           val = (self.num,)
           mycursor.execute(sql, val)
           mysqldb.commit()
           lastid = mycursor.lastrowid
           messagebox.showinfo("Status", "Record Deleted successfully...")

           self.clear_entry()
           self.clear_tree()
           self.show()

        except Exception as e:

           print(e)
           messagebox.showinfo("Error" ,e)
           mysqldb.rollback()
           mysqldb.close()
           

    def show(self):
        self.clear_tree()

        mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="attendance")
        mycursor = mysqldb.cursor()

        if self.sort_option == "Alphabetical":
            query = (""" SELECT student.id,student.name,courses.course_name, student.year FROM student INNER JOIN courses ON student.course_code = courses.course_code ORDER BY name """)

        elif self.sort_option == "Year":
            query =("""SELECT student.id,student.name,courses.course_name, student.year FROM student INNER JOIN courses ON student.course_code = courses.course_code ORDER BY year""")

        else:
            query = "SELECT student.id,student.name,courses.course_name, student.year FROM student INNER JOIN courses ON student.course_code = courses.course_code"
        mycursor.execute(query)
        records = mycursor.fetchall()  

        for i, (id,name,course,year) in enumerate(records, start=1):
            self.tree.insert("", "end", values=(id,name, course,year))
            mysqldb.close()

    def sort(self, sort_option):
        self.sort_option = self.sort_ch.get()
        self.show()

    def clear_tree(self):
        for item  in self.tree.get_children():
            self.tree.delete(item)

    def tv_search(self):
        self.substring = self.search_bar.get()
        if self.substring == '':
            messagebox.showerror("Input error", "Please provide the needed information")
        for item in self.tree.get_children():
            self.tree.delete(item)
        mysqldb = mysql.connector.connect(host ="localhost",user = "root",password = "Beleta000",database = "attendance")
        mycursor= mysqldb.cursor()

        mycursor.execute("SELECT student.id,student.name,courses.course_name, student.year FROM student INNER JOIN courses ON student.course_code = courses.course_code WHERE id LIKE %s ",( "%" +self.substring+"%",))
        records = mycursor.fetchall()
        for i, (id, name, course,year) in enumerate(records, start =1):
            self.tree.insert("", "end", values = (id,name, course, year))
            mysqldb.close()
        self.selected = self.tree.get_children()[0]
        self.tree.selection_set(self.selected) 
        self.tree.yview_moveto(0)

class SIS(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the window properties
        self.title("Student Information System")
        self.state('zoomed')
        self.configure(bg = 'slategray2')
        mainframe(self).grid()


if __name__ == '__main__':
    app = SIS()
    app.mainloop()
