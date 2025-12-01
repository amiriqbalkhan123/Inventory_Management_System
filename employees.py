from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.ttk import Combobox
import mysql.connector
from tkinter import messagebox





class HoverButton(Button):
    def __init__(self, master=None, **kw):
        self.default_bg = kw.get('bg', '#011A2D')  # Default background
        self.hover_bg = kw.get('activebackground', '#023A63')  # Lighter hover shade for contrast
        self.default_fg = kw.get('fg', 'white')
        self.hover_fg = kw.get('activeforeground', 'white')

        Button.__init__(self, master, **kw)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_enter(self, event):
        self.config(bg=self.hover_bg, fg=self.hover_fg)

    def on_leave(self, event):
        self.config(bg=self.default_bg, fg=self.default_fg, relief=FLAT)

    def on_press(self, event):
        self.config(relief=SUNKEN)

    def on_release(self, event):
        self.config(relief=FLAT)


def show_info_popup(anchor_widget):
    # Destroy existing popups if any
    for widget in anchor_widget.master.winfo_children():
        if isinstance(widget, Toplevel) and widget.title() == "InfoPopup":
            widget.destroy()

    popup = Toplevel(anchor_widget)
    popup.title("InfoPopup")
    popup.overrideredirect(True)  # Remove window border
    popup.attributes('-topmost', True)

    # Position the popup next to the button
    x = anchor_widget.winfo_rootx() + 40
    y = anchor_widget.winfo_rooty() + 40
    popup.geometry(f"+{x}+{y}")

    info_label = Label(
        popup,
        text="Keyboard Shortcuts:\n\n"
             "Ctrl + A → Add\n"
             "Ctrl + U → Update\n"
             "Ctrl + D → Delete\n"
             "Ctrl + C → Clear",
        font=("Winky Rough", 10, "bold"),
        justify=LEFT,
        bg="white",
        bd=1,
        relief="solid",
        padx=10,
        pady=10
    )
    info_label.pack()

    # Auto-close the popup after 5 seconds (5000 milliseconds)
    popup.after(2000, popup.destroy)




def connect_database():
    try:  # If connection is succeeded without any problem
        connection = mysql.connector.connect(host='localhost', user='root', password="Amir@12345")
        cursor = connection.cursor()  # Creating The Cursor using cursor() function
    except:  # If the connection is not succeeded and gets any errors
        messagebox.showerror('Error', "Database Connectivity Issue, Try Again")
        return None, None

    return cursor, connection


def create_database_table():
    cursor, connection = connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_management_system')
    cursor.execute('USE inventory_management_system')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS employee_data(empid INT PRIMARY KEY, name VARCHAR(200), email VARCHAR(100), '
        'gender VARCHAR(50), dob VARCHAR(30), contact VARCHAR(30), employment_type VARCHAR(50), education VARCHAR(30), '
        'work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), salary VARCHAR(50), '
        'usertype VARCHAR(50), password VARCHAR(50))')


def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_management_system')
    try:
        cursor.execute("SELECT * FROM employee_data")
        employee_records = cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def add_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
                 user_type, password):
    from dashboard import update_dashboard_counts
    if (name == "" or email == "" or gender == "Select Gender" or contact == "" or
            employment_type == "Select Type" or education == "Select Education" or
            work_shift == "Select Work Shift" or address.strip() == "" or salary == "" or
            user_type == "Select User Type" or password == ""):
        messagebox.showerror('Error', 'All Fields are Required')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('use inventory_management_system')
        # Clean up address by removing extra whitespace and newlines
        address = ' '.join(address.strip().split())

        cursor.execute(
            'INSERT INTO employee_data VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (empid, name, email, gender, dob, contact, employment_type, education,
             work_shift, address, doj, salary, user_type, password)
        )
        connection.commit()
        update_dashboard_counts()
        treeview_data()  # Refresh the treeview
        messagebox.showinfo('Success', 'Data has been Added successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to add employee: {str(e)}')
    finally:
        cursor.close()
        connection.close()


