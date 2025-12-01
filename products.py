from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox

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






def show_all(treeview, search_combobox, search_entry):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)







def search_product(search_combobox, search_entry, treeview):
    if search_combobox.get() == 'Search By':
        messagebox.showwarning('Warning', 'Please Select an Option')
    elif search_entry.get() == '':
        messagebox.showwarning('Warning', 'Please enter the value to search')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_management_system')
            column_name = search_combobox.get()
            query = "SELECT * FROM product_data WHERE {} = %s".format(column_name)
            cursor.execute(query, (search_entry.get(),))
            records = cursor.fetchall()
            if len(records) == 0:
                messagebox.showerror('Error', 'No Records have been Found')
                return
            treeview.delete(*treeview.get_children())
            for record in records:
                treeview.insert('', END, values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Due to {e}')
        finally:
            cursor.close()
            connection.close()








def clear_fields(category_combobox,supplier_combobox, name_entry,price_entry,quantity_entry,status_combobox, discount_spinbox,treeview):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select Category')
    supplier_combobox.set('Select Combobox')
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0,END)
    status_combobox.set('Select Status')
    discount_spinbox.delete(0, END)
    discount_spinbox.insert(0, 0)






def delete_product(treeview, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox, discount_spinbox):
    from dashboard import update_dashboard_counts
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No Row is Selected!')
        return

    dict = treeview.item(index)
    content = dict.get('values', [])

    if len(content) == 0:
        messagebox.showerror('Error', 'Selected row contains no data!')
        return

    id = content[0]
    ans = messagebox.askyesno('Confirm', 'Do You Really want to Delete the Record?')
    if ans:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_management_system')
            cursor.execute('DELETE FROM product_data WHERE id=%s', (id,))
            connection.commit()
            update_dashboard_counts()
            treeview_data(treeview)
            messagebox.showinfo('Info', 'Record has been Successfully Deleted!')
            clear_fields(category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox, discount_spinbox,treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Due to {e}')
        finally:
            cursor.close()
            connection.close()






def update_product(category, supplier, name, price,discount, quantity, status, treeview):
    from dashboard import update_dashboard_counts
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    if not index:
        messagebox.showerror('Error', 'No Row is Selected')
        return
    id=content[0]
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_management_system')
    cursor.execute('SELECT * FROM product_data WHERE id=%s', (id,))
    current_data = cursor.fetchone()
    current_data = current_data[1:]
    current_data = list(current_data[1:])
    current_data = list(current_data)
    current_data[3] = str(current_data[3])
    current_data[4] = str(current_data[4])

    del current_data[5]
    current_data=tuple(current_data)

    price = float(price)
    discount = float(discount)
    quantity = int(quantity)
    new_data = (category, supplier, name, price, discount,quantity, status)
    if current_data == new_data:
        messagebox.showinfo('Info', 'No Changes Detected')
        return
    discounted_price = round(float(price) * (1-float(discount) / 100), 2)
    cursor.execute('UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s, discount=%s,discounted_price=%s, quantity=%s, status=%s WHERE id=%s',(category, supplier, name, price,discount,discounted_price, quantity,status, id))
    connection.commit()
    update_dashboard_counts()
    messagebox.showinfo('Info', 'Data has been successfully Updated!')
    treeview_data(treeview)






def select_data(event, treeview, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox, discount_spinbox):
    index = treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    discount_spinbox.delete(0,END)

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0,content[3])
    price_entry.insert(0, content[4])
    discount_spinbox.insert(0, content[5])
    quantity_entry.insert(0, content[7])
    status_combobox.insert(0, content[8])







def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT * from product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()





def fetch_supplier_category(category_combobox, supplier_combobox):
    category_option = []
    supplier_option = []
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_management_system')
    cursor.execute('SELECT name from category_data')
    names = cursor.fetchall()
    if len(names) > 0:
        category_combobox.set("Select Category")
        for name in names:
            category_option.append(name[0])
        category_combobox.config(values=category_option)
    cursor.execute('SELECT name from supplier_data')
    names = cursor.fetchall()
    if len(names) > 0:
        supplier_combobox.set('Select Supplier')
        for name in names:
            supplier_option.append(name[0])
        supplier_combobox.config(values=supplier_option)






def add_product(category, supplier, name, price,discount, quantity, status, treeview):
    from dashboard import update_dashboard_counts
    if category == 'Empty':
        messagebox.showerror('Error', 'Please Add Category!')
    elif supplier == 'Empty':
        messagebox.showerror('Error', 'Please Add Suppliers!')
    elif category == 'Select' or supplier == 'Select' or name == '' or price =='' or quantity == '' or status == 'Select Status':
        messagebox.showerror('Error', "All Fields are Required!")
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_management_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(100), '
                       'supplier VARCHAR(100), name VARCHAR(100), price DECIMAL(10,2), quantity INT, status VARCHAR(50))')
        cursor.execute('SELECT * FROM product_data WHERE category=%s AND supplier=%s AND name=%s',(category, supplier, name))
        existing_product = cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error', 'Product Already Exists')
            return
        discounted_price = round(float(price)*(1-float(discount)/100),2) # the formula to find the discounted price
        cursor.execute('INSERT INTO product_data (category, supplier, name, price, discount, discounted_price, quantity, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(category, supplier, name, price,discount, discounted_price, quantity, status))


        connection.commit()
        update_dashboard_counts()
        messagebox.showinfo('Success', 'Data has been successfully Added!')
        treeview_data(treeview) # Displaying the data into the treeview of the GUI too








# Product Form GUI
def product_form(window):
    global back_image
    # Overall Product Frame
    product_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    product_frame.place(x=0, y=123)

    heading_label = Label(product_frame, text="Manage Product Details", font=('Winky Rough', 16, 'bold'),
                          bg='#193B52', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # Back Image
    back_image = PhotoImage(file='images/back.png')
    # Back Button
    back_button = Button(product_frame, image=back_image, bd=0, cursor='hand2',
                         command=lambda: product_frame.place_forget(), bg='#ACB1CA', activebackground='#ACB1CA')
    back_button.place(x=10, y=37)

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(product_frame, image=information_image, bd=0, cursor='hand2',
                                command=lambda: show_info_popup(information_button), bg='#193B52',
                                activebackground='#193B52')
    information_button.image = information_image  # prevent garbage collection
    information_button.place(x=10, y=8)  # or .grid(...) as per your layout


    # Left Frame
    left_frame = Frame(product_frame, bg='#ACB1CA', relief=RIDGE, bd=1)
    left_frame.place(x=120, y=62)
    # Heading Label
    heading_label = Label(left_frame, text="Manage Product Details", font=('Winky Rough', 14, 'bold'), bg='#193B52',
                          fg='white')
    heading_label.grid(row=0, columnspan=2, sticky='we')
    # Category Label
    category_label = Label(left_frame, text="Category", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    category_label.grid(row=1, column=0, padx=20, sticky='w')
    # Category Combobox
    category_combobox = ttk.Combobox(left_frame, font=('Winky Rough', 14, 'bold'), width=19, state='readonly')
    category_combobox.grid(row=1, column=1,pady=40)
    category_combobox.set('Empty')
    # Supplier Label
    supplier_label = Label(left_frame, text="Supplier", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    supplier_label.grid(row=2, column=0, padx=20, sticky='w')
    # Supplier Combobox
    supplier_combobox = ttk.Combobox(left_frame, font=('Winky Rough', 14, 'bold'), width=19, state='readonly')
    supplier_combobox.grid(row=2, column=1)
    supplier_combobox.set('Empty')
    # Name Label
    name_label = Label(left_frame, text="Name", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    name_label.grid(row=3, column=0, padx=20, sticky='w')
    name_entry = Entry(left_frame, font=('Winky Rough', 14, 'bold'), bg='white')
    name_entry.grid(row=3, column=1, pady=30)
    # Price Label
    price_label = Label(left_frame, text="Price", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    price_label.grid(row=4, column=0, padx=20, sticky='w')
    price_entry = Entry(left_frame, font=('Winky Rough', 14, 'bold'), bg='white')
    price_entry.grid(row=4, column=1)

    discount_label = Label(left_frame, text="Discount (%)", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    discount_label.grid(row=5, column=0, padx=20, sticky='w', pady=(20,0))

    discount_spinbox = Spinbox(left_frame, from_=0, to=100, font=('Winky Rough', 14, 'bold'), width=19)
    discount_spinbox.grid(row=5, column=1, pady=(20,0))
    # Quantity Label
    quantity_label = Label(left_frame, text="Quantity", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    quantity_label.grid(row=6, column=0, padx=20, sticky='w')
    quantity_entry = Entry(left_frame, font=('Winky Rough', 14, 'bold'), bg='white', width=20)
    quantity_entry.grid(row=6, column=1,pady=30)
    # Status Label
    status_label = Label(left_frame, text="Status", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    status_label.grid(row=7, column=0, padx=20, sticky='w')
    status_combobox = ttk.Combobox(left_frame, values=('Active', 'Inactive'), font=('Winky Rough', 14, 'bold'), width=19, state='readonly')
    status_combobox.grid(row=7, column=1)
    status_combobox.set('Select Status')
    # Buttons Frame
    button_frame = Frame(left_frame, bg='#ACB1CA')
    button_frame.grid(row=8, columnspan=2, pady=(30,10))
    # Add Button
    add_button = HoverButton(button_frame, text='Add', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2', fg='white', bg='#193B52', command=lambda:add_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), discount_spinbox.get(),quantity_entry.get(),status_combobox.get(), treeview))
    add_button.grid(row=0, column=0, padx=10)

    def on_ctrl_a(event):
        add_button.invoke()
        return "break"

    window.bind('<Control-a>', on_ctrl_a)


    # Update Button
    update_button = HoverButton(button_frame, text='Update', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2', fg='white',
                        bg='#193B52', command=lambda:update_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(),discount_spinbox.get(), quantity_entry.get(),status_combobox.get(), treeview))
    update_button.grid(row=0, column=1, padx=10)
    def on_ctrl_u(event):
        update_button.invoke()
        return "break"

    window.bind('<Control-u>', on_ctrl_u)

    # Delete Button
    delete_button = HoverButton(button_frame, text='Delete', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2',
                           fg='white',
                           bg='#193B52', command=lambda:delete_product(treeview, category_combobox,supplier_combobox, name_entry,price_entry,quantity_entry,status_combobox, discount_spinbox))
    delete_button.grid(row=0, column=2, padx=10)
    def on_ctrl_d(event):
        delete_button.invoke()
        return "break"

    window.bind('<Control-d>', on_ctrl_d)

    # Clear Button
    clear_button = HoverButton(button_frame, text='Clear', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2',
                           fg='white',
                           bg='#193B52', command=lambda:clear_fields(category_combobox,supplier_combobox, name_entry,price_entry,quantity_entry,status_combobox, discount_spinbox,treeview))
    clear_button.grid(row=0, column=3, padx=10)
    def on_ctrl_c(event):
        clear_button.invoke()
        return "break"
    window.bind('<Control-c>', on_ctrl_c)

    # Search Frame



    search_frame = LabelFrame(product_frame, text='Search Product', font=('times new roman', 14, 'bold'), bg='#ACB1CA', bd=2)
    search_frame.place(x=800, y=60)

    search_combobox = ttk.Combobox(search_frame, values=('Category', 'Supplier', 'Name', 'Status'), state='readonly', width=16, font=('times new roman', 14, 'bold'))
    search_combobox.grid(row=0, column=0, padx=10)
    search_combobox.set('Search By')
    search_entry = Entry(search_frame, font=('Winky Rough', 14, 'bold'), bg='white', width=16)
    search_entry.grid(row=0, column=1)

    search_button = HoverButton(search_frame, text='Search', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2',
                           fg='white',
                           bg='#193B52', command=lambda:search_product(search_combobox, search_entry, treeview))
    search_button.grid(row=0, column=2, padx=(10,0), pady=10)

    show_button = HoverButton(search_frame, text='Show All', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2',
                           fg='white',
                           bg='#193B52', command=lambda:show_all(treeview, search_combobox, search_entry))
    show_button.grid(row=0, column=3, padx=10)

    # Creating a Treeview here at this point

    treeview_frame = Frame(product_frame)
    treeview_frame.place(x=800, y=160, width=590, height=480)

    style = ttk.Style()
    style.theme_use('default')  # Use a theme that supports heading customization
    style.configure("Treeview.Heading", background="#ACB1CA", foreground="black", font=("Winky Rough", 12, "bold"))

    horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient=HORIZONTAL, style="Horizontal.TScrollbar")
    vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient=VERTICAL, style="Vertical.TScrollbar")

    treeview = ttk.Treeview(treeview_frame, columns=('id','category', 'supplier', 'name', 'price','discount','discounted_price', 'quantity', 'status'), show='headings',
                            yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    # PACKING THE SCROLL BARS
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('category', text='Category')
    treeview.heading('supplier', text='Supplier')
    treeview.heading('name', text='Product Name')
    treeview.heading('price', text='Price')
    treeview.heading('discount', text='Discount')
    treeview.heading('discounted_price', text='Discounted Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')

    treeview.column('id', width=60)
    treeview.column('category', width=120)
    treeview.column('supplier', width=120)
    treeview.column('name', width=120)
    treeview.column('price', width=120)
    treeview.column('discount', width=120)
    treeview.column('discounted_price', width=120)
    treeview.column('quantity', width=120)
    treeview.column('status', width=120)
    fetch_supplier_category(category_combobox, supplier_combobox)
    treeview_data(treeview)

    treeview.bind('<ButtonRelease-1>', lambda event :select_data(event, treeview, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox, discount_spinbox))




    def close_prod_frame(event=None):
        product_frame.place_forget()
    window.bind("<Escape>", close_prod_frame)
    return product_frame













