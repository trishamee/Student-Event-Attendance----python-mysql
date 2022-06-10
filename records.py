from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector 
import re

class mainframe(Frame):
	def __init__(self, master, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		self.sort_ch = StringVar()
		self.gender_choice = StringVar()
		self.stud_num = StringVar()
		self.stud_name = StringVar()
		self.stud_course = StringVar()
		self.stud_year = StringVar()
		self.stud_gender = StringVar()
		self.stud_data = []
		self.option = 1
		self.id_num = ''
		self.year_lvl = StringVar()
		self.substring = ''
		self.sort_option =''
		self.course_name = ''
		self.course_id = ''
		self.Course =[]

	#Create Database if it does not exist
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000")
		mycursor = mysqldb.cursor()
		mycursor.execute("CREATE DATABASE IF NOT EXISTS app")
		mysqldb.close()

	#Create table for Course
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()
		#check if table already exists
		mycursor.execute("SHOW TABLES LIKE 'Course'")
		result = mycursor.fetchone()
		if result:
			# there is a table 
			pass
		else:
			 # there are no tables 
			mycursor.execute("CREATE TABLE Course(course_id CHAR(10) NOT NULL,course_name CHAR(60) NOT NULL, PRIMARY KEY (course_id))")
			#this none chuchu is para sa mu replace incase i delete ang certain Course
			mycursor.execute("INSERT INTO Course(course_id, course_name) VALUES ('None', 'None')")
			mysqldb.commit()
			lastid = mycursor.lastrowid
		mysqldb.close()

	#Create table for students
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()
		#check if table already exists
		mycursor.execute("SHOW TABLES LIKE 'Student'")
		result = mycursor.fetchone()
		if result:
			# there is a table 
			pass
		else:
			 # there are no tables
			mycursor.execute("CREATE TABLE Student(student_id VARCHAR(9) NOT NULL,student_name VARCHAR(60) NOT NULL, c_id CHAR(10) NOT NULL, year_level INT(1) NOT NULL, PRIMARY KEY (student_id), FOREIGN KEY (c_id) REFERENCES Course(course_id)")
		mysqldb.close()

	#Frame For student Information
	#located at the rightmost side
		self.stud_form = Frame(master, width = 420, height = 485, highlightthickness = 2)
		self.stud_form.grid(row = 3 , column = 8, sticky = 'nEw', padx = 10, pady = 10, columnspan = 4)
		self.stud_form.grid_propagate(False)
		self.stud_form.config(background = 'slategray2', highlightbackground = 'White')

	#Scroll frame for student display
	#Scroll frame for treeview
		self.sf = Frame(master, width=1100, height=480, bg = 'yellow')
		self.sf.grid(row = 3, rowspan = 6,column = 0, columnspan = 8, sticky = "nsew", padx = 7, pady = 7)
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
		self.tree.column('Name', width = 350)
		self.tree.heading('Course', text = 'Course')
		self.tree.column('Course', width = 310  )
		self.tree.heading('Year level', text = 'Year')
		self.tree.column('Year level', width = 105)
		self.tree.bind('<<TreeviewSelect>>', self.GetValue)
		self.tree.pack(side = LEFT, fill = BOTH)
		self.show()
		self.main()

	#Frame for options
	#Dre located tng mga search bar, sort button 
		self.btn_frame = Frame(master, width = 620, height = 55, highlightthickness = 2)
		self.btn_frame.grid(row = 1, column = 4, sticky = 'Ew', padx = 30, pady = 10)
		self.btn_frame.grid_propagate(False)
		self.btn_frame.config(background = 'slategray2', highlightbackground = 'White')

	#Options : Order by // Manage Course
		sort_op = ["Alphabetical","Year"]
		self.sort_ch.set("Order by")
		self.sort_by = OptionMenu(self.btn_frame, self.sort_ch, *sort_op, command = self.sort)
		self.sort_by.grid(row=0, column = 4,pady =7,padx =7,sticky="e")   
		self.sort_by.config(width = 10)   
		Button(self.btn_frame, text='Manage Courses', font = "Segoe 13", relief = GROOVE, bd = 0, command = self.manage_course, fg ='black', height= 1, bg= 'White').grid(row = 0, column = 3,pady =7,padx =7,sticky="W")

	# Automatic clear entry in search box (for binding)
		def on_click(event):
			event.widget.delete(0, END)
		default_text = StringVar()
		default_text.set('Enter ID# here(0000-0000)')

	#search in treeview in every input (for binding)
		def treesearch(event):
			self.tv_search()

	#Search bar
		self.search_bar = Entry(self.btn_frame, font="Segoe 15", fg="Gray", bg="white", bd=0, justify=RIGHT, textvariable= default_text, width = 25,)
		self.search_bar.bind("<Button-1>", on_click)
		self.search_bar.bind("<KeyRelease>",treesearch)
		self.search_bar.grid(row = 0, column = 1, sticky = 'w',columnspan = 2) 

	#Search label // app title // return button
		self.disp_label = Label(self.btn_frame, text = 'Search:', font= 'Segoe 16', bg = 'slategray2', fg = 'White').grid(row = 0, column = 0,padx = 1, pady =5, sticky ='e')
		self.title_label = Label(master, text = 'Student Information System', font = 'Segoe 35', bg = 'slategray2', fg = 'White').grid(row = 0, column = 1,sticky = 'ew', padx = 7, pady = 25, columnspan = 12)
		Button(master, text = "Return", font = "Segoe 15", relief = RAISED, bd = 3, command = self.back, fg = "black", bg="white", height = 1, width = 10). grid(row=0,column = 0, padx = 10)
	
	# widgets in student form
	# dre tng labels, buttons, and entry widgets nga naa sa rightmost frame
	def main(self):
		for widgets in self.stud_form.winfo_children():
			widgets.destroy()
		Yrlvl_op = ["1",'2','3','4','5']
		self.course_choices()

		#if user wants to save new student
		if self.option == 1:
			Button(self.stud_form, text="Save", font="Segoe 11", relief=GROOVE, bd=0, command=self.save_sql, fg="black", bg="White",height = 1, width = 5).grid(row=7, column = 1, pady =7,padx =2, sticky = 'e')      
			Button(self.stud_form, text="Cancel", font="Segoe 11", relief=GROOVE, bd=0, command=self.cancel, fg="black", bg="White",height = 1, width = 5).grid(row=7, column = 2, pady =7,padx =10)      

		#if user want to edit student record
		if self.option == 2:
			Button(self.stud_form, text="Update", font="Segoe 11", relief=GROOVE, bd=0, command=self.update, fg="black", bg="White",height = 1, width = 5).grid(row=7, column = 1, pady =15,padx =2, sticky = 'nsew')      
			Button(self.stud_form, text="Cancel", font="Segoe 11", relief=GROOVE, bd=0, command=self.cancel, fg="black", bg="White",height = 1, width = 5).grid(row=7, column = 2, pady =15,padx =10 , sticky = 'nsew')  
			Button(self.stud_form, text="Delete", font="Segoe 11", relief=GROOVE, bd=0, command=self.delete, fg="black", bg="White",height = 1, width = 5).grid(row=7, column = 0, pady =15,padx =10, sticky = 'nsew')  

		#Labels and entry for Student Form
		self.label = Label(self.stud_form, text = '------------', fg= 'slategray2' , font =('Segoe 18'), bg = 'slategray2').grid(row= 0, column = 0, columnspan = 5, pady = 30, sticky = 'nsew')
		self.label = Label(self.stud_form, text = 'Student Information', fg= 'White' , font =('Segoe 18'), bg = 'slategray2').grid(row= 0, column = 1, columnspan = 5, pady = 30, sticky = 'nsw')
		self.id_lbl = Label(self.stud_form,text = 'ID number :', fg = 'White', font = 'Segoe 15', bg = 'slategray2').grid(row = 2, column = 0, sticky = 'sew', padx = 3, pady = 13)
		self.name_lbl = Label(self.stud_form,text = 'Name :', fg = 'White', font = 'Segoe 15', bg = 'slategray2').grid(row = 3, column = 0, sticky = 'sew', padx = 3, pady = 13)
		self.course_lbl = Label(self.stud_form,text = 'Course :', fg = 'White', font = 'Segoe 15', bg = 'slategray2').grid(row = 4, column = 0, sticky = 'sew', padx = 3, pady = 13) 
		self.year_lbl = Label(self.stud_form,text = 'Year :', fg = 'White', font = 'Segoe 15', bg = 'slategray2').grid(row = 5, column = 0, sticky = 'sew', padx = 3, pady = 13)
	
		self.id_bar = Entry (self.stud_form, textvariable = self.stud_num, font = 'Segoe 15', bg = 'white', justify = LEFT)       
		self.name_bar = Entry (self.stud_form,textvariable = self.stud_name, font = 'Segoe 15', bg = 'white', justify = LEFT)
		self.year_bar = OptionMenu(self.stud_form, self.year_lvl, *Yrlvl_op)

		self.id_bar.grid(row=2, column = 1 , pady =13, padx = 3, sticky = 'sW', columnspan = 2)       
		self.name_bar.grid(row = 3, column= 1, pady= 13, padx = 3, sticky = 'sw',columnspan = 2)       

		self.year_bar.grid(row = 5, column= 1, pady= 13, padx = 3, sticky = 'sw',columnspan = 2)
		self.year_bar.config(width = 10)

	#Function pra maka blik sa main screen
	def back(self):
		self.master.destroy()


	#Get student info based on selected row on treeview - then iinsert sa entry widgets
	#for updating purposes
	def GetValue(self,event):
		self.clear_entry()
		self.option = 2
		self.row_id = self.tree.selection()[0]
		select = self.tree.set(self.row_id)
		self.id_bar.insert(0, select['ID number'])
		temp_id = select['ID number']
		self.name_bar.insert(0, select['Name'])
		temp_course = select['Course']
		mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="app")
		mycursor = mysqldb.cursor()
		mycursor.execute("SELECT course_id FROM Course WHERE course_name LIKE %s ",( "%" +temp_course+"%",))
		records = mycursor.fetchone()
		self.stud_course.set(records[0])
		self.year_lvl.set(select['Year level'])
		self.main()

	#clear all entry widget
	def clear_entry(self):
		self.id_bar.delete(0,END)
		self.name_bar.delete(0,END)
		self.stud_course.set(None)
		self.year_lvl.set(None)

	# murag refresh
	def cancel(self):
		self.id_num = ''
		self.clear_entry()
		self.clear_tree()
		self.show()
		self.search_bar.delete(0,END)
		for widgets in self.stud_form.winfo_children():
			widgets.destroy()
		#self.option = 1 pra ang mu display nga buttons sa student form is ang save and cancel
		self.option = 1
		self.main()

	#retrieve user input from the entry widgets -- mao ni values gamiton dayun pra pang save sa sql
	def retrieve_data(self):
		self.num = self.stud_num.get()
		self.name = self.stud_name.get()
		self.course = self.stud_course.get()
		if self.course == 'No Course Added':
			messagebox.showerror('No available course','Please add a Course before submitting new student entry')
			return False
		self.year = self.year_lvl.get()
		self.stud_data = [self.num, self.name, self.course, self.year]
		# kani is pang check if nagsunod ba sa id number nga format 0000-0000
		if not re.match('^[0-9]{4}-[0-9]{4}$', self.stud_data[0]):
			messagebox.showerror('Invalid Input','ID number is invalid. Must be in format 0000-0000')
			return False
		#pang check if completo ba ang input sa user before musave
		for data in self.stud_data:
			if len(data)==0 or data == 'None':
				messagebox.showerror('Missing Fields', "One of the required field is empty; please check your input" )
				return False

	#save into sql
	def save_sql(self):
		#if naay errors sa user input kay di ka save si user
		if self.retrieve_data() == False:
			return

		mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="app")
		mycursor=mysqldb.cursor()
		try:
		   sql = "INSERT INTO  Student(student_id, student_name, year_level ,c_id) VALUES (%s, %s, %s, %s)"
		   val = (self.num, self.name, self.year, self.course)
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

	#update info in sql
	def update(self):

		if self.retrieve_data() == False:
			print ("False update")
			return

		mysqldb = mysql.connector.connect(host = "localhost", user = "root", password = "Beleta000", database = "app")
		mycursor = mysqldb.cursor()

		try:
		   sql = "Update  Student set student_name= %s ,year_level= %s, c_id = %s where student_id= %s"
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
		self.option = 1
		self.main()

	#remove info from sql
	def delete(self):
		#For user confirmation
		answer = messagebox.askquestion("delete?", "Are you sure you want to remove student from the database?")
		if answer == 'yes':
			pass
		else:
			return

		self.num = self.stud_num.get()
		mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="app")
		mycursor=mysqldb.cursor()

		try:
		   sql = "delete from Student where student_id = %s"
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
		   
	#Para mu display or mag insert ug data ddto sa treeview
	def show(self):
		self.clear_tree()

		mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="app")
		mycursor = mysqldb.cursor()

		#For alphabetical order
		if self.sort_option == "Alphabetical":
			query = (""" SELECT Student.student_id,Student.student_name,Course.course_name, Student.year_level FROM Student INNER JOIN Course ON student.c_id = Course.course_id ORDER BY name """)

		#For year level order
		elif self.sort_option == "Year":
			query =("""SELECT Student.student_id,Student.student_name,Course.course_name, Student.year_level FROM Student INNER JOIN Course ON student.c_id = Course.course_id ORDER BY year""")

		#default
		else:
			query = "SELECT Student.student_id,Student.student_name,Course.course_name, Student.year_level FROM Student INNER JOIN Course ON student.c_id = Course.course_id"
		mycursor.execute(query)
		records = mycursor.fetchall()  

		#pag insert sa values into treeview
		for i, (id,name,course,year) in enumerate(records, start=1):
			self.tree.insert("", "end", values=(id,name, course,year))
			mysqldb.close()

	#pra makapili ug order by option
	def sort(self, sort_option):
		self.sort_option = self.sort_ch.get()
		self.show()

	#remove all input in tree
	def clear_tree(self):
		for item  in self.tree.get_children():
			self.tree.delete(item)

	#function nga naka bind sa search bar pra per input kay musearch na sya
	def tv_search(self):
		#substring is ang current nga input sa search bar
		self.substring = self.search_bar.get()

		self.clear_tree()

		mysqldb = mysql.connector.connect(host ="localhost",user = "root",password = "Beleta000",database = "app")
		mycursor= mysqldb.cursor()

		mycursor.execute("SELECT Student.student_id,Student.student_name,Course.course_name, Student.year_level FROM Student INNER JOIN Course ON student.c_id = Course.course_id WHERE student_id LIKE %s ",( "%" +self.substring+"%",))
		records = mycursor.fetchall()
		for i, (id, name, course,year) in enumerate(records, start =1):
			self.tree.insert("", "end", values = (id,name, course, year))
			mysqldb.close()

		#pra ang automatic nga ma select sa every search is ang top record
		self.selected = self.tree.get_children()[0]
		self.tree.selection_set(self.selected) 
		self.tree.yview_moveto(0)

	#Tig update sa course choices sa dropdown menu everytime naay i alter sa Course nga data
	def course_choices(self):
		self.Course.clear()
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()
		mycursor.execute("SELECT course_id from Course")
		data = mycursor.fetchall()
		#Pra dle maapil ang ktng 'None' nga naa sa course
		for element in data:
			if element[0] != 'None':
				self.Course.append(element[0])
		#If wala pay course naa
		#less than 2 kay naa nmn daan sa sulod si 'None','None', unya wa to labot
		if len(data) <2 :
			self.Course.append('No Course Added')

		self.course_bar = OptionMenu(self.stud_form,self.stud_course, *self.Course)
		self.course_bar.grid(row = 4, column= 1, pady= 13, padx = 3, sticky = 'sw',columnspan = 2) 
		self.course_bar.config(width = 10)
		
	#Gikan dre kay puros npd about sa Course
	#CRUDL -- courses version
	def manage_course(self):
		#creating toplevel -- window pra sa courses nga CRUDL
		self.mngtp = Toplevel()
		self.mngtp.geometry("800x500")
		self.mngtp.title("Manage Course")
		self.mngtp.resizable(False, False)
		self.mngtp.wm_transient(self.master)
		self.mngtp.configure(bg = "slategray2")

		#Dre nga frame gibutang ang label ug entry widget sa pagkuha sa course name and id
		self.course_frame = Frame(self.mngtp, width = 750, highlightthickness = 2, height = 150)
		self.course_frame.grid(row= 0, column = 0, columnspan = 3, rowspan = 3, sticky = 'nsew', padx = 15, pady = 10)
		self.course_frame.grid_propagate(False)
		self.course_frame.config(background = 'slategray2', highlightbackground = 'White')

		#course name and id -- label and entry widget
		Label( self.course_frame, text = "Course ID:", font = 'Segoe 17', bg = "slategray2", fg= "White").grid(row = 0, column = 0, padx = 10, pady = 20, sticky = 'w')
		self.course_id_bar = Entry( self.course_frame, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT)
		self.course_id_bar.grid(row =0,  column = 1, pady = 15, padx = 10, columnspan =2) 
		Label( self.course_frame, text = "Course name:", font = 'Segoe 17', bg = "slategray2", fg= "White").grid(row = 1, column = 0, padx = 10, pady = 20, sticky = 'w')
		self.course_name_bar = Entry( self.course_frame, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT)
		self.course_name_bar.grid(row =1 ,  column = 1, pady = 15, padx = 10, columnspan =2) 

		#Scroll frame pra sa treeview sa course list
		self.sf2 = Frame(self.mngtp, width=750, height=350, bg = 'yellow')
		self.sf2.grid(row = 4, rowspan = 6,column = 0, columnspan = 3, sticky = "nsew", padx = 7, pady = 7)
		self.sf2.columnconfigure(0, weight = 1)

		#Dre nga frame gibutang ang mga buttons
		self.frame2 = Frame(self.mngtp, width = 750, height  =50)
		self.frame2.grid(row = 10, column = 0, columnspan = 3, sticky= 'nsew', pady = 10, padx = 10)
		self.frame2.config(background = 'slategray2', highlightbackground = 'White')

		#Add new course to sql
		def save_course():

			mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="app")
			mycursor=mysqldb.cursor()

			#Retrieve entries
			self.course_id = self.course_id_bar.get()
			self.course_name = self.course_name_bar.get()

			mycursor.execute("SELECT course_name FROM Course where course_id LIKE %s", ("%" +self.course_id+ "%",))
			records = mycursor.fetchall()

			if len(records) != 0:
				messagebox.showerror("Course code already exists", "Record already exists in the database. ")
				clear_course()

			sql = "INSERT INTO  Course (course_id, course_name) VALUES (%s, %s)"
			val = (self.course_id, self.course_name)
			mycursor.execute(sql, val)
			mysqldb.commit()
			lastid = mycursor.lastrowid
			messagebox.showinfo("information", "Course Added successfully...")

			clear_course()
			self.course_choices()
			clear_tree2()
			show2()
			self.course_choices()

		#same sa clear_entry sa taas -- removes all user input sa entry widgets
		def clear_course():
			self.course_id_bar.delete(0, 'end')
			self.course_name_bar.delete(0, 'end')

		#Get course info based on selected row on treeview - then iinsert sa entry widgets
		#same sa getvalue func sa taas ganiha
		def retrieve_course(event):
			clear_course()
			update_only = 1
			self.row_id = self.tree2.selection()[0]
			select = self.tree2.set(self.row_id)
			self.course_id_bar.insert(0, select['Course Code'])
			self.temp_code = select['Course Code']
			self.course_name_bar.insert(0, select['Course Name'])

		#Update existing course on sql
		def update_course():
			#incase dapat save tuslokon pro si update button na enter
			if self.course_id_bar.get() != self.temp_code:
				messagebox.showerror("Primary Key","Course Code cannot be edited")
				return

			#Retrive data from entry widgets
			self.course_id = self.course_id_bar.get()
			self.course_name = self.course_name_bar.get()

			mysqldb = mysql.connector.connect(host = "localhost", user = "root", password = "Beleta000", database = "app")
			mycursor = mysqldb.cursor()
			mycursor.execute("SELECT course_name FROM Course where course_id LIKE %s", ("%" +self.course_id+ "%",))
			records = mycursor.fetchall()

			if len(records) == 0:
				messagebox.showerror("Cannot Updated", "Record does not exist")

			sql = "Update  Course set course_name = %s where course_id= %s"
			val = (self.course_name, self.course_id)
			mycursor.execute(sql, val)
			mysqldb.commit()
			lastid = mycursor.lastrowid
			messagebox.showinfo("information", "Record Updated successfully...")

			clear_tree2()
			show2()
			clear_course()
			self.course_choices()
	  
		def clear_tree2():
			for item  in self.tree2.get_children():
				self.tree2.delete(item)

		#remove course in sql
		def delete_course():
			self.course_id = self.course_id_bar.get()

			mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="app")
			mycursor=mysqldb.cursor()

			sql = "Update Student set c_id = %s where c_id = %s"
			#Ilisan ug 'None' ang mga c_id sa mga student nga naa sa course nga gi delete
			val = ('None', self.course_id)
			mycursor.execute(sql, val)
			mysqldb.commit()

			sql = "delete from Course where course_id = %s"
			val = (self.course_id,)
			mycursor.execute(sql, val)
			mysqldb.commit()
			lastid = mycursor.lastrowid
			messagebox.showinfo("Status", "Record Deleted successfully...")

			clear_tree2()
			show2()
			clear_course()
			self.course_choices()
			self.show()

		#Tng tanan buttons nga naa sa ubos
		def buttons():
			Button(self.frame2, text="Save", font="Segoe 15", relief=GROOVE, bd=0, command=save_course, fg="black", bg="White",height = 1, width = 7).grid(row=0, column = 0, pady =7,padx =15, sticky = 'e')      
			Button(self.frame2, text="Update", font="Segoe 15", relief=GROOVE, bd=0, command=update_course, fg="black", bg="White",height = 1, width = 7).grid(row=0, column = 1, pady =7,padx =15, sticky = 'e')      
			Button(self.frame2, text="Cancel", font="Segoe 15", relief=GROOVE, bd=0, command=clear_course, fg="black", bg="White",height = 1, width = 7).grid(row=0, column = 3, pady =7,padx =15, sticky = 'e')      
			Button(self.frame2, text="Delete", font="Segoe 15", relief=GROOVE, bd=0, command=delete_course, fg="black", bg="White",height = 1, width = 7).grid(row=0, column = 2, pady =7,padx =15,sticky = 'e')      

		#Pang insert ug data into treeview
		def show2():
			mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="app")
			mycursor = mysqldb.cursor()
			mycursor.execute("SELECT course_id, course_name FROM Course ORDER BY course_name")
			records = mycursor.fetchall()  

			#Dle iapil ug display si None
			records.remove(('None', 'None'))
			for i, (course_id,course_name) in enumerate(records, start=1):
				if records != ('None', 'None'):
					self.tree2.insert("", "end", values=(course_id, course_name))
					mysqldb.close()

	#Treeview for course display
		columns = ('Course Code', 'Course Name')
		self.tree2 = ttk.Treeview(self.sf2, style = "mystyle.Treeview",columns = columns, show = 'headings')
		treescroll = Scrollbar(self.sf2, orient = "vertical", command = self.tree.yview)
		treescroll.pack(side = RIGHT, fill = Y)
		self.tree2.configure(yscrollcommand = treescroll.set)
		self.tree2.heading('Course Code', text = 'Course Code')
		self.tree2.column('Course Code', width = 250 )
		self.tree2.heading('Course Name', text = 'Course Name')
		self.tree2.column('Course Name', width = 500)
		self.tree2.bind('<<TreeviewSelect>>', retrieve_course)
		self.tree2.pack(side = LEFT, fill = BOTH)
		show2() 
		buttons()

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
