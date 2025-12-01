from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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








def delete_supplier(invoice, treeview):
    from dashboard import update_dashboard_counts
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No Row is Selected!')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s', (invoice,))
        connection.commit()
        update_dashboard_counts()
        treeview_data(treeview)
        messagebox.showinfo('Info','Record has been Successfully Deleted!')
    except Exception as e:
        messagebox.showerror('Error', f'Due to {e}')
    finally:
        cursor.close()
        connection.close()


def clear(invoice_entry, name_entry, contact_entry, description_text, treeview):
    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())


def search_supplier(search_value, treeview):
    if search_value == "":
        messagebox.showerror('Error', 'Please Enter Invoice No')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s',(search_value,))
            record=cursor.fetchone()
            if not record:
                messagebox.showerror('Error', 'No Record Found')
                return
            treeview.delete(*treeview.get_children())
            treeview.insert("", END, values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()



def show_all(treeview, search_entry):
    treeview_data(treeview)
    search_entry.delete(0, END)





def update_supplier(invoice, name, contact, description, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No Row is Selected!')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', (invoice,))
        current_data = cursor.fetchone()
        current_data = current_data[1:]

        new_data = (name, contact, description)

        if current_data == new_data:
            messagebox.showinfo('Info', 'No Changes has been detected')
            return

        cursor.execute('UPDATE supplier_data SET name=%s, contact=%s, description=%s WHERE invoice=%s',(name, contact, description, invoice))
        connection.commit()
        messagebox.showinfo('Info', 'Data has been Successfully Updated!')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()








def select_data(invoice_entry, name_entry, contact_entry, description_text, treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content = content['values']
    if not actual_content:  # Check if the selected row has data
        messagebox.showerror('Error', 'No data available in the selected row!')
        return
    # These 4 Lines of code will delete all the data prior to selecting other rows,
    # cause if we don't delete the previous selected it will be merged with the next selected row's data
    invoice_entry.delete(0,END)
    name_entry.delete(0, END)
    contact_entry.delete(0,END)
    description_text.delete(1.0, END)
    # These 4 Lines of code will select all the datas from the 4 fields of
    # invoice, name, contact, description and will bring it into the entries
    invoice_entry.insert(0, actual_content[0])
    name_entry.insert(0, actual_content[1])
    contact_entry.insert(0, actual_content[2])
    description_text.insert(1.0, actual_content[3])


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT * FROM supplier_data')
        records = cursor.fetchall()
        treeview.delete(* treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()

def add_supplier(invoice, name, contact, description, treeview):
    from dashboard import update_dashboard_counts
    if invoice == '' or name=='' or contact == '' or description == "":
        messagebox.showerror('Error', 'All fields are Required!')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_management_system')


            cursor.execute('CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY, name VARCHAR(100), contact VARCHAR(100), description TEXT)')

            cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', (invoice,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'ID already Exists')
                return
            cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s)', (invoice, name, contact, description))
            connection.commit()
            update_dashboard_counts()
            messagebox.showinfo('Info', 'The Data has been Successfully Inserted')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()








def supplier_form(window):
    global back_image
    supplier_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    supplier_frame.place(x=0, y=123)

    heading_label = Label(supplier_frame, text="Manage Supplier Details", font=('Winky Rough', 16, 'bold'), bg='#193B52', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='images/back.png')
    back_button = Button(supplier_frame, image=back_image, bd=0, cursor='hand2', command=lambda: supplier_frame.place_forget(), bg='#ACB1CA', activebackground='#ACB1CA') # the .place_forget() methods gets the frame backs the menu (closes it)
    back_button.place(x=10, y=37)

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(supplier_frame, image=information_image, bd=0, cursor='hand2',
                                command=lambda: show_info_popup(information_button), bg='#193B52',
                                activebackground='#193B52')
    information_button.image = information_image  # prevent garbage collection
    information_button.place(x=10, y=8)  # or .grid(...) as per your layout


    # Left Frame on the Supplier Frame
    left_frame = Frame(supplier_frame, bg='#ACB1CA', relief=RIDGE, bd=2)
    left_frame.place(x=130, y=130, width=570, height=360)

    left_frame_title = Label(supplier_frame, bg='#193B52', fg='white', text="Supplier Details", font=('Winky Rough', 16, 'bold'), width=51)
    left_frame_title.place(x=130, y=92)

    invoice_label = Label(left_frame, text='Invoice No', font=('Winky Rough', 14, 'bold'),bg='#ACB1CA')
    invoice_label.grid(row=0, column=0, padx=30, sticky='w')
    invoice_entry = Entry(left_frame, font=('Consolas', 14, 'bold'), bg='white')
    invoice_entry.grid(row=0, column=1)


    name_label = Label(left_frame, text='Supplier Name', font=('Winky Rough', 14, 'bold'),bg='#ACB1CA')
    name_label.grid(row=1, column=0, padx=30, pady=25,sticky='w')
    name_entry = Entry(left_frame, font=('Consolas', 14, 'bold'), bg='white')
    name_entry.grid(row=1, column=1)

    contact_label = Label(left_frame, text='Supplier Contact', font=('Winky Rough', 14, 'bold'),bg='#ACB1CA')
    contact_label.grid(row=2, column=0, padx=30 ,sticky='w')
    contact_entry = Entry(left_frame, font=('Consolas', 14, 'bold'), bg='white')
    contact_entry.grid(row=2, column=1)

    # Description
    description_label = Label(left_frame, text='Description', font=('Winky Rough', 14, 'bold'),bg='#ACB1CA')
    description_label.grid(row=3, column=0, padx=30,sticky='nw', pady=25)
    description_text = Text(left_frame, bg='white', width=25, height=3, bd=2)
    description_text.grid(row=3, column=1, pady=25)

    button_frame = Frame(left_frame,bg='#ACB1CA')
    button_frame.grid(row=6, columnspan=2)

    add_button = HoverButton(button_frame, text='Add', font=('Winky Rough', 14, 'bold'), width=10, cursor='hand2', fg='white', bg='#193B52', command=lambda:add_supplier(invoice_entry.get(),name_entry.get() ,contact_entry.get() , description_text.get(1.0, END).strip(), treeview))
    add_button.grid(row=0, column=0, padx=15)

    update_button = HoverButton(button_frame, text='Update', font=('Winky Rough', 14, 'bold'),width=10, cursor='hand2', fg='white', bg='#193B52', command=lambda:update_supplier(invoice_entry.get(),name_entry.get() ,contact_entry.get() , description_text.get(1.0, END).strip(), treeview))
    update_button.grid(row=0, column=1, padx=15)


    delete_button = HoverButton(button_frame, text='Delete', font=('Winky Rough', 14, 'bold'), width=10, cursor='hand2', fg='white', bg='#193B52', command=lambda:delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0, column=2, padx=15)



    clear_button = HoverButton(button_frame, text='Clear', font=('Winky Rough', 14, 'bold'), width=10, cursor='hand2', fg='white', bg='#193B52', command=lambda:clear(invoice_entry, name_entry, contact_entry, description_text, treeview))
    clear_button.grid(row=0, column=3, padx=15)



    # Right Frame for the Entries

    right_frame = Frame(supplier_frame,bg='#ACB1CA', relief=RIDGE, bd=2)
    right_frame.place(x=780, y=90, width=590, height=400)

    search_frame = Frame(right_frame,bg='#ACB1CA')
    search_frame.pack(pady=10)

    invoice_no_label = Label(search_frame, text='Invoice No', font=('Winky Rough', 14, 'bold'),bg='#ACB1CA')
    invoice_no_label.grid(row=0, column=0, padx=(0,10), sticky='w')
    search_entry = Entry(search_frame, font=('Consolas', 14, 'bold'), bg='white', width=14)
    search_entry.grid(row=0, column=1)

    search_button = HoverButton(search_frame, text='Search', font=('Winky Rough', 14, 'bold'), width=10, cursor='hand2',
                          fg='white', bg='#193B52', command=lambda:search_supplier(search_entry.get(), treeview))
    search_button.grid(row=0, column=2, padx=10)



    show_button = HoverButton(search_frame, text='Show All', font=('Winky Rough', 14, 'bold'), width=10, cursor='hand2',
                          fg='white', bg='#193B52', command=lambda:show_all(treeview,search_entry))
    show_button.grid(row=0, column=3, padx=10)


    # Pre Styling of the Scrollbars using style method of ttk
    style = ttk.Style()
    style.theme_use("default")  # Use a theme that supports color customization
    style.configure("Horizontal.TScrollbar", background="#ACB1CA", troughcolor="#ACB1CA", arrowcolor="black")
    style.configure("Vertical.TScrollbar", background="#ACB1CA", troughcolor="#ACB1CA", arrowcolor="black")
    # Adding The Scrollbars to the Treeview
    vertical_scrollbar = ttk.Scrollbar(right_frame, orient=VERTICAL, style="Vertical.TScrollbar")
    horizontal_scrollbar = ttk.Scrollbar(right_frame, orient=HORIZONTAL, style="Horizontal.TScrollbar")


    treeview = ttk.Treeview(right_frame, columns=('invoice', 'name', 'contact', 'description'), show="headings", yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('invoice', text='Invoice ID')
    treeview.heading('name', text='Supplier Name')
    treeview.heading('contact', text='Supplier Contact')
    treeview.heading('description', text='Description')


    treeview.column('invoice', width=100)
    treeview.column('name', width=170)
    treeview.column('contact', width=150)
    treeview.column('description', width=230)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(invoice_entry, name_entry, contact_entry, description_text, treeview))



    # This function is for the Updating Button Function Using Control+U as Keyboard Shortcut
    window.bind("<Control-u>", lambda event: update_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(),
                                                             description_text.get(1.0, END).strip(), treeview))



    # These lines of codes using binding methods are used for Keyboard Shortcuts for the buttons inside the Supplier Form
    window.bind("<Control-u>",lambda event: update_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(),
                                                  description_text.get(1.0, END).strip(), treeview))
    window.bind("<Control-c>",lambda event: clear(invoice_entry, name_entry, contact_entry, description_text, treeview))
    window.bind("<Control-s>",lambda event: add_supplier(invoice_entry.get(), name_entry.get(), contact_entry.get(),
                                               description_text.get(1.0, END).strip(), treeview))
    window.bind("<Control-d>", lambda event: delete_supplier(invoice_entry.get(), treeview))



    def close_supplier_frame(event=None):
        supplier_frame.place_forget()
    window.bind("<Escape>", close_supplier_frame)


    return supplier_frame