def select_data(event, empid_entry, name_entry, email_entry, dob_date_entry, gender_combobox,
                contact_entry, employment_type_combobox, education_combobox,
                work_shift_combobox, address_text, doj_date_entry, salary_entry,
                usertype_combobox, password_entry):
    index = employee_treeview.selection()
    if not index:  # Check if any item is selected
        return

    content = employee_treeview.item(index)
    row = content['values']

    if not row or len(row) < 14:
        return

    clear_fields(empid_entry, name_entry, email_entry, dob_date_entry, gender_combobox,
                 contact_entry, employment_type_combobox, education_combobox,
                 work_shift_combobox, address_text, doj_date_entry, salary_entry,
                 usertype_combobox, password_entry, False)

    try:
        # Temporarily make empid_entry writable to insert value
        empid_entry.config(state='normal')
        empid_entry.delete(0, END)
        empid_entry.insert(0, row[0])
        empid_entry.config(state='readonly')

        # Rest of your field population code remains the same
        name_entry.insert(0, row[1])
        email_entry.insert(0, row[2])
        gender_combobox.set(row[3])
        dob_date_entry.set_date(row[4])
        contact_entry.insert(0, row[5])
        employment_type_combobox.set(row[6])
        education_combobox.set(row[7])
        work_shift_combobox.set(row[8])
        address_text.insert(1.0, row[9])
        doj_date_entry.set_date(row[10])
        salary_entry.insert(0, row[11])
        usertype_combobox.set(row[12])
        password_entry.insert(0, row[13])
    except IndexError:
        messagebox.showwarning("Data Error", "Incomplete employee record")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {str(e)}")


def clear_fields(empid_entry, name_entry, email_entry, dob_date_entry, gender_combobox, contact_entry,
                 employment_type_combobox, education_combobox, work_shift_combobox, address_text, doj_date_entry,
                 salary_entry, usertype_combobox, password_entry, check):
    # Get next available ID
    next_id = get_next_empid()

    # Clear and reset empid
    empid_entry.config(state='normal')
    empid_entry.delete(0, END)
    empid_entry.insert(0, str(next_id))
    empid_entry.config(state='readonly')

    # Rest of your clearing code remains the same
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    from datetime import date
    dob_date_entry.set_date(date.today())
    gender_combobox.set('Select Gender')
    contact_entry.delete(0, END)
    employment_type_combobox.set('Select Type')
    education_combobox.set('Select Education')
    work_shift_combobox.set('Select Work Shift')
    address_text.delete(1.0, END)
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0, END)
    usertype_combobox.set('Select User Type')
    password_entry.delete(0, END)
    if check:
        employee_treeview.selection_remove(employee_treeview.selection())


