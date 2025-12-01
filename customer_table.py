
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from pandas.tseries.holiday import next_monday_or_tuesday

from employees import connect_database


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


def get_next_customer_id():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return 1  # Default starting ID if connection fails

    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT MAX(customer_id) FROM customer_data')
        max_id = cursor.fetchone()[0]
        return max_id + 1 if max_id is not None else 1
    except Exception as e:
        messagebox.showerror('Error', f'Error getting next customer ID: {e}')
        return 1
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def show_all(treeview, search_combobox, search_entry):
    customer_treeview(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)


# This function facilitates the connection between the treeview and the sql database.
def customer_treeview(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT * from customer_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()

# This function adds the customer data to the treeview and the database accordingly.
def add_customer_data(customer_id, customer_name, customer_contact, customer_address, customer_type, additional_notes,
                      treeview):
    if (customer_name == '' or customer_contact == '' or customer_address == '' or
            customer_type == 'Select Type' or additional_notes == ''):
        messagebox.showerror('Error', 'All Fields are Required')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('use inventory_management_system')
        # Clean up additional notes
        additional_notes = ' '.join(additional_notes.strip().split())

        cursor.execute('INSERT INTO customer_data VALUES (%s,%s,%s,%s,%s,%s)', (
            customer_id, customer_name, customer_contact, customer_address, customer_type, additional_notes))

        connection.commit()
        customer_treeview(treeview)
        messagebox.showinfo('Success', 'Data has been successfully Added!')

    except Exception as e:
        messagebox.showerror('Error', f"Due to {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# This function updates the customer data to the treeview and the database accordingly.
def update_customer_data(customer_id, customer_name, customer_contact, customer_address, customer_type, additional_notes,treeview):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No Row is Selected')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:  # if cursor and connection are not met the connection will not be established
            return
        try:
            cursor.execute('USE inventory_management_system')
            cursor.execute('SELECT * from customer_data WHERE customer_id=%s',(customer_id,))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (customer_id, customer_name, customer_contact, customer_address, customer_type, additional_notes)
            if current_data == new_data:
                messagebox.showinfo('Information', "No changes Detected")
                return
            cursor.execute(
                '''UPDATE customer_data 
                   SET customer_name=%s, customer_contact=%s, customer_address=%s, 
                       customer_type=%s, additional_notes=%s 
                   WHERE customer_id=%s''',
                (customer_name, customer_contact, customer_address, customer_type, additional_notes, customer_id)
            )

            connection.commit()
            customer_treeview(treeview) # in this section all the updated data will be shown in the Treeview of the GUI on the Upper Frame inside the Employee Button
            messagebox.showinfo('Success', 'Data has been successfully Updated')
        except Exception as e:
            messagebox.showerror('Error', f"Due to {e}")
        finally:
            cursor.close()
            connection.close()


def delete_product_data(customer_id, treeview):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No Row is Selected')
    else:
        result=messagebox.askyesno('Confirm', 'Do you really want to Delete the Record?')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('USE inventory_management_system')
                cursor.execute('DELETE FROM customer_data WHERE customer_id=%s',(customer_id,))
                connection.commit()
                customer_treeview(treeview)
                messagebox.showinfo('Success', 'Record has been Successfully Deleted')
            except Exception as e:
                messagebox.showerror('Error', f"Due to {e}")
            finally:
                cursor.close()
                connection.close()


def search_product_data(search_option, value, treeview):
    # Define mapping of user-friendly options to actual database column names
    column_mapping = {
        'Customer ID': 'customer_id',
        'Customer Name': 'customer_name',
        'Customer Type': 'customer_type',  # Adjust based on your actual column name
    }

    if search_option == 'Search By':
        messagebox.showerror('Error', 'No Option is selected')
        return
    elif value == "":
        messagebox.showerror('Error', 'Enter the value to search')
        return

    # Get the actual column name from the mapping
    actual_column = column_mapping.get(search_option)
    if not actual_column:
        messagebox.showerror('Error', f"Invalid search option: {search_option}")
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_management_system')
        # Use the actual column name in the query
        cursor.execute(f"SELECT * FROM customer_data WHERE {actual_column} LIKE %s", (f"%{value}%",))
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, value=record)

    except Exception as e:
        messagebox.showerror('Error', f"Due to {e}")
    finally:
        cursor.close()
        connection.close()

# This function clears all the entry fields and the Combo Boxes in the customer frame.
def clear_fields(cust_id_entry, customer_name_entry, contact_info_entry, address_entry, customer_type_combobox,
                 additional_notes_text,check, treeview):
    next_id = get_next_customer_id()

    # Clear and reset customer ID
    cust_id_entry.config(state='normal')
    cust_id_entry.delete(0, END)
    cust_id_entry.insert(0, str(next_id))
    cust_id_entry.config(state='readonly')

    customer_name_entry.delete(0, END)
    contact_info_entry.delete(0, END)
    address_entry.delete(0, END)
    customer_type_combobox.set('Select Type')
    additional_notes_text.delete('1.0', END)


    if check and treeview:
        treeview.selection_remove(treeview.selection())

# This function fills the entries in the customer frame whenever the treeview rows are clicked.
def select_data(event, cust_id_entry, customer_name_entry, contact_info_entry, address_entry, customer_type_combobox,
                additional_notes_text, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No Item is selected')
        return

    content = treeview.item(index)
    row = content.get('values')
    if not row or len(row) < 6:
        print("Invalid or missing data in the selected row.")
        return

    # Clear fields (without clearing treeview selection)
    clear_fields(cust_id_entry, customer_name_entry, contact_info_entry, address_entry, customer_type_combobox,
                 additional_notes_text, False, None)

    try:
        # Temporarily make cust_id_entry writable to insert value
        cust_id_entry.config(state='normal')
        cust_id_entry.delete(0, END)
        cust_id_entry.insert(0, row[0])
        cust_id_entry.config(state='readonly')

        # Populate other fields
        customer_name_entry.insert(0, row[1])
        contact_info_entry.insert(0, row[2])
        address_entry.insert(0, row[3])
        customer_type_combobox.set(row[4])
        additional_notes_text.insert('1.0', row[5])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {str(e)}")


# Customer Table Treeview GUI
def cust_table(window):
    global back_image
    cust_table_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    cust_table_frame.place(x=0, y=123)

    heading_label = Label(cust_table_frame, text="Customer Details", font=('Winky Rough', 16, 'bold'),
                          bg='#193B52',
                          fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='images/back.png')
    back_button = Button(cust_table_frame, image=back_image, bd=0, cursor='hand2',
                         command=lambda: cust_table_frame.place_forget(), bg='#ACB1CA',
                         activebackground='#ACB1CA', )  # the .place_forget() methods gets the frame backs the menu (closes it)
    back_button.place(x=10, y=37)

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(cust_table_frame, image=information_image, bd=0, cursor='hand2',
                                command=lambda: show_info_popup(information_button), bg='#193B52',
                                activebackground='#193B52')
    information_button.image = information_image  # prevent garbage collection
    information_button.place(x=10, y=8)  # or .grid(...) as per your layout



    left_frame = Frame(cust_table_frame, bg='#ACB1CA', bd=1, relief=RIDGE, width=340, height=510)
    left_frame.place(x=60, y=63)

    heading_label = Label(left_frame, text="Customer Details", font=('Winky Rough', 14, 'bold'), bg='#193B52',
                          fg='white', bd=5, width=33)
    heading_label.grid(columnspan=2, sticky='we')

    cust_id_label = Label(left_frame, text='Customer ID', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    cust_id_label.grid(row=1, column=0, sticky='w', pady=20, padx=10)

    cust_id_entry = Entry(left_frame, font=('Winky Rough', 12, 'bold'), width=18, state='readonly')

    cust_id_entry.grid(row=1, column=1)
    next_id = get_next_customer_id()
    cust_id_entry.config(state='normal')
    cust_id_entry.insert(0, str(next_id))
    cust_id_entry.config(state='readonly')



    customer_name_label = Label(left_frame, text='Customer Name', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    customer_name_label.grid(row=2, column=0, pady=20, sticky='w', padx=10)

    customer_name_entry = Entry(left_frame, font=('Winky Rough', 12, 'bold'), bg='white', width=18)
    customer_name_entry.grid(row=2, column=1)

    contact_info_label = Label(left_frame, text="Contact", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    contact_info_label.grid(row=3, column=0, pady=20, sticky='w', padx=10)

    contact_info_entry = Entry(left_frame, font=('Winky Rough', 12, 'bold'), bg='white', width=18)
    contact_info_entry.grid(row=3, column=1)

    address_label = Label(left_frame, text="Customer Address", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    address_label.grid(row=4, column=0, pady=20, sticky='w', padx=10)

    address_entry = Entry(left_frame, font=('Winky Rough', 12, 'bold'), bg='white', width=18)
    address_entry.grid(row=4, column=1)

    customer_type_label = Label(left_frame, font=('Winky Rough', 12, 'bold'), text='Customer Type', bg='#ACB1CA')
    customer_type_label.grid(row=5, column=0, pady=20, sticky='w', padx=10)

    customer_type_combobox = ttk.Combobox(left_frame, font=('Winky Rough', 12, 'bold'), width=17, state='readonly',
                                          values=('Regular', 'Wholesale', 'VIP'))
    customer_type_combobox.grid(row=5, column=1)
    customer_type_combobox.set('Select Type')

    additional_notes_label = Label(left_frame, text='Additional Notes', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    additional_notes_label.grid(row=6, column=0, pady=20, sticky='w', padx=10)

    additional_notes_text = Text(left_frame, font=('Winky Rough', 12, 'bold'), width=18, height=2, bd=2, bg='white')
    additional_notes_text.grid(row=6, column=1)


    # BUTTONS
    cust_add_button = HoverButton(cust_table_frame, text='Add', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                             width=8, command=lambda:add_customer_data(cust_id_entry.get(), customer_name_entry.get(), contact_info_entry.get(),address_entry.get(),customer_type_combobox.get(),additional_notes_text.get(1.0, END), treeview))
    cust_add_button.place(x=70, y=555)

    def on_ctrl_a_customer(event):
        cust_add_button.invoke()
        return "break"
    window.bind('<Control-a>', on_ctrl_a_customer)

    cust_update_button = HoverButton(cust_table_frame, text='Update', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                                width=8,command=lambda:update_customer_data(cust_id_entry.get(),customer_name_entry.get(), contact_info_entry.get(),address_entry.get(), customer_type_combobox.get(), additional_notes_text.get(1.0, END), treeview))
    cust_update_button.place(x=150, y=555)
    def on_ctrl_u_customer(event):
        cust_update_button.invoke()
        return "break"
    window.bind('<Control-u>', on_ctrl_u_customer)
    cust_delete_button = HoverButton(cust_table_frame, text='Delete', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                                width=8, command=lambda:delete_product_data(cust_id_entry.get(), treeview))
    cust_delete_button.place(x=230, y=555)
    def on_ctrl_d_customer(event):
        cust_delete_button.invoke()
        return "break"
    window.bind('<Control-d>', on_ctrl_d_customer)
    cust_clear_button = HoverButton(cust_table_frame, text='Clear', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                               width=8, command=lambda:clear_fields(cust_id_entry, customer_name_entry, contact_info_entry, address_entry, customer_type_combobox, additional_notes_text, True, treeview))
    cust_clear_button.place(x=310, y=555)
    def on_ctrl_c_customer(event):
        cust_clear_button.invoke()
        return "break"

    window.bind('<Control-c>', on_ctrl_c_customer)
    # Treeview Frame

    treeview_frame = Frame(cust_table_frame, bg='#ACB1CA')
    treeview_frame.place(x=500, y=125, width=970, height=400)

    search_frame = LabelFrame(cust_table_frame, bg='#ACB1CA')
    search_frame.place(x=500, y=53, width=970, height=70)

    search_frame.grid_propagate(False)  # Prevent resizing due to widgets
    search_frame.grid_rowconfigure(0, weight=2)  # Adjust row height
    search_frame.grid_columnconfigure((0, 1, 3, 4), weight=1)  # Adjust column width

    search_combobox = ttk.Combobox(search_frame, values=('Customer ID', 'Customer Name', 'Customer Type'), state='readonly',
                                   width=12, font=('Winky Rough', 16, 'bold'))
    search_combobox.grid(row=0, column=0, padx=10, pady=10, ipady=4, sticky='ew')
    search_combobox.set('Search By')
    search_entry = Entry(search_frame, font=('Winky Rough', 14, 'bold'), bg='white', width=12)
    search_entry.grid(row=0, column=1, padx=10, pady=10, ipady=4, sticky='ew')

    search_button = HoverButton(search_frame, bg='#193B52', fg='white', width=6, text='Search',
                           font=('Winky Rough', 13, 'bold'), command=lambda : search_product_data(search_combobox.get(), search_entry.get(), treeview))
    search_button.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

    show_all_button = HoverButton(search_frame, bg='#193B52', fg='white', width=6, text='Show All',
                             font=('Winky Rough', 13, 'bold'), command=lambda: show_all(treeview, search_combobox, search_entry))
    show_all_button.grid(row=0, column=4, padx=10, pady=10, sticky='ew')

    # Styling for the Treeview
    style = ttk.Style()
    style.theme_use('default')  # Use a theme that supports heading customization
    style.configure("Treeview.Heading", background="#ACB1CA", foreground="black", font=("Winky Rough", 12, "bold"))
    # Horizontal and Vertical Scrollbars Configuration on following lines of code
    horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient=HORIZONTAL, style="Horizontal.TScrollbar")
    vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient=VERTICAL, style="Vertical.TScrollbar")
    # Treeview Creation over treeview frame
    treeview = ttk.Treeview(treeview_frame, columns=(
        'customer_id', 'customer_name', 'customer_contact', 'customer_address', 'customer_type', 'additional_notes'),show='headings',
                            yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    # PACKING THE SCROLL BARS
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    # Naming the Headings of the Treeview
    treeview.heading('customer_id', text='Customer ID')
    treeview.heading('customer_name', text='Customer Name')
    treeview.heading('customer_contact', text='Customer_Contact')
    treeview.heading('customer_address', text='Customer Address')
    treeview.heading('customer_type', text='Customer Type')
    treeview.heading('additional_notes', text='Additional Notes')

    # Setting the width for the headings of the columns in the treeview
    treeview.column('customer_id', width=70)
    treeview.column('customer_name', width=140)
    treeview.column('customer_contact', width=120)
    treeview.column('customer_address', width=160)
    treeview.column('customer_type', width=120)
    treeview.column('additional_notes', width=180)

    treeview.bind('<ButtonRelease-1>',
                  lambda event: select_data(event, cust_id_entry, customer_name_entry, contact_info_entry,
                                            address_entry,
                                            customer_type_combobox,
                                            additional_notes_text,treeview))



    def close_cust_table_frame(event=None):
        cust_table_frame.place_forget()
    window.bind("<Escape>", close_cust_table_frame)
    customer_treeview(treeview)
