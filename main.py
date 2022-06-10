from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector 
import re
from datetime import datetime
import records

class mainframe(Frame):
	def __init__(self, master, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		self.file_name = StringVar()
		self.ongoing_att = 0
		self.event_name = '---------'
		self.location = '----------'
		self.date_started = '--------'
		self.date_ended = '---------'
		self.files=[]
		self.event_id =''
		self.event_name =''
		self.location =''
		self.date_started =''
		self.date_ended =''

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
			mycursor.execute("CREATE TABLE Student(student_id VARCHAR(9) NOT NULL,student_name VARCHAR(60) NOT NULL, c_id CHAR(10) NOT NULL, year_level INT(1) NOT NULL, PRIMARY KEY (student_id), FOREIGN KEY (c_id) REFERENCES Course(course_id))")
		mysqldb.close()

	#Create a table for event information
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()
		mycursor.execute("SHOW TABLES LIKE 'Event'")
		result = mycursor.fetchone()
		if result:
			# there is a table named "tableName"
			pass
		else:
			# there are no tables named "tableName"
			mycursor.execute("CREATE TABLE Event(event_id INT(6) NOT NULL , event_name VARCHAR(80) NOT NULL , location VARCHAR(80) NOT NULL, date_started DATETIME(6) NOT NULL, date_ended DATETIME(6), PRIMARY KEY (event_id))")
		mysqldb.close()

	#Create a table for attendance
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()
		mycursor.execute("SHOW TABLES LIKE 'Attendance'")
		result = mycursor.fetchone()
		if result:
			# there is a table named "tableName"
			pass
		else:
			# there are no tables named "tableName"
			mycursor.execute("CREATE TABLE Attendance(e_id INT(6) NOT NULL , s_id VARCHAR(9) NOT NULL, time_in DATETIME(6) NOT NULL, time_out DATETIME(6), FOREIGN KEY(e_id) REFERENCES Event(event_id), FOREIGN KEY(s_id) REFERENCES Student(student_id))")
		mysqldb.close()


	#Frame For student Event Attendance Label --> upper left
		self.ttl_frame = Frame(master, width = 900, height = 150, highlightthickness = 2)
		self.ttl_frame.grid(row = 0 , column = 0, sticky = 'nsEw', padx = 10, pady = 10, columnspan = 3, rowspan = 3)
		self.ttl_frame.grid_propagate(False)
		self.ttl_frame.config(background = 'slategray2', highlightbackground = "white", highlightcolor = "white")

	#Frame for options --> upper right
		self.op_frame = Frame(master, width = 350, height = 150, highlightthickness = 2)
		self.op_frame.grid(row = 0, column = 4, sticky = 'nsEw', padx = 10, pady = 10, rowspan = 3,columnspan =2)
		self.op_frame.grid_propagate(False)
		self.op_frame.config(background = 'slategray2', highlightbackground = "white", highlightcolor = "white")

	#Frame for Attendance 
		self.att_frame = Frame(master, width = 1345, height = 525, highlightthickness = 2)
		self.att_frame.grid(row = 5, column = 0, sticky = 'nsEw', padx = 10, pady = 10, columnspan = 5, rowspan = 5)
		self.att_frame.grid_propagate(False)
		self.att_frame.config(background = 'slategray2', highlightbackground = 'white', highlightcolor = "white")

	#Buttons -> Start new app // Open student records // browse events
		#Pra ni sa start attendance nga option pra mag change2 ang title sa button mao stringvar
		self.start_end = StringVar()
		self.start_end.set("Start New Attendance")

		#Kani kay pra makuha ang list sa mga available nga events
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()

		Button(self.op_frame, textvariable= self.start_end, font="Segoe 13", relief=RAISED, bd=0, command=self.start, fg="black", bg="white",height = 1, width = 30, borderwidth = 3).grid(row=0, column = 0, pady =7,padx =30, sticky = 'ew', columnspan = 2)      
		Button(self.op_frame, text="Open Student records", font="Segoe 13", relief=RAISED, bd=0, command=self.open_records, fg="black", bg="white",height = 1, width = 30, borderwidth = 3).grid(row=1, column = 0, pady =7,padx =30, sticky= 'ew', columnspan = 2)      
		self.file_choices()

	# Automatic clear entry in entry box
		def on_click(event):
			event.widget.delete(0, END)
		default_text = StringVar()
		default_text.set('Enter ID# here(0000-0000)')		

		#Entry widget --> dre i input ang student id
		self.entry_bar = Entry(self.att_frame, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT, textvariable= default_text)
		self.entry_bar.bind("<Button-1>", on_click)
		self.entry_bar.bind('<Return>', self.insert_stud)
		self.entry_bar.grid(row = 0, column = 0, sticky = 'ew',columnspan = 5, pady = 7, padx = 500) 
		self.entry_bar.config(width = 30)

	#Scroll frame for attendance display
		self.sf = Frame(self.att_frame, width=1250, height= 450, bg = 'red')
		self.sf.grid(row = 1,rowspan = 5, column = 0, columnspan =4, sticky = "nsew", padx = 43, pady = 7)
		self.sf.columnconfigure(0, weight = 1)

	#Treeview style
		style = ttk.Style()
		style.configure("mystyle.Treeview", highlightthickness=2, highlightbackground = 'Black', bd=0, font=('Segoe', 14))
		style.configure("mystyle.Treeview.Heading", font=('Segoe', 16,'bold'))
		style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
	#Treeview for student display

		columns = ('Name', 'Course', 'Year level', 'Time in', 'Time out')
		self.tree = ttk.Treeview(self.sf, style = "mystyle.Treeview",columns = columns, show = 'headings', height = 22)

		treescroll = Scrollbar(self.sf, orient = "vertical", command = self.tree.yview)
		treescroll.pack(side = RIGHT, fill = Y)
		self.tree.configure(yscrollcommand = treescroll.set)
		self.tree.heading('Name', text = 'Name')
		self.tree.column('Name', width = 400)
		self.tree.heading('Course', text = 'Course')
		self.tree.column('Course', width = 350 )
		self.tree.heading('Year level', text = 'Year level')
		self.tree.column('Year level', width = 120)
		self.tree.heading('Time in', text = 'Time in')
		self.tree.column('Time in', width = 190)
		self.tree.heading('Time out', text = 'Time out')
		self.tree.column('Time out', width = 190)
		self.tree.pack(side = LEFT, fill = BOTH)
		self.show()
		self.disp_event_info()

	def disp_event_info(self):
	#Label at upper left -- current event information
		print(self.event_id)
		for widget in self.ttl_frame.winfo_children():
			widget.destroy()
		if self.ongoing_att == 0:
			self.event_name = '---------'
			self.location = '----------'
			self.date_started = '--------'
			self.date_ended = '---------'
		else:
			mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
			mycursor = mysqldb.cursor()
			sql = ("SELECT * from Event WHERE event_id = '%s' ")
			value = (self.event_id)
			mycursor.execute(sql, value)
			result = mycursor.fetchall()
			self.event_name = result[0][1]
			self.location = result[0][2]
			self.date_started = result [0][3]
			self.date_ended = result[0] [4]
		Label(self.ttl_frame, text = 'Current event:', font = 'Segoe 18', bg = 'slategray2', fg = 'Black').grid(row= 0, column = 0,sticky = "nsw", columnspan = 4, padx = 15, pady = 10)
		Label(self.ttl_frame, text = 'Event:', font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=1, column = 1, sticky = 'nsw', padx = 15, pady = 10)
		Label(self.ttl_frame, text = 'Location:', font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=2, column = 1, sticky = 'nsw', padx = 15, pady = 10)
		Label(self.ttl_frame, text = 'Date Started:', font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=1, column = 3, sticky = 'nsw', padx = 15, pady = 10)
		Label(self.ttl_frame, text = 'Date Ended:', font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=2, column = 3, sticky = 'nsw', padx = 15, pady = 10)
		Label(self.ttl_frame, text = self.event_name, font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=1, column = 2, sticky = 'nsw', padx = 15, pady = 10)
		Label(self.ttl_frame, text = self.location, font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=2, column = 2, sticky = 'nsw', padx =15, pady = 10)
		Label(self.ttl_frame, text = self.date_started, font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=1, column = 4, sticky = 'nsw', padx = 15, pady = 10)
		Label(self.ttl_frame, text = self.date_ended, font = 'Segoe 15', bg = 'slategray2', fg = 'Black').grid(row=2, column = 4, sticky = 'nsw', padx = 15, pady = 10)


	def clear_tree(self):
		for item  in self.tree.get_children():
			self.tree.delete(item)

	#Kani ang function pra makapili if mag  start or end ug isa ka attendance
	def start(self):

		#If mag start ug new attendance / event
		if self.start_end.get() == 'Start New Attendance':
			self.start_end.set("End Attendance")

			#Toplevel -- dre nga window i input ang event name ug location
			self.new_att = Toplevel()
			self.new_att.geometry("500x300")
			self.new_att.title("New Attendance")
			self.new_att.resizable(False, False)
			self.new_att.configure(bg = "slategray2")

			#Labels and entry widgets --> Event ID, event name, event location
			Label(self.new_att, text = "Event ID:", font = 'Segoe 15', bg = "slategray2").grid(row = 0, column = 0, padx = 30, pady = 20, sticky = 'w')
			self.event_id_bar = Entry(self.new_att, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT)
			self.event_id_bar.grid(row =0,  column = 1, pady = 15, padx = 15) 
			Label(self.new_att, text = "Event name:", font = 'Segoe 15', bg = "slategray2").grid(row = 1, column = 0, padx = 30, pady = 20, sticky = 'w')
			self.event_name_bar = Entry(self.new_att, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT)
			self.event_name_bar.grid(row =1 ,  column = 1, pady = 15, padx = 15) 
			Label(self.new_att, text = "Event location:", font = 'Segoe 15', bg = "slategray2").grid(row = 2, column = 0, padx = 30, pady = 20,  sticky = 'w')
			self.location_bar = Entry(self.new_att, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT)
			self.location_bar.grid(row =2,  column = 1, pady = 15, padx = 15) 
			Button(self.new_att, text="OK", font="Segoe 12", relief=RAISED, bd=0, command=self.new_attendance, fg="black", bg="white",height = 1, width = 5, borderwidth = 3).grid(row=3, column = 0, columnspan = 2, pady =10,padx =10)      

		#If i end ang attendance
		elif self.start_end.get() == 'End Attendance':
			self.file_choices()
			save = messagebox.askquestion("Save?", "Do you want to save the attendance?")
			self.start_end.set("Start New Attendance")

			if save == 'no':
				self.ongoing_att = 0
				self.clear_tree()
				self.event_id = ''
				self.event_name = ''
				self.location = ''
				self.date_started = ''
				self.date_ended = ''
				messagebox.showinfo("Information","Attendance was not saved.")
				mysqldb.close()
				self.clear_tree()

			if save == 'yes':
				self.ongoing_att = 0
				now = datetime.now()
				#save current date
				self.date_ended = now.strftime('%Y-%m-%d %H:%M:%S')
				mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
				mycursor = mysqldb.cursor()
				sql = "Update Event set date_ended = %s where event_id = %s"
				val = (self.date_ended, self.event_id_2)
				mycursor.execute(sql, val)
				mysqldb.commit()
				lastid = mycursor.lastrowid
				self.file_choices()	
				self.clear_tree()


			self.disp_event_info()

	#if mag add ug new event for attendance
	def new_attendance(self):
		self.ongoing_att = 1

		#retrieve info
		self.event_id = self.event_id_bar.get()
		self.event_id_2  =self.event_id
		self.event_name = self.event_name_bar.get()
		self.location = self.location_bar.get()
		now = datetime.now()
		self.date_started = now.strftime('%Y-%m-%d %H:%M:%S')

		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()

		sql = "INSERT INTO Event(event_id, event_name, location, date_started) VALUES (%s,%s,%s,%s)"
		val = (self.event_id, self.event_name, self.location, self.date_started)
		mycursor.execute(sql, val)
		mysqldb.commit()
		lastid = mycursor.lastrowid

		mycursor.execute("SELECT event_id from Event where event_name LIKE %s ",( "%" +self.event_name+"%",))
		result = mycursor.fetchall()
		self.event_id = result[0]
		self.disp_event_info()

		self.new_att.destroy()
		self.clear_tree()

	def insert_stud(self, event):
		if self.ongoing_att == 0:
			messagebox.showerror("Not yet started", "There is no ongoing attendance")
			return

		stud_id = self.entry_bar.get()
		now = datetime.now()
		curr_time = now.strftime('%Y-%m-%d %H:%M:%S')

		mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="app")
		mycursor=mysqldb.cursor()

		#check if stud_id is already entered once
		sql = "SELECT * from Attendance where e_id = %s and s_id = %s"
		val  = (self.event_id_2, stud_id)
		mycursor.execute(sql, val)
		result = mycursor.fetchall()
		print(result)

		print(stud_id)
		if len(result) == 0:
			sql = "INSERT INTO Attendance (e_id, s_id,time_in) VALUES (%s, %s, %s)"
			val = ( self.event_id_2, stud_id, curr_time)
			mycursor.execute(sql, val)
			mysqldb.commit()
			lastid = mycursor.lastrowid
			messagebox.showinfo("Information", "Attendance successfully recorded - time in")
		else:
			sql = "Update  Attendance set time_out = %s where s_id= %s and e_id = %s"
			val = (curr_time, stud_id, self.event_id_2 )
			mycursor.execute(sql,val )
			mysqldb.commit()
			lastid = mycursor.lastrowid
			messagebox.showinfo("Information", "Attendance successfully recorded - time out")

		self.clear_tree()
		self.show()		

	def open_records(self):
		self.top = Toplevel(self.master)
		self.top.state("zoomed")
		self.top.title("Student Records")
		self.top.resizable(False, False)
		self.top.configure(bg = "slategray2")
		self.top.wm_transient(self.master)
		records.mainframe(self.top) 
		

	def file_open(self,event):
		self.event_name = self.file_name.get()
		mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="app")
		mycursor = mysqldb.cursor()
		mycursor.execute("SELECT event_id from Event where event_name LIKE %s ",( "%" +self.event_name+"%",))
		result = mycursor.fetchall()
		self.event_id = result[0]
		self.show()
		self.ongoing_att = 2
		self.disp_event_info()


	def show(self):
		print('----show------')
		self.clear_tree()
		print(self.event_id)
		mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="app")
		mycursor = mysqldb.cursor()

		query = " SELECT s.student_name, c.course_name, s.year_level, a.time_in, a.time_out FROM (Student s JOIN Course c ON s.c_id = c.course_id) JOIN  Attendance a ON a.s_id = s.student_id WHERE( a.e_id = '%s')  ORDER BY a.time_in DESC"
		value = (self.event_id)
		mycursor.execute(query, value) 
		records = mycursor.fetchall()  

		for i, (name,course,year,time_in, time_out) in enumerate(records, start=1):
			self.tree.insert("", "end", values=(name, course,year,time_in, time_out))
			mysqldb.close()

	def file_choices(self):
		self.files.clear()
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "app")
		mycursor = mysqldb.cursor()
		mycursor.execute("SELECT event_name from Event")
		data = mycursor.fetchall()

		for element in data:
			self.files.append(element[0])
		if len(data) == 0 :
			self.files.append('No previous events')

		self.files_list = OptionMenu(self.op_frame, self.file_name, *self.files, command = self.file_open)
		self.files_list.grid(row=2, column = 0,pady =7,padx =30,sticky="ew", columnspan = 2)   
		self.files_list.config(width=30, height =1, bg = "white", font = "Segoe 11")
		self.file_name.set("Browse files")

class SIS(Tk):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# set the window properties
		self.title("Student Event Attendance System")
		self.state('zoomed')
		self.configure(bg = 'slategray2')
		mainframe(self).grid()


if __name__ == '__main__':
	app = SIS()
	app.mainloop()