def update_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                    salary, user_type, password):
    from dashboard import update_dashboard_counts

    if not empid:  # Check if empid is empty
        messagebox.showerror('Error', 'No Employee ID found - please select a record to update')
        return

    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No Row is Selected')
        return

    try:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        cursor.execute('use inventory_management_system')

        # First verify the employee exists
        cursor.execute('SELECT * from employee_data WHERE empid=%s', (empid,))
        current_record = cursor.fetchone()

        if not current_record:
            messagebox.showerror('Error', 'Selected employee not found in database')
            return

        current_data = current_record[1:]  # Skip empid in comparison
        address = address.strip()
        new_data = (name, email, gender, dob, contact, employment_type, education, work_shift,
                    address, doj, salary, user_type, password)

        if current_data == new_data:
            messagebox.showinfo('Information', "No changes Detected")
            return

        cursor.execute(
            'UPDATE employee_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, '
            'employment_type=%s, education=%s, work_shift=%s, address=%s, doj=%s, '
            'salary=%s, usertype=%s, password=%s WHERE empid=%s',
            (*new_data, empid))

        connection.commit()
        update_dashboard_counts()
        treeview_data()
        messagebox.showinfo('Success', 'Data has been successfully Updated')

    except Exception as e:
        messagebox.showerror('Error', f"Failed to update employee: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def delete_employee(empid, ):
    from dashboard import update_dashboard_counts
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No Row is Selected')
    else:
        result = messagebox.askyesno('Confirm', 'Do you really want to Delete the Record?')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('use inventory_management_system')
                cursor.execute('DELETE FROM employee_data WHERE empid=%s', (empid,))
                connection.commit()
                update_dashboard_counts()
                treeview_data()
                messagebox.showinfo('Success', 'Record has been Successfully Deleted')
            except Exception as e:
                messagebox.showerror('Error', f"Due to {e}")
            finally:
                cursor.close()
                connection.close()


def search_employee(search_option, value):
    if search_option == 'Search By':
        messagebox.showerror('Error', 'No Option is selected')
    elif value == "":
        messagebox.showerror('Error', 'Enter the value to search')
    else:
        search_option = search_option.replace(' ', '_')
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute(f'SELECT * FROM employee_data WHERE {search_option} LIKE %s', (f'%{value}%',))
            records = cursor.fetchall()
            employee_treeview.delete(*employee_treeview.get_children())
            for record in records:
                employee_treeview.insert('', END, value=record)

        except Exception as e:
            messagebox.showerror('Error', f"Due to {e}")
        finally:
            cursor.close()
            connection.close()


def show_all(search_entry, search_combobox):
    treeview_data()
    search_entry.delete(0, END)
    search_combobox.set('Search By')


def get_next_empid():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return 1  # Default starting ID if connection fails

    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT MAX(empid) FROM employee_data')
        max_id = cursor.fetchone()[0]
        return max_id + 1 if max_id is not None else 1
    except Exception as e:
        messagebox.showerror('Error', f'Error getting next employee ID: {e}')
        return 1
    finally:
        cursor.close()
        connection.close()






# GUI PART OF THE EMPLOYEES WINDOW

def employee_form(window):
    global back_image, employee_treeview, logo_image
    employee_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    employee_frame.place(x=0, y=123)
    heading_label = Label(employee_frame, text="Manage Employee Details", font=('Winky Rough', 16, 'bold'),
                          bg='#193B52',
                          fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # Top Frame
    top_frame = Frame(employee_frame, bg="#ACB1CA")
    top_frame.place(x=0, y=40, relwidth=1, height=295)

    logo_image = PhotoImage(file='images/emp350.png')
    logo_label = Label(employee_frame, image=logo_image, bg='#ACB1CA')
    logo_label.place(x=1150, y=340)

    back_image = PhotoImage(file='images/back.png')
    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2',
                         command=lambda: employee_frame.place_forget(), bg='#ACB1CA',
                         activebackground='#ACB1CA')  # using the lambda inside command argument for the method place_forget will erase the page (get back to the main window)
    back_button.place(x=6, y=0)

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(employee_frame, image=information_image, bd=0, cursor='hand2',
                                command=lambda: show_info_popup(information_button), bg='#193B52',
                                activebackground='#193B52')
    information_button.image = information_image  # PREVENTING GARBAGE COLLECTION
    information_button.place(x=10, y=8)




    # Search Frame
    search_frame = Frame(top_frame, bg='#ACB1CA')
    search_frame.pack()
    # Search ComboBox
    search_combobox = ttk.Combobox(search_frame,
                                   values=('EmpId', 'Name', 'Email', 'Employment Type', 'Education', 'Work Shift'),
                                   font=('Winky Rough', 12, 'bold'),
                                   state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=3)
    # Search Entry
    search_entry = Entry(search_frame, font=('Winky Rough', 12), bg='white')
    search_entry.grid(row=0, column=1)
    # Search Button
    search_button = HoverButton(search_frame, text="Search", font=('Winky Rough', 12, 'bold'), width=10, cursor='hand2',
                           fg='white', bg='#193B52',
                           command=lambda: search_employee(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)
    # Show Button
    show_button = HoverButton(search_frame, text="Show All", font=('Winky Rough', 12, 'bold'), width=10, cursor='hand2',
                         fg='white', bg="#193B52", command=lambda: show_all(search_entry, search_combobox))
    show_button.grid(row=0, column=3)
    # Placing Scroll Bar

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Horizontal.TScrollbar", background="#ACB1CA", troughcolor="#ACB1CA", arrowcolor="black")
    style.configure("Vertical.TScrollbar", background="#ACB1CA", troughcolor="#ACB1CA", arrowcolor="black")

    # Apply  custom styling to the scrollbars
    horizontal_scrollbar = ttk.Scrollbar(top_frame, orient=HORIZONTAL, style="Horizontal.TScrollbar")
    vertical_scrollbar = ttk.Scrollbar(top_frame, orient=VERTICAL, style="Vertical.TScrollbar")

    # Employee Table (Treeview)
    employee_treeview = ttk.Treeview(top_frame, columns=(
        'empid', 'name', 'email', 'gender', 'dob', 'contact', 'employment_type', 'education',
        'work_shift', 'address', 'doj', 'salary', 'usertype'), show='headings', yscrollcommand=vertical_scrollbar.set,
                                     xscrollcommand=horizontal_scrollbar.set)
    # Styling of the Employee Treeview using ttk style option
    # Create a custom style for the Treeview headings
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview.Heading", background="#ACB1CA", foreground="black", font=("Winky Rough", 12, "bold"))

    # Packing the Scroll bars
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10, 0))

    employee_treeview.heading('empid', text="Emp Id")
    employee_treeview.heading('name', text="Name")
    employee_treeview.heading('email', text="Email")
    employee_treeview.heading('gender', text="Gender")
    employee_treeview.heading('dob', text='Date of Birth')
    employee_treeview.heading('contact', text='Contact')
    employee_treeview.heading('employment_type', text="Employment  Type")
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text="Work  Shift")
    employee_treeview.heading('address', text="Address")
    employee_treeview.heading('doj', text='Date of Joining')
    employee_treeview.heading('salary', text="Salary")
    employee_treeview.heading('usertype', text="Type of User")

    employee_treeview.column('empid', width=80)
    employee_treeview.column('name', width=200)
    employee_treeview.column('email', width=200)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('dob', width=200)
    employee_treeview.column('contact', width=200)
    employee_treeview.column('employment_type', width=200)
    employee_treeview.column('education', width=200)
    employee_treeview.column('work_shift', width=200)
    employee_treeview.column('address', width=200)
    employee_treeview.column('doj', width=200)
    employee_treeview.column('salary', width=200)
    employee_treeview.column('usertype', width=200)

    treeview_data()  # calling the treeview to display the data into the treeview inside the GUI of the system

    # END OF EMPLOYEE TABLE

    # Details Frame (Lower Frame)
    detail_frame = Frame(employee_frame, bg="#ACB1CA")
    detail_frame.place(x=40, y=340)
    # Employee ID Label and Entry
    empid_label = Label(detail_frame, text='EmpId', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    empid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    next_id = get_next_empid()
    empid_entry = Entry(detail_frame, font=('Winky Rough', 12, 'bold'), bg="white")
    empid_entry.grid(row=0, column=1, padx=20, pady=10)
    empid_entry.insert(0, str(next_id))
    empid_entry.config(state='readonly')



















    # Name Label and Entry
    name_label = Label(detail_frame, text='Name', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    name_entry = Entry(detail_frame, font=('Winky Rough', 12, 'bold'), bg="white")
    name_entry.grid(row=0, column=3, padx=20, pady=10)

    # Email Label and Entry
    email_label = Label(detail_frame, text='Email', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    email_label.grid(row=0, column=4, padx=20, pady=10, sticky='w')
    email_entry = Entry(detail_frame, font=('Winky Rough', 12, 'bold'), bg="white")
    email_entry.grid(row=0, column=5, padx=20, pady=10)

    # Gender Label and Entry
    gender_label = Label(detail_frame, text='Gender', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    gender_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')

    gender_combobox = Combobox(detail_frame, values=('Male', 'Female'), font=('Winky Rough', 12, 'bold'), width=19,
                               state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1)

    # Date of Birth Label and Entry
    dob_label = Label(detail_frame, text='Date of Birth', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    dob_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')

    dob_date_entry = DateEntry(detail_frame, width=19, font=('Winky Rough', 12, 'bold'), state='readonly',
                               date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1, column=3)

    # Contact Label and Entry
    contact_label = Label(detail_frame, text='Contact', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    contact_label.grid(row=1, column=4, padx=20, pady=10, sticky='w')

    contact_entry = Entry(detail_frame, font=('Winky Rough', 12, 'bold'), bg="white")
    contact_entry.grid(row=1, column=5, padx=20, pady=10)

    # Employment Type Label and Entry
    employment_type_label = Label(detail_frame, text='Employment Type', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    employment_type_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')

    employment_type_combobox = Combobox(detail_frame, values=('Full Time', 'Part Time', 'Casual', 'Contract', 'Intern'),
                                        font=('Winky Rough', 12, 'bold'), width=19, state='readonly')
    employment_type_combobox.set('Select Type')
    employment_type_combobox.grid(row=2, column=1)

    # Education Label and Entry
    education_label = Label(detail_frame, text='Education', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    education_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')
    education_options = ['B.Tech', 'B.Com', 'M.Tech', 'M.Com', 'B.Sc', 'M.Sc', 'BBA', 'MBA', 'LLB', 'LLM', 'B.Arch',
                         'M.Arch']
    education_combobox = Combobox(detail_frame, values=education_options, font=('Winky Rough', 12, 'bold'), width=19,
                                  state='readonly')
    education_combobox.set('Select Education')
    education_combobox.grid(row=2, column=3)

    # Work Shift Label and Entry
    work_shift_label = Label(detail_frame, text='Work Shift', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    work_shift_label.grid(row=2, column=4, padx=20, pady=10, sticky='w')

    work_shift_combobox = Combobox(detail_frame, values=('Morning', 'Evening', 'Night'),
                                   font=('Winky Rough', 12, 'bold'),
                                   width=19, state='readonly')
    work_shift_combobox.set('Select Work Shift')
    work_shift_combobox.grid(row=2, column=5)

    # Address Label and Entry
    address_label = Label(detail_frame, text='Address', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    address_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    address_text = Text(detail_frame, width=20, height=3, font=('Winky Rough', 12), bg='white')
    address_text.grid(row=3, column=1, rowspan=2)

    # Date of Joining Label and Entry

    doj_label = Label(detail_frame, text='Date of Joining', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    doj_label.grid(row=3, column=2, padx=20, pady=10, sticky='w')

    doj_date_entry = DateEntry(detail_frame, width=19, font=('Winky Rough', 12, 'bold'), state='readonly',
                               date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3, column=3)

    # User Type Label and Entry

    usertype_label = Label(detail_frame, text='User Type', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    usertype_label.grid(row=4, column=2, padx=20, pady=10, sticky='w')

    usertype_combobox = Combobox(detail_frame, values=('Admin', 'Employee'), font=('Winky Rough', 12, 'bold'), width=19,
                                 state='readonly')
    usertype_combobox.set('Select User Type')
    usertype_combobox.grid(row=4, column=3)

    # Salary Label and Entry
    salary_label = Label(detail_frame, text='Salary', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    salary_label.grid(row=3, column=4, padx=20, pady=10, sticky='w')

    salary_entry = Entry(detail_frame, font=('Winky Rough', 12, 'bold'), bg="white")
    salary_entry.grid(row=3, column=5, padx=20, pady=10)

    # Password Label and Entry
    password_label = Label(detail_frame, text='Password', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    password_label.grid(row=4, column=4, padx=20, pady=10, sticky='w')

    password_entry = Entry(detail_frame, font=('Winky Rough', 12, 'bold'), bg="white")
    password_entry.grid(row=4, column=5, padx=20, pady=10)

    button_frame = Frame(employee_frame, bg='#ACB1CA')
    button_frame.place(x=230, y=590)

    add_button = HoverButton(button_frame, text="Add", font=('Winky Rough', 16, 'bold'), width=10, height=0, cursor='hand2',
                        fg='white', bg='#193B52',
                        command=lambda: add_employee(empid_entry.get(), name_entry.get(), email_entry.get(),
                                                     gender_combobox.get(),
                                                     dob_date_entry.get(), contact_entry.get(),
                                                     employment_type_combobox.get(), education_combobox.get(),
                                                     work_shift_combobox.get(),
                                                     address_text.get(1.0, END), doj_date_entry.get(),
                                                     salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    add_button.grid(row=0, column=0, padx=40)

    def on_ctrl_a(event):
        add_button.invoke()
        return "break"

    window.bind('<Control-a>', on_ctrl_a)


    update_button = HoverButton(button_frame, text="Update", font=('Winky Rough', 16, 'bold'), width=10, height=0,
                           cursor='hand2', fg='white', bg='#193B52',
                           command=lambda: update_employee(empid_entry.get(), name_entry.get(), email_entry.get(),
                                                           gender_combobox.get(),
                                                           dob_date_entry.get(), contact_entry.get(),
                                                           employment_type_combobox.get(), education_combobox.get(),
                                                           work_shift_combobox.get(),
                                                           address_text.get(1.0, END), doj_date_entry.get(),
                                                           salary_entry.get(), usertype_combobox.get(),
                                                           password_entry.get()))
    update_button.grid(row=0, column=2, padx=40)
    def on_ctrl_u(event):
        update_button.invoke()
        return "break"

    window.bind('<Control-u>', on_ctrl_u)
    delete_button = HoverButton(button_frame, text="Delete", font=('Winky Rough', 16, 'bold'), width=10, height=0,
                           cursor='hand2', fg='white', bg='#193B52',
                           command=lambda: delete_employee(empid_entry.get(), ))
    delete_button.grid(row=0, column=3, padx=40)
    def on_ctrl_d(event):
        delete_button.invoke()
        return "break"
    window.bind('<Control-d>', on_ctrl_d)

    clear_button = HoverButton(button_frame, text="Clear", font=('Winky Rough', 16, 'bold'), width=10, height=0,
                          cursor='hand2',
                          fg='white', bg='#193B52',
                          command=lambda: clear_fields(empid_entry, name_entry, email_entry, dob_date_entry,
                                                       gender_combobox, contact_entry, employment_type_combobox,
                                                       education_combobox, work_shift_combobox, address_text,
                                                       doj_date_entry,
                                                       salary_entry, usertype_combobox, password_entry, True))
    clear_button.grid(row=0, column=4, padx=40)
    def on_ctrl_c(event):
        clear_button.invoke()
        return "break"
    window.bind('<Control-c>', on_ctrl_c)

    employee_treeview.bind('<ButtonRelease-1>',
                           lambda event: select_data(event, empid_entry, name_entry, email_entry, dob_date_entry,
                                                     gender_combobox,
                                                     contact_entry, employment_type_combobox, education_combobox,
                                                     work_shift_combobox, address_text, doj_date_entry, salary_entry,
                                                     usertype_combobox, password_entry))



    def close_employees_frame(event=None):
        employee_frame.place_forget()
    window.bind("<Escape>", close_employees_frame)

    create_database_table()
    return employee_frame