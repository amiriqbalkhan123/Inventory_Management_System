from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
from employees import connect_database
from tkinter import messagebox
from datetime import datetime, date



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


def get_next_transaction_id():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return 1  # Default starting ID if connection fails

    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT MAX(transaction_id) FROM transaction_data')
        max_id = cursor.fetchone()[0]
        return max_id + 1 if max_id is not None else 1
    except Exception as e:
        messagebox.showerror('Error', f'Error getting next transaction ID: {e}')
        return 1
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def show_all(treeview, search_combobox, search_entry):
    transaction_treeview(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)


# This function facilitates the connection between the treeview and the sql database.
def transaction_treeview(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT * from transaction_data')
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
def add_transaction_data(transaction_id, transaction_date, transaction_time, payment_type, payment_status,
                         total_amount, handled_by, notes, treeview):
    if (transaction_date == '' or transaction_time == '' or
            payment_type == 'Select Payment Type' or payment_status == 'Select Payment Status' or
            total_amount == '' or handled_by == '' or notes == ''):
        messagebox.showerror('Error', 'All Fields are Required')
        return

    try:
        # Validate total_amount is numeric
        float(total_amount)
    except ValueError:
        messagebox.showerror('Error', 'Total Amount must be a number')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('use inventory_management_system')
        # Clean up notes
        notes = ' '.join(notes.strip().split())

        cursor.execute('INSERT INTO transaction_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (
            transaction_id, transaction_date, transaction_time, payment_type, payment_status,
            total_amount, handled_by, notes))

        connection.commit()
        transaction_treeview(treeview)
        messagebox.showinfo('Success', 'Data has been successfully Added!')
    except Exception as e:
        messagebox.showerror('Error', f"Due to {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# This function updates the customer data to the treeview and the database accordingly.
def update_transaction_data(transaction_id, transaction_date, transaction_time, payment_type, payment_status, total_amount, handled_by, notes,treeview):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No Row is Selected')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:  # if cursor and connection are not met the connection will not be established
            return
        try:
            cursor.execute('USE inventory_management_system')
            cursor.execute('SELECT * from transaction_data WHERE transaction_id=%s',(transaction_id,))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (transaction_id, transaction_date, transaction_time, payment_type, payment_status, total_amount, handled_by, notes)
            if current_data == new_data:
                messagebox.showinfo('Information', "No changes Detected")
                return
            cursor.execute(
                '''UPDATE transaction_data 
                   SET transaction_date=%s, transaction_time=%s, payment_type=%s, 
                       payment_status=%s, total_amount=%s, handled_by=%s, notes=%s 
                   WHERE transaction_id=%s''',
                (transaction_date, transaction_time, payment_type, payment_status, total_amount, handled_by, notes,
                 transaction_id)
            )

            connection.commit()
            transaction_treeview(treeview) # in this section all the updated data will be shown in the Treeview of the GUI on the Upper Frame inside the Employee Button
            messagebox.showinfo('Success', 'Data has been successfully Updated')
        except Exception as e:
            messagebox.showerror('Error', f"Due to {e}")
        finally:
            cursor.close()
            connection.close()


def delete_transaction_data(transaction_id, treeview):
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
                cursor.execute('DELETE FROM transaction_data WHERE transaction_id=%s',(transaction_id,))
                connection.commit()
                transaction_treeview(treeview)
                messagebox.showinfo('Success', 'Record has been Successfully Deleted')
            except Exception as e:
                messagebox.showerror('Error', f"Due to {e}")
            finally:
                cursor.close()
                connection.close()


def search_transaction_data(search_option, value, treeview):
    # Define mapping of user-friendly options to actual database column names
    column_mapping = {
        'Transaction ID': 'transaction_id',
        'Payment Type': 'payment_type',
        'Handled By': 'handled_by',  # Adjust based on your actual column name
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
        cursor.execute(f"SELECT * FROM transaction_data WHERE {actual_column} LIKE %s", (f"%{value}%",))
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
def clear_fields(transaction_id_entry, transaction_date_entry, transaction_time_entry, payment_type_combobox, payment_status_combobox,
                 total_amount_entry,handled_by_entry, notes_text,check, treeview):
    next_id = get_next_transaction_id()

    transaction_id_entry.config(state='normal')
    transaction_id_entry.delete(0, END)
    transaction_id_entry.insert(0, str(next_id))
    transaction_id_entry.config(state='readonly')



    transaction_date_entry.set_date(date.today())
    transaction_time_entry.delete(0, END)
    payment_type_combobox.set('Select Payment Type')
    payment_status_combobox.set('Select Payment Status')
    total_amount_entry.delete(0, END)
    handled_by_entry.delete(0, END)
    notes_text.delete('1.0', END)


    if check and treeview:
        treeview.selection_remove(treeview.selection())

# This function fills the entries in the customer frame whenever the treeview rows are clicked.
def select_data(event, transaction_id_entry, transaction_date_entry, transaction_time_entry, payment_type_combobox, payment_status_combobox,
                total_amount_entry,handled_by_entry, notes_text, treeview):
    # Get the selected item
    index = treeview.selection()
    if not index:
        # No item is selected
        messagebox.showerror('Error', 'No Item is selected')
        return
    # Get item content
    content = treeview.item(index)
    row = content.get('values')
    if not row or len(row) < 8:  # Ensure row is not empty and has enough elements
        print("Invalid or missing data in the selected row.")
        return
    # Clear the fields
    clear_fields(transaction_id_entry, transaction_date_entry, transaction_time_entry, payment_type_combobox, payment_status_combobox,
                 total_amount_entry,handled_by_entry, notes_text, treeview, False)
    try:
        # Populate the fields
        transaction_id_entry.config(state='normal')
        transaction_id_entry.delete(0, END)
        transaction_id_entry.insert(0, row[0])
        transaction_id_entry.config(state='readonly')


        transaction_date_entry.set_date(row[1])
        transaction_time_entry.insert(0, row[2])
        payment_type_combobox.set(row[3])
        payment_status_combobox.set(row[4])
        total_amount_entry.insert(0, row[5])
        handled_by_entry.insert(0, row[6])
        notes_text.insert(1.0, row[7])
    except Exception as e:
        messagebox.showerror('Error', f'Failed to Load Data: {str(e)}')


# THE GUI PART OF THE TRANSACTION FORM
def tran_table(window):
    global back_image
    tran_table_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    tran_table_frame.place(x=0, y=123)

    heading_label = Label(tran_table_frame, text="Transaction Summary", font=('Winky Rough', 16, 'bold'),
                          bg='#193B52',
                          fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='images/back.png')
    back_button = Button(tran_table_frame, image=back_image, bd=0, cursor='hand2',
                         command=lambda: tran_table_frame.place_forget(), bg='#ACB1CA',
                         activebackground='#ACB1CA', )  # the .place_forget() methods gets the frame backs the menu (closes it)
    back_button.place(x=10, y=37)

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(tran_table_frame, image=information_image, bd=0, cursor='hand2',
                                command=lambda: show_info_popup(information_button), bg='#193B52',
                                activebackground='#193B52')
    information_button.image = information_image  # prevent garbage collection
    information_button.place(x=10, y=8)  # or .grid(...) as per your layout

    # Treeview Frame
    treeview_frame = Frame(tran_table_frame, bg='#ACB1CA')
    treeview_frame.place(x=500, y=125, width=970 , height=448)

    search_frame = LabelFrame(tran_table_frame, bg='#ACB1CA')
    search_frame.place(x=500, y=53, width=970, height=70)

    search_frame.grid_propagate(False)  # Prevent resizing due to widgets
    search_frame.grid_rowconfigure(0, weight=2)  # Adjust row height
    search_frame.grid_columnconfigure((0, 1, 3, 4), weight=1)  # Adjust column width

    search_combobox = ttk.Combobox(search_frame, values=('Transaction ID', 'Payment Type', 'Handled By'),
                                   state='readonly',
                                   width=15, font=('Winky Rough', 16, 'bold'))
    search_combobox.grid(row=0, column=0, padx=10, pady=10, ipady=4, sticky='ew')
    search_combobox.set('Search By')
    search_entry = Entry(search_frame, font=('Winky Rough', 14, 'bold'), bg='white', width=12)
    search_entry.grid(row=0, column=1, padx=10, pady=10, ipady=4, sticky='ew')

    search_button = HoverButton(search_frame, bg='#193B52', fg='white', width=6, text='Search',
                           font=('Winky Rough', 13, 'bold'), command=lambda:search_transaction_data(search_combobox.get(), search_entry.get(), treeview))
    search_button.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

    show_all_button = HoverButton(search_frame, bg='#193B52', fg='white', width=6, text='Show All',
                             font=('Winky Rough', 13, 'bold'), command=lambda:show_all(treeview, search_combobox, search_entry))
    show_all_button.grid(row=0, column=4, padx=10, pady=10, sticky='ew')

    transaction_frame = Frame(tran_table_frame, bg='#ACB1CA', height=660, bd=1, relief=RIDGE, width=320)
    transaction_frame.place(x=50, y=63)

    heading_label = Label(transaction_frame, text="Transaction Summary", font=('Winky Rough', 14, 'bold'), bg='#193B52',
                          fg='white', bd=5)
    heading_label.grid(row=1, column=0, columnspan=2, sticky='we')

    transaction_id_label = Label(transaction_frame, text="Transaction ID", font=('Winky Rough', 12, 'bold'),
                                 bg='#ACB1CA')
    transaction_id_label.grid(row=2, column=0, padx=15, pady=15, sticky='w')

    transaction_id_entry = Entry(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='white', state='readonly')
    transaction_id_entry.grid(row=2, column=1)
    next_id = get_next_transaction_id()
    transaction_id_entry.config(state='normal')
    transaction_id_entry.insert(0, str(next_id))
    transaction_id_entry.config(state='readonly')



    transaction_date_label = Label(transaction_frame, text="Transaction Date", font=('Winky Rough', 12, 'bold'),
                                   bg='#ACB1CA')
    transaction_date_label.grid(row=3, column=0, padx=15, pady=15, sticky='w')

    transaction_date_entry = DateEntry(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='white', date_pattern='dd/mm/yyyy', state='readonly', width=19)
    transaction_date_entry.grid(row=3, column=1)
    transaction_date_entry.set_date(date.today())
    transaction_time_label = Label(transaction_frame, text="Transaction Time", font=('Winky Rough', 12, 'bold'),
                                   bg='#ACB1CA')
    transaction_time_label.grid(row=4, column=0, padx=15, pady=14, sticky='w')

    transaction_time_entry = Entry(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='white', state='readonly', justify="center")
    transaction_time_entry.grid(row=4, column=1)
    transaction_time_entry.config(state='normal')
    transaction_time_entry.delete(0, END)

    def update_time():
        """Update the transaction_time_entry every second."""
        current_time = datetime.now().strftime("%I:%M:%S %p")
        transaction_time_entry.config(state='normal')  # Temporarily enable editing
        transaction_time_entry.delete(0, END)
        transaction_time_entry.insert(0, current_time)
        transaction_time_entry.config(state='readonly')  # Set back to read-only
        window.after(1000, update_time)
    update_time()
    payment_type_label = Label(transaction_frame, text="Payment Type", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    payment_type_label.grid(row=5, column=0, padx=15, pady=14, sticky='w')

    payment_type_combobox = ttk.Combobox(transaction_frame, font=('Winky Rough', 12, 'bold'), state='readonly',
                                         values=('Credit Card', 'Debit Card', 'Master Card', 'Paypal', 'Azizi Bank', 'COD'), width=19)
    payment_type_combobox.set('Select Payment Type')
    payment_type_combobox.grid(row=5, column=1)

    payment_status_label = Label(transaction_frame, text="Payment Status", font=('Winky Rough', 12, 'bold'),
                                 bg='#ACB1CA')
    payment_status_label.grid(row=6, column=0, padx=15, pady=14, sticky='w')

    payment_status_combobox = ttk.Combobox(transaction_frame, font=('Winky Rough', 12, 'bold'), state='readonly',
                                           values=('Completed', 'Pending', 'Failed', 'In Progress', 'Refunded'), width=19)
    payment_status_combobox.grid(row=6, column=1, sticky='w', padx=14, pady=15)
    payment_status_combobox.set('Select Payment Status')

    total_amount_label = Label(transaction_frame, text="Total Amount", font=('winky Rough', 12, 'bold'), bg='#ACB1CA')
    total_amount_label.grid(row=7, column=0, padx=15, pady=14, sticky='w')

    total_amount_entry = Entry(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='white', width=20)
    total_amount_entry.grid(row=7, column=1, pady=15, padx=14, sticky='w')

    handled_by_label = Label(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='#ACB1CA', text='Handled By')
    handled_by_label.grid(row=8, column=0, padx=15, pady=14, sticky='w')

    handled_by_entry = Entry(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='white', width=20)
    handled_by_entry.grid(row=8, column=1, padx=15, pady=14, sticky='w')

    notes_label = Label(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='#ACB1CA', text="Notes")
    notes_label.grid(row=9, column=0, padx=15, pady=14, sticky='w')

    notes_text = Text(transaction_frame, font=('Winky Rough', 12, 'bold'), bg='white', width=20, height=2)
    notes_text.grid(row=9, column=1)


    # BUTTONS

    tran_add_button = HoverButton(tran_table_frame, text='Add', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                             width=8, command=lambda:add_transaction_data(transaction_id_entry.get(), transaction_date_entry.get(),transaction_time_entry.get(),payment_type_combobox.get(),payment_status_combobox.get(),total_amount_entry.get(), handled_by_entry.get(), notes_text.get(1.0, END),treeview))
    tran_add_button.place(x=70, y=580)

    def on_ctrl_a_transaction(event):
        tran_add_button.invoke()
        return "break"
    window.bind('<Control-a>', on_ctrl_a_transaction)

    tran_update_button = HoverButton(tran_table_frame, text='Update', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                                width=8, command=lambda:update_transaction_data(transaction_id_entry.get(), transaction_date_entry.get(), transaction_time_entry.get(), payment_type_combobox.get(), payment_status_combobox.get(),total_amount_entry.get(), handled_by_entry.get(), notes_text.get(1.0, END),treeview))
    tran_update_button.place(x=150, y=580)
    def on_ctrl_u_transaction(event):
        tran_update_button.invoke()
        return "break"
    window.bind('<Control-u>', on_ctrl_u_transaction)
    tran_delete_button = HoverButton(tran_table_frame, text='Delete', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                                width=8, command=lambda:delete_transaction_data(transaction_id_entry.get(), treeview))
    tran_delete_button.place(x=230, y=580)
    def on_ctrl_d_transaction(event):
        tran_delete_button.invoke()
        return "break"
    window.bind('<Control-d>', on_ctrl_d_transaction)
    tran_clear_button = HoverButton(tran_table_frame, text='Clear', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52',
                               width=8, command=lambda: clear_fields(transaction_id_entry, transaction_date_entry, transaction_time_entry, payment_type_combobox,payment_status_combobox, total_amount_entry, handled_by_entry, notes_text, True, treeview))
    tran_clear_button.place(x=310, y=580)

    def on_ctrl_c_transaction(event):
        tran_clear_button.invoke()
        return "break"

    window.bind('<Control-c>', on_ctrl_c_transaction)

    # Styling for the Treeview
    style = ttk.Style()
    style.theme_use('default')  # Use a theme that supports heading customization
    style.configure("Treeview.Heading", background="#ACB1CA", foreground="black", font=("Winky Rough", 12, "bold"))
    # Horizontal and Vertical Scrollbars Configuration on following lines of code
    horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient=HORIZONTAL, style="Horizontal.TScrollbar")
    vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient=VERTICAL, style="Vertical.TScrollbar")
    # Treeview Creation over treeview frame
    treeview = ttk.Treeview(treeview_frame, columns=(
        'transaction_id', 'transaction_date', 'transaction_time', 'payment_type', 'payment_status', 'total_amount', 'handled_by', 'notes'),
                            show='headings',
                            yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    # PACKING THE SCROLL BARS
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    # Naming the Headings of the Treeview
    treeview.heading('transaction_id', text='Transaction ID')
    treeview.heading('transaction_date', text='Transaction Date')
    treeview.heading('transaction_time', text='Transaction Time')
    treeview.heading('payment_type', text='Payment Type')
    treeview.heading('payment_status', text='Payment Status')
    treeview.heading('total_amount', text='Total Amount')
    treeview.heading('handled_by', text='Handled By')
    treeview.heading('notes', text='Notes')


    # Setting the width for the headings of the columns in the treeview
    treeview.column('transaction_id', width=120)
    treeview.column('transaction_date', width=150)
    treeview.column('transaction_time', width=150)
    treeview.column('payment_type', width=160)
    treeview.column('payment_status', width=140)
    treeview.column('total_amount', width=180)
    treeview.column('handled_by', width=180)
    treeview.column('notes', width=180)

    treeview.bind('<ButtonRelease-1>',
                  lambda event: select_data(event, transaction_id_entry, transaction_date_entry, transaction_time_entry,
                                            payment_type_combobox,
                                            payment_status_combobox,
                                            total_amount_entry,handled_by_entry, notes_text, treeview))



    def close_tran_table_frame(event=None):
        tran_table_frame.place_forget()
    window.bind("<Escape>", close_tran_table_frame)



    transaction_treeview(treeview)