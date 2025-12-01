from tkinter import * # this imports anything from the tkinter
from tkinter import ttk # this imports ttk from the tkinter
from tkinter.ttk import Combobox # this imports the combobox field from the tkinter.ttk module
from tkcalendar import DateEntry # this will import the dateentry from the tkcalendar module
from customer_table import cust_table # this will import the customer table (another module of the same project)
from transaction_table import tran_table # this will import the transaction table (another module of the same project)
from employees import connect_database # this will import the employees module of the same project
from tkinter import messagebox # this will import the messagebox widget from the tkinter





# HOVER CLASS FOR THE BUTTONS AT THE FORM
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



def autofill_product_details(product_id_entry, product_name_combobox, category_combobox, purchase_price_entry):
    product_id = product_id_entry.get().strip()
    if not product_id.isdigit():
        return  # Optionally, show a warning or clear fields

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_management_system')
        cursor.execute('SELECT name, category, price FROM product_data WHERE id = %s', (product_id,))
        product = cursor.fetchone()

        if product:
            name, category, price = product

            product_name_combobox.set(name)
            category_combobox.set(category)
            purchase_price_entry.delete(0, END)
            purchase_price_entry.insert(0, price)
        else:
            # Clear fields if no product is found
            product_name_combobox.set('')
            category_combobox.set('')
            purchase_price_entry.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch product: {e}")
    finally:
        cursor.close()
        connection.close()


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



# Showing all the table data implementing the following show_all function.
def show_all(treeview, search_combobox, search_entry):
    sales_treeview(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)


def sales_treeview(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT * from sales_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()


# This function does add the product data through the button defined below in the GUI part of the code
def add_product_data(product_id, product_name, category, unit_of_measure, price_per_unit, purchase_price, selling_price,
                     quantity, expiry_date, discount, tax, sub_total, notes, treeview):
    if (
            product_id == '' or product_name == '' or quantity == '' or price_per_unit == '' or sub_total == '' or discount == '' or tax == '' or
            category == '' or unit_of_measure == 'Select Measurement' or purchase_price == '' or selling_price == '' or
            expiry_date == '\n' or notes == ''):
        messagebox.showerror('Error', 'All Fields are Required')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE inventory_management_system')
    try:
        # Remove duplicate ID check—allow multiple entries per product
        cursor.execute(
            'INSERT INTO sales_data (product_id, product_name, category, unit_of_measure, price_per_unit, purchase_price, selling_price, quantity, expiry_date, discount, tax, sub_total, notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (product_id, product_name, category, unit_of_measure, price_per_unit, purchase_price, selling_price,
             quantity, expiry_date, discount, tax, sub_total, notes))
        connection.commit()

        sales_treeview(treeview)
        messagebox.showinfo('Success', 'Data has been successfully added!')
    except Exception as e:
        messagebox.showerror('Error', f"Due to {e}")
    finally:
        cursor.close()
        connection.close()


def search_product_data(search_option, value, treeview):
    # Define mapping of user-friendly options to actual database column names
    column_mapping = {
        'Product ID': 'product_id',
        'Category': 'category',
        'Measurement': 'unit_of_measure',  # Adjust based on your actual column name
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
        cursor.execute(f"SELECT * FROM sales_data WHERE {actual_column} LIKE %s", (f"%{value}%",))
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, value=record)

    except Exception as e:
        messagebox.showerror('Error', f"Due to {e}")
    finally:
        cursor.close()
        connection.close()


def delete_product_data(product_id, treeview):
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
                cursor.execute('DELETE FROM sales_data WHERE product_id=%s',(product_id,))
                connection.commit()
                sales_treeview(treeview)
                messagebox.showinfo('Success', 'Record has been Successfully Deleted')
            except Exception as e:
                messagebox.showerror('Error', f"Due to {e}")
            finally:
                cursor.close()
                connection.close()

