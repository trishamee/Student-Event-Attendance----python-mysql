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
		self.event_name = ''
		self.ongoing_att = 0

		#Create Database if it does not exist
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000")
		mycursor = mysqldb.cursor()
		mycursor.execute("CREATE DATABASE IF NOT EXISTS attendance")
		mysqldb.close()

		#Create a table that will act as temporary storage
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "attendance")
		mycursor = mysqldb.cursor()
		mycursor.execute("SHOW TABLES LIKE 'temp_table'")
		result = mycursor.fetchone()
		if result:
			# there is a table named "tableName"
			pass
		else:
			# there are no tables named "tableName"
			mycursor.execute("CREATE TABLE temp_table(student_id CHAR(10) NOT NULL, time_in VARCHAR(100))")
		mysqldb.close()



		#Frame For student Event Attendance Label
		self.ttl_frame = Frame(master, width = 900, height = 150)
		self.ttl_frame.grid(row = 0 , column = 0, sticky = 'nsEw', padx = 10, pady = 10, columnspan = 3, rowspan = 3)
		self.ttl_frame.grid_propagate(False)
		self.ttl_frame.config(background = 'slategray2')

		#Frame for options
		self.op_frame = Frame(master, width = 350, height = 150, highlightthickness = 2)
		self.op_frame.grid(row = 0, column = 4, sticky = 'nsEw', padx = 10, pady = 10, rowspan = 3,columnspan =2)
		self.op_frame.grid_propagate(False)
		self.op_frame.config(background = 'slategray2', highlightbackground = "white", highlightcolor = "white")

		#Frame for Attendance
		self.att_frame = Frame(master, width = 1345, height = 525, highlightthickness = 2)
		self.att_frame.grid(row = 5, column = 0, sticky = 'nsEw', padx = 10, pady = 10, columnspan = 5, rowspan = 5)
		self.att_frame.grid_propagate(False)
		self.att_frame.config(background = 'slategray2', highlightbackground = 'white', highlightcolor = "white")

		#Label for application
		Label(self.ttl_frame, text = 'Student event attendance', font = 'Segoe 35', bg = 'slategray2', fg = 'Black').grid(row= 0, column = 0,sticky = "nsew", columnspan = 3, padx = 150, pady = 10)
		Label(self.ttl_frame, text = 'monitoring system', font = 'Segoe 35', bg = 'slategray2', fg = 'Black').grid(row= 1, column = 0, sticky = 'nsew', columnspan = 3, padx = 150, pady = 10)


		#Buttons -> Start new attendance // Open student records
		self.start_end = StringVar()
		self.start_end.set("Start New Attendance")

		Button(self.op_frame, textvariable= self.start_end, font="Segoe 13", relief=RAISED, bd=0, command=self.start, fg="black", bg="white",height = 1, width = 30, borderwidth = 3).grid(row=0, column = 0, pady =7,padx =30, sticky = 'ew', columnspan = 2)      
		Button(self.op_frame, text="Open Student records", font="Segoe 13", relief=RAISED, bd=0, command=self.open_records, fg="black", bg="white",height = 1, width = 30, borderwidth = 3).grid(row=1, column = 0, pady =7,padx =30, sticky= 'ew', columnspan = 2)      
		browse_op = ['example1', 'example2']
		self.files_list = OptionMenu(self.op_frame, self.file_name, *browse_op, command = self.file_open)
		self.files_list.grid(row=2, column = 0,pady =7,padx =30,sticky="ew", columnspan = 2)   
		self.files_list.config(width=30, height =1, bg = "white", font = "Segoe 11")
		self.file_name.set("Browse files")

	# Automatic clear entry in entry box
		def on_click(event):
			event.widget.delete(0, END)
		default_text = StringVar()
		default_text.set('Enter ID# here(0000-0000)')		

		self.entry_bar = Entry(self.att_frame, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT, textvariable= default_text)
		self.entry_bar.bind("<Button-1>", on_click)
		self.entry_bar.bind('<Return>', self.insert_stud)
		self.entry_bar.grid(row = 0, column = 0, sticky = 'ew',columnspan = 5, pady = 7, padx = 500) 
		self.entry_bar.config(width = 30)


	#Scroll frame for student display
		self.sf = Frame(self.att_frame, width=1250, height= 450, bg = 'red')
		self.sf.grid(row = 1,rowspan = 5, column = 0, columnspan =4, sticky = "nsew", padx = 43, pady = 7)
		self.sf.columnconfigure(0, weight = 1)

	#Treeview style
		style = ttk.Style()
		style.configure("mystyle.Treeview", highlightthickness=2, highlightbackground = 'Black', bd=0, font=('Segoe', 14))
		style.configure("mystyle.Treeview.Heading", font=('Segoe', 16,'bold'))
		style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
	#Treeview for student display

		columns = ('Name', 'Course', 'Year level', 'Time')
		self.tree = ttk.Treeview(self.sf, style = "mystyle.Treeview",columns = columns, show = 'headings', height = 22)

		treescroll = Scrollbar(self.sf, orient = "vertical", command = self.tree.yview)
		treescroll.pack(side = RIGHT, fill = Y)
		self.tree.configure(yscrollcommand = treescroll.set)
		self.tree.heading('Name', text = 'Name')
		self.tree.column('Name', width = 500)
		self.tree.heading('Course', text = 'Course')
		self.tree.column('Course', width = 400 )
		self.tree.heading('Year level', text = 'Year level')
		self.tree.column('Year level', width = 150)
		self.tree.heading('Time', text = 'Time')
		self.tree.column('Time', width = 200)
		self.tree.pack(side = LEFT, fill = BOTH)
		self.show()

	def clear_tree(self):
		for item  in self.tree.get_children():
			self.tree.delete(item)

	def start(self):
		if self.start_end.get() == 'Start New Attendance':
			self.start_end.set("End Attendance")
			self.new_att = Toplevel()
			self.new_att.geometry("300x200")
			self.new_att.title("New Attendance")
			self.new_att.resizable(False, False)
			self.new_att.configure(bg = "slategray2")
			Label(self.new_att, text = "Please enter event name:", font = 'Segoe 15', bg = "slategray2").grid(row = 0, column = 0, padx = 30, pady = 20, columnspan = 3)
			self.event_entry = Entry(self.new_att, font="Segoe 17", fg="Gray", bg="white", bd=0, justify=RIGHT)
			self.event_entry.grid(row = 1, column = 0, pady = 15, padx = 15, columnspan  =3) 
			Button(self.new_att, text="OK", font="Segoe 12", relief=RAISED, bd=0, command=self.new_attendance, fg="black", bg="white",height = 1, width = 5, borderwidth = 3).grid(row=2, column = 0, columnspan = 3, pady =10,padx =10)      


		elif self.start_end.get() == 'End Attendance':
			self.start_end.set("Start New Attendance")
			self.ongoing_att = 0
			#create new table within the "attendance" database
			mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "attendance")
			mycursor = mysqldb.cursor()
			#copy table Students into CopyStudents
			query= "CREATE TABLE "+ self.event_name +" SELECT * FROM temp_table"
			mycursor.execute(query)
			mycursor.execute("TRUNCATE TABLE temp_table")
			self.clear_tree()
			messagebox.showerror("Saved","Attendance has been successfully saved.")
			mysqldb.close()

		pass

	def new_attendance(self):
		self.ongoing_att = 1
		self.event_name = self.event_entry.get()
		self.new_att.destroy()
		self.clear_tree()
		#Check if database already exists
		mysqldb = mysql.connector.connect(host="localhost",user="root",password="Beleta000", database = "attendance")
		mycursor = mysqldb.cursor()
		mycursor.execute("SHOW TABLES LIKE %s",( "%" +self.event_name+"%",))
		result = mycursor.fetchone()
		if result:
			# there is a table named "tableName"
			messagebox.showerror("Event name error", "Event Name already exists.")
			print('there are tables')
			return
		else:
			# there are no tables named "tableName"
			pass
			# populate table
		mysqldb.close()
		

	def insert_stud(self, event):
		if self.ongoing_att == 0:
			messagebox.showerror("Not yet started", "There is no ongoing attendance")
			return

		stud_id = self.entry_bar.get()
		now = datetime.now()
		curr_time = now.strftime('%Y-%m-%d %H:%M:%S')
		mysqldb=mysql.connector.connect(host="localhost",user="root",password = "Beleta000",database="attendance")
		mycursor=mysqldb.cursor()
		try:
		   sql = "INSERT INTO temp_table (student_id, time_in) VALUES (%s, %s)"
		   val = (stud_id, curr_time)
		   mycursor.execute(sql, val)
		   mysqldb.commit()
		   lastid = mycursor.lastrowid
		   messagebox.showinfo("Information", "Attendance successfully recorded")

		except Exception as e:
		   print(e)
		   messagebox.showinfo("Error" ,e)
		   mysqldb.rollback()
		   mysqldb.close()
		self.clear_tree()
		self.show()		

	def open_records(self):
		pass  

	def file_open(self):
		pass

	def show(self):
		self.clear_tree()

		mysqldb = mysql.connector.connect(host="localhost", user="root", password = "Beleta000", database="attendance")
		mycursor = mysqldb.cursor()

		query = " SELECT s.name, c.course_name, s.year, e.time_in FROM (student s JOIN courses c ON s.course_code = c.course_code) JOIN  temp_table e ON e.student_id = s.id ORDER BY e.time_in DESC"
		mycursor.execute(query) 
		records = mycursor.fetchall()  

		for i, (name,course,year,time) in enumerate(records, start=1):
			self.tree.insert("", "end", values=(name, course,year,time))
			mysqldb.close()

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