def update_product_data(product_id, product_name, category, unit_of_measure, price_per_unit, purchase_price, selling_price, quantity, expiry_date, discount, tax, sub_total, notes,treeview):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No Row is Selected')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:  # if cursor and connection are not met the connection will not be established
            return
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute('SELECT * from sales_data WHERE product_id=%s',(product_id,))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            new_data = (product_id, product_name, category, unit_of_measure, price_per_unit, purchase_price, selling_price, quantity, expiry_date, discount,
                        tax, sub_total, notes)
            if current_data == new_data:
                messagebox.showinfo('Information', "No changes Detected")
                return
            cursor.execute(
                'UPDATE sales_data SET product_name=%s, category=%s, unit_of_measure=%s, price_per_unit=%s, purchase_price=%s, selling_price=%s, quantity=%s, expiry_date=%s, discount=%s, tax=%s, sub_total=%s, notes=%s WHERE product_id=%s',
                (product_name, category, unit_of_measure, price_per_unit, purchase_price, selling_price, quantity, expiry_date, discount,
                        tax, sub_total, notes,product_id,))
            connection.commit()
            sales_treeview(treeview) # in this section all the updated data will be shown in the Treeview of the GUI on the Upper Frame inside the Employee Button
            messagebox.showinfo('Success', 'Data has been successfully Updated')
        except Exception as e:
            messagebox.showerror('Error', f"Due to {e}")
        finally:
            cursor.close()
            connection.close()


# This function will select the data selected in the treeview to entry fields
def select_data(event, product_id_entry, product_name_combobox, category_combobox, unit_of_measure_combobox, price_unit_entry,
                purchase_price_entry, selling_price_entry, quantity_entry,
                expiry_date_entry, discount_spinbox, tax_spinbox, subtotal_entry,
                notes_text_entry, treeview):
    # Get the selected item
    index = treeview.selection()
    if not index:
        # No item is selected
        messagebox.showerror('Error', 'No Item is selected')
        return
    # Get item content
    content = treeview.item(index)
    row = content.get('values')
    if not row or len(row) < 13:  # Ensure row is not empty and has enough elements
        print("Invalid or missing data in the selected row.")
        return
    # Clear the fields
    clear_fields(product_id_entry, product_name_combobox, category_combobox, unit_of_measure_combobox, price_unit_entry,
                 purchase_price_entry, selling_price_entry, quantity_entry,
                 expiry_date_entry, discount_spinbox, tax_spinbox, subtotal_entry,
                 notes_text_entry, treeview, False)
    # Populate the fields
    product_id_entry.insert(0, row[0])
    product_name_combobox.set(row[1])
    category_combobox.set(row[2])
    unit_of_measure_combobox.set(row[3])
    price_unit_entry.insert(0, row[4])
    purchase_price_entry.insert(0, row[5])
    selling_price_entry.insert(0, row[6])
    quantity_entry.insert(0, row[7])
    expiry_date_entry.set_date(row[8])
    discount_spinbox.insert(0, row[9])
    tax_spinbox.insert(0, row[10])
    subtotal_entry.insert(0, row[11])
    notes_text_entry.insert("1.0", row[12])


# This function is implemented to Clear all the Entry field including dates in the Product Frame inside Sales Form
def clear_fields(product_id_entry, product_name_combobox, category_combobox, unit_of_measure_combobox, price_unit_entry,
                 purchase_price_entry, selling_price_entry, quantity_entry, expiry_date_entry, discount_spinbox,
                 tax_spinbox, subtotal_entry, notes_text_entry, check, treeview):
    product_id_entry.delete(0, END)
    product_name_combobox.set('Select Product')
    category_combobox.set('Select Category')
    unit_of_measure_combobox.set('Select Measurement')
    price_unit_entry.delete(0, END)
    purchase_price_entry.delete(0, END)
    selling_price_entry.delete(0, END)
    quantity_entry.delete(0, END)

    from datetime import date
    expiry_date_entry.set_date(date.today())

    discount_spinbox.delete(0, END)
    discount_spinbox.insert(0, "0")
    tax_spinbox.delete(0, END)
    tax_spinbox.insert(0, "0")
    subtotal_entry.configure(state='normal')  # Enable editing
    subtotal_entry.delete(0, END)
    notes_text_entry.delete("1.0", END)  # Ensure proper text index

    if check and treeview:
        treeview.selection_remove(treeview.selection())





# This will avoid the over flapping of the sales menu
current_frame = None
def show_form_sales(form_function, window):
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame=form_function(window)




# GUI PART OF THE SALES FORM
def sales_form(window):
    global back_image

    sales_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    sales_frame.place(x=0, y=123)
    heading_label = Label(sales_frame, text="Manage Sales' Details", font=('Winky Rough', 16, 'bold'),
                          bg='#193B52',
                          fg='white')
    heading_label.place(x=0, y=0, relwidth=1)


    back_image = PhotoImage(file='images/back.png')
    back_button = Button(sales_frame, image=back_image, bd=0, cursor='hand2',
                         command=lambda: sales_frame.place_forget(), bg='#ACB1CA',
                         activebackground='#ACB1CA',)  # the .place_forget() methods gets the frame backs the menu (closes it)
    back_button.place(x=10, y=37)

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(sales_frame, image=information_image, bd=0, cursor='hand2',
                                command=lambda: show_info_popup(information_button), bg='#193B52', activebackground='#193B52')
    information_button.image = information_image  # prevent garbage collection
    information_button.place(x=10, y=8)  # or .grid(...) as per your layout

    customer_details_button = HoverButton(heading_label, text='Customer Table', font=('Winky Rough', 12, 'bold'), bg='#193B52', fg='white', width=15, relief=FLAT, activebackground='#193B52',cursor='hand2',command = lambda: show_form_sales(cust_table,window))
    customer_details_button.place(x=1100, y=0)

    transaction_summary_button = HoverButton(heading_label, text='Transaction Summary', font=('Winky Rough', 12, 'bold'), bg='#193B52', fg='white', width=20, relief=FLAT, activebackground='#193B52',cursor='hand2', command = lambda: show_form_sales(tran_table, window))
    transaction_summary_button.place(x=1240, y=0)






    # Product Details Frame of the Window
    product_frame = Frame(sales_frame, bg='#ACB1CA', height=465, bd=1, relief=RIDGE, width=520)
    product_frame.place(x=60, y=63)


    # Title of the Frame

    heading_label = Label(product_frame, text="Product Details", font=('Winky Rough', 14, 'bold'), bg='#193B52',
                          fg='white', bd=5, width=33)
    heading_label.grid(row=0, columnspan=2, sticky='we')

    product_id_label = Label(product_frame, text="Product ID", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    product_id_label.grid(row=1, column=0, padx=10, pady=2, sticky='w')



    product_id_entry = Entry(product_frame, font=('Winky Rough', 12, 'bold'), bg='white')
    product_id_entry.grid(row=1, column=1)

    product_name_label = Label(product_frame, text='Product Name', font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    product_name_label.grid(row=2, column=0, padx=10, pady=2, sticky='w')

    product_name_combobox = Combobox(product_frame, font=('Winky Rough', 12, 'bold'), state='readonly', width=19)
    product_name_combobox.set('Select Product')
    product_name_combobox.grid(row=2, column=1)

    category_label = Label(product_frame, text="Category", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    category_label.grid(row=3, column=0, padx=10, pady=2, sticky='w')

    category_combobox = Combobox(product_frame, font=('Winky Rough', 12, 'bold'), state='readonly', width=19)
    category_combobox.grid(row=3, column=1)
    category_combobox.set("Select Category")  # default value

    unit_of_measure_label = Label(product_frame, text="Unit of Measure", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    unit_of_measure_label.grid(row=4, column=0, padx=10, pady=2, sticky='w')

    unit_of_measure_combobox = ttk.Combobox(product_frame, font=('Winky Rough', 12, 'bold'), state='readonly', values=(
    'kg', 'lb', 'oz', 'mL', 'gallons', 'm', 'cm', 'inches', 'Feet', 'pieces', 'packs', 'boxes', 'sheets', 'cartons'), width=19)
    unit_of_measure_combobox.grid(row=4, column=1)
    unit_of_measure_combobox.set('Select Measurement')

    price_unit_label = Label(product_frame, text="Price per Unit", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    price_unit_label.grid(row=5, column=0, padx=10, pady=2, sticky='w')

    price_unit_entry = Entry(product_frame, font=('Winky Rough', 12, 'bold'), bg='white')
    price_unit_entry.grid(row=5, column=1)

    purchase_price_label = Label(product_frame, text="Purchase Price", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    purchase_price_label.grid(row=6, column=0, padx=10, pady=2, sticky='w')

    purchase_price_entry = Entry(product_frame, font=('Winky Rough', 12, 'bold'), bg='white')
    purchase_price_entry.grid(row=6, column=1)

    selling_price_label = Label(product_frame, text="Selling Price", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    selling_price_label.grid(row=7, column=0, padx=10, pady=2, sticky='w')

    selling_price_entry = Entry(product_frame, font=('Winky Rough', 12, 'bold'), bg='white')
    selling_price_entry.grid(row=7, column=1)

    quantity_label = Label(product_frame, text="Quantity", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    quantity_label.grid(row=8, column=0, padx=10, pady=2, sticky='w')

    quantity_entry = Entry(product_frame, font=('Winky Rough', 12, 'bold'), bg='white')
    quantity_entry.grid(row=8, column=1)

    expiry_date_label = Label(product_frame, text="Expiry Date", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    expiry_date_label.grid(row=9, column=0, padx=10, pady=2, sticky='w')

    expiry_date_entry = DateEntry(product_frame, font=('Winky Rough', 12, 'bold'), bg='white', state='readonly',
                                  date_pattern='dd/mm/yyyy', width=19)
    expiry_date_entry.grid(row=9, column=1)

    discount_label = Label(product_frame, text="Discount %", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    discount_label.grid(row=10, column=0, padx=10, pady=3, sticky='w')

    discount_spinbox = Spinbox(product_frame, from_=0, to=100, increment=1, font=('Winky Rough', 12, 'bold'),
                               bg='white', width=19)
    discount_spinbox.grid(row=10, column=1)

    tax_label = Label(product_frame, text="Tax %", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    tax_label.grid(row=11, column=0, padx=10, pady=3, sticky='w')

    tax_spinbox = Spinbox(product_frame, from_=0, to=100, increment=1, font=('Winky Rough', 12, 'bold'),
                               bg='white', width=19)
    tax_spinbox.grid(row=11, column=1)

    subtotal_label = Label(product_frame, text="Sub Total", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    subtotal_label.grid(row=12, column=0, padx=10, pady=3, sticky='w')

    subtotal_entry = Entry(product_frame, font=('Winky Rough', 12, 'bold'), bg='white', state='readonly')
    subtotal_entry.grid(row=12, column=1)

    notes_text_label = Label(product_frame, text="Notes", font=('Winky Rough', 12, 'bold'), bg='#ACB1CA')
    notes_text_label.grid(row=13, column=0, padx=10, pady=5, sticky='w')

    notes_text_entry = Text(product_frame, font=('Winky Rough', 12, 'bold'), bg='white', width=20, height=2)
    notes_text_entry.grid(row=13, column=1)


    # Treeview Frame

    treeview_frame = Frame(sales_frame, bg='#ACB1CA')
    treeview_frame.place(x=500, y=125, width=970 , height=448)

    # Center-align widgets in the search_frame
    search_frame = LabelFrame(sales_frame, bg='#ACB1CA', font=('Winky Rough', 10, 'bold'))
    search_frame.place(x=500, y=53, width=970, height=70)

    search_frame.grid_propagate(False)  # Prevent resizing due to widgets
    search_frame.grid_rowconfigure(0, weight=2)  # Adjust row height
    search_frame.grid_columnconfigure((0, 1, 3, 4), weight=1)  # Adjust column width

    search_combobox = ttk.Combobox(search_frame, values=('Product ID', 'Category', 'Measurement'), state='readonly',
                                   width=15, font=('Winky Rough', 16, 'bold'))
    search_combobox.grid(row=0, column=0, padx=10, pady=10, ipady=4, sticky='ew')  # Align horizontally
    search_combobox.set('Search By')

    search_entry = Entry(search_frame, font=('Winky Rough', 14, 'bold'), bg='white', width=15)
    search_entry.grid(row=0, column=1, padx=10, pady=10, ipady=4, sticky='ew')  # Align horizontally

    search_button = HoverButton(search_frame, bg='#193B52', fg='white', width=8, text='Search',
                           font=('Winky Rough', 13, 'bold'), command=lambda:search_product_data(search_combobox.get(),search_entry.get(),treeview))
    search_button.grid(row=0, column=3, padx=10, pady=10, sticky='ew')  # Align horizontally

    show_all_button = HoverButton(search_frame, bg='#193B52', fg='white', width=8, text='Show All',
                             font=('Winky Rough', 13, 'bold'),
                             command=lambda: show_all(treeview, search_combobox, search_entry))
    show_all_button.grid(row=0, column=4, padx=10, pady=10, sticky='ew')  # Align horizontally

    # Styling for the Treeview
    style = ttk.Style()
    style.theme_use('default')  # we use a theme that supports heading customization of the treeview.
    style.configure("Treeview.Heading", background="#ACB1CA", foreground="black", font=("Winky Rough", 12, "bold"))
    # Horizontal and Vertical Scrollbars Configuration on following lines of code
    horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient=HORIZONTAL, style="Horizontal.TScrollbar")
    vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient=VERTICAL, style="Vertical.TScrollbar")
    # Treeview Creation over treeview frame
    treeview = ttk.Treeview(treeview_frame, columns=(
    'product_id', 'product_name', 'category', 'unit_of_measure', 'price_per_unit', 'purchase_price', 'selling_price', 'quantity', 'expiry_date','discount','tax','sub_total', 'notes'),
                            show='headings',
                            yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    # PACKING THE SCROLL BARS
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    # Naming the Headings of the Treeview
    treeview.heading('product_id', text='Product ID')
    treeview.heading('product_name', text='Product Name')
    treeview.heading('category', text='Category')
    treeview.heading('unit_of_measure', text='Unit of Measure')
    treeview.heading('price_per_unit', text='Price/Unit')
    treeview.heading('purchase_price', text='Purchase Price')
    treeview.heading('selling_price', text='Selling Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('expiry_date', text='Expiry Date')
    treeview.heading('discount', text='Discount')
    treeview.heading('tax', text='Tax')
    treeview.heading('sub_total', text='Sub Total')
    treeview.heading('notes', text='Notes')
    # Setting the width for the headings of the columns in the treeview
    treeview.column('product_id', width=120)
    treeview.column('product_name', width=120)
    treeview.column('category', width=120)
    treeview.column('unit_of_measure',width=120)
    treeview.column('price_per_unit', width=120)
    treeview.column('purchase_price', width=120)
    treeview.column('selling_price',width=120)
    treeview.column('quantity', width=120)
    treeview.column('expiry_date',width=120)
    treeview.column('discount',width=120)
    treeview.column('tax', width=120)
    treeview.column('sub_total', width=120)
    treeview.column('notes', width=120)


    # BUTTONS SECTION



    prod_add_button = HoverButton(sales_frame, text='Add', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52', width=8, command=lambda:add_product_data(product_id_entry.get(),product_name_combobox.get(), category_combobox.get(),unit_of_measure_combobox.get(),price_unit_entry.get(), purchase_price_entry.get(),selling_price_entry.get() ,quantity_entry.get(),expiry_date_entry.get() ,discount_spinbox.get(),tax_spinbox.get(),subtotal_entry.get(),notes_text_entry.get(1.0, END), treeview))
    prod_add_button.place(x=70, y=580)

    def on_ctrl_a_sales(event):
        prod_add_button.invoke()
        return "break"
    window.bind('<Control-a>', on_ctrl_a_sales)

    prod_update_button = HoverButton(sales_frame, text='Update', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52', width=8, command= lambda : update_product_data(product_id_entry.get(), product_name_combobox.get(), category_combobox.get(), unit_of_measure_combobox.get(), price_unit_entry.get(),purchase_price_entry.get(), selling_price_entry.get(),quantity_entry.get(),expiry_date_entry.get(), discount_spinbox.get(),tax_spinbox.get(),subtotal_entry.get(),notes_text_entry.get(1.0, END), treeview))
    prod_update_button.place(x=150, y=580)
    def on_ctrl_u_sales(event):
        prod_update_button.invoke()
        return "break"
    window.bind('<Control-u>', on_ctrl_u_sales)
    prod_delete_button = HoverButton(sales_frame, text='Delete', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52', width=8, command=lambda:delete_product_data(product_id_entry.get(), treeview))
    prod_delete_button.place(x=230, y=580)
    def on_ctrl_d_sales(event):
        prod_delete_button.invoke()
        return "break"
    window.bind('<Control-d>', on_ctrl_d_sales)
    prod_clear_button = HoverButton(sales_frame, text='Clear', font=('Winky Rough', 12, 'bold'), fg='white', bg='#193B52', width=8, command=lambda: clear_fields(product_id_entry, product_name_combobox,category_combobox, unit_of_measure_combobox, price_unit_entry, purchase_price_entry, selling_price_entry, quantity_entry,expiry_date_entry,discount_spinbox, tax_spinbox,subtotal_entry,notes_text_entry, True, treeview))
    prod_clear_button.place(x=310, y=580)
    def on_ctrl_c_sales(event):
        prod_clear_button.invoke()
        return "break"

    window.bind('<Control-c>', on_ctrl_c_sales)


    treeview.bind('<ButtonRelease-1>',
                        lambda event: select_data(event, product_id_entry, product_name_combobox, category_combobox,
                                                  unit_of_measure_combobox,
                                                  price_unit_entry,
                                                  purchase_price_entry, selling_price_entry, quantity_entry,
                                                  expiry_date_entry, discount_spinbox, tax_spinbox, subtotal_entry,
                                                  notes_text_entry, treeview))

    product_id_entry.bind("<FocusOut>", lambda event: autofill_product_details(
        product_id_entry, product_name_combobox, category_combobox, purchase_price_entry))





    def load_categories():
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('USE inventory_management_system')
            cursor.execute('SELECT name FROM category_data')
            records = cursor.fetchall()
            category_names = [record[0] for record in records]
            category_combobox['values'] = category_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {e}")
        finally:
            cursor.close()
            connection.close()

    def load_products():
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('USE inventory_management_system')
            cursor.execute('SELECT name FROM product_data')
            records = cursor.fetchall()
            product_names = [record[0] for record in records]
            product_name_combobox['values'] = product_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")
        finally:
            cursor.close()
            connection.close()




    load_products()
    load_categories()

    def calculate_subtotal(*args):
        try:
            quantity = int(quantity_entry.get()) if quantity_entry.get() else 0
            selling_price = float(selling_price_entry.get()) if selling_price_entry.get() else 0.0
            subtotal = quantity * selling_price

            # Enable editing the readonly entry temporarily
            subtotal_entry.configure(state='normal')
            subtotal_entry.delete(0, END)
            subtotal_entry.insert(0, f"{subtotal:.2f}")
            subtotal_entry.configure(state='readonly')

        except ValueError:
            pass  # Prevents error if non-numeric value is entered

    quantity_entry.bind("<KeyRelease>", calculate_subtotal)
    selling_price_entry.bind("<KeyRelease>", calculate_subtotal)

    def calculate_final_subtotal(*args):
        try:
            quantity = int(quantity_entry.get()) if quantity_entry.get() else 0
            selling_price = float(selling_price_entry.get()) if selling_price_entry.get() else 0.0
            discount = float(discount_spinbox.get()) if discount_spinbox.get() else 0.0
            tax = float(tax_spinbox.get()) if tax_spinbox.get() else 0.0

            # Step 1: Base subtotal (before adjustments)
            base_subtotal = quantity * selling_price

            # Step 2: Apply discount
            discounted_price = base_subtotal - (base_subtotal * (discount / 100))

            # Step 3: Apply tax
            final_total = discounted_price + (discounted_price * (tax / 100))

            # Step 4: Update readonly subtotal entry
            subtotal_entry.configure(state='normal')  # Temporarily enable editing
            subtotal_entry.delete(0, END)
            subtotal_entry.insert(0, f"{final_total:.2f}")  # Store final subtotal
            subtotal_entry.configure(state='readonly')  # Set back to readonly

        except ValueError:
            pass  # Handles unexpected non-numeric input

    quantity_entry.bind("<KeyRelease>", calculate_final_subtotal)
    selling_price_entry.bind("<KeyRelease>", calculate_final_subtotal)
    discount_spinbox.bind("<KeyRelease>", calculate_final_subtotal)
    tax_spinbox.bind("<KeyRelease>", calculate_final_subtotal)


    def close_sales_frame(event=None):
        sales_frame.place_forget()
    window.bind("<Escape>", close_sales_frame)



    sales_treeview(treeview)