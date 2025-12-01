
from datetime import datetime
from tkinter import *
from reports import reports_form

from employees import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form
from employees import connect_database
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from sales import sales_form
import tkinter as tk
import os
from developer import developer_form



# UPDATING DASHBOARD DATA
def update_dashboard_counts():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return


    try:
        cursor.execute('USE inventory_management_system')

        cursor.execute('SELECT * FROM employee_data')
        emp_records = cursor.fetchall()
        total_emp_count_label.config(text=len(emp_records))

        cursor.execute('SELECT * FROM supplier_data')
        sup_records = cursor.fetchall()
        total_sup_count_label.config(text=len(sup_records))

        cursor.execute('SELECT * FROM category_data')
        cat_records = cursor.fetchall()
        total_cat_count_label.config(text=len(cat_records))

        cursor.execute('SELECT * FROM product_data')
        prod_records = cursor.fetchall()
        total_prod_count_label.config(text=len(prod_records))
    except Exception as e:
        print(f"Error updating dashboard: {e}")








# BUTTONS FEATURES AND HOVER ANIMATIONS STYLING CLASS
class HoverButton(Button):
    def __init__(self, master=None, **kw):
        self.default_bg = kw.get('bg', '#005f5f')
        self.hover_bg = kw.get('activebackground', '#007f7f')
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


# This will avoid Over Flapping of the form
current_frame = None

def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame = form_function(window)


def open_dashboard(login_root):
    global window
    global total_emp_count_label, total_sup_count_label, total_cat_count_label, total_prod_count_label, total_sales_count_label

    window = tk.Toplevel()
    window.geometry('1530x830')
    window.title("Dashboard")
    window.resizable(False, False)
    window.config(bg='white')


    def configure_styles():

        # Create style engine
        style = ttk.Style()

        # Global theme settings
        style.theme_use('clam')  # Best theme for customizability

        # ===== Button Styles =====
        style.configure(
            'TButton',
            font=('Winky Rough', 14, 'bold'),
            padding=8,
            relief='flat',
            background='#ACB1CA',
            foreground='black',
            borderwidth=0,
            focusthickness=0,
            focuscolor='none'
        )

        style.map(
            'TButton',
            background=[('active', '#4783C2'), ('pressed', '#2A5A8A')],
            foreground=[('active', 'white'), ('pressed', 'white')],
            relief=[('pressed', 'sunken'), ('!pressed', 'flat')]
        )

        # ===== Card Styles =====
        style.configure(
            'Card.TFrame',
            background='#193B52',
            borderwidth=2,
            relief='ridge',
            highlightthickness=2,
            highlightbackground='#00cccc'
        )

        style.map(
            'Card.TFrame',
            background=[('active', '#1E4D6B')],
            bordercolor=[('active', '#00cccc')]
        )

        style.configure(
            'Card.TLabel',
            background='#193B52',
            foreground='white',
            font=('Winky Rough', 16)
        )

        style.map(
            'Card.TLabel',
            background=[('active', '#1E4D6B')],
            foreground=[('active', 'white')]
        )

        # Special style for counter numbers
        style.configure(
            'Counter.TLabel',
            background='#193B52',
            foreground='#00cccc',
            font=('Winky Rough', 28, 'bold')
        )

        style.map(
            'Counter.TLabel',
            background=[('active', '#1E4D6B')]
        )

        # ===== Entry/Combobox Styles =====
        style.configure(
            'TEntry',
            fieldbackground='white',
            foreground='black',
            insertcolor='black',
            bordercolor='#005f5f',
            lightcolor='#00cccc',
            darkcolor='#005f5f'
        )

        style.map(
            'TEntry',
            bordercolor=[('focus', '#00cccc'), ('!focus', '#005f5f')],
            lightcolor=[('focus', '#00cccc')],
            darkcolor=[('focus', '#00cccc')]
        )

    # CALLING THE STYLE CONFIGURATION FOR APPLYTING STYLING.
    configure_styles()
    # Logout Function
    def logout():
        if messagebox.askyesno('Logout', 'Do you want to log out of the current session?'):
            window.destroy()  # THIS METHOD EXISTS THE CURRENT WINDOW AND REDIRECTS US THE PREVIOUS ONE.
            login_root.deiconify()

            # THE EXITING FUNCTION TO EXIT THE OVERALL SYSTEM
    def exit_window():
        if messagebox.askyesno('Exit', 'Do you really  want to exit the window?'):
            window.destroy()




    # Date and Time updater
    def update_datetime():
        now = datetime.now()
        current_datetime = f"\u00A9 Developed by: Amir Iqbal Khan\t\t Date: {now.strftime('%Y-%m-%d')}\t\t Time: {now.strftime('%I:%M:%S %p')}"
        subtitleLabel.config(text=current_datetime)
        window.after(1000, update_datetime)


    # Background Image
    bg_img = Image.open("images/backphoto.jpg")
    bg_img = bg_img.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = Label(window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

    # TITLE AND LOGO
    bg_image = PhotoImage(file='images/789.png')
    titleLabel = Label(window, image=bg_image, compound=LEFT, text="                     Inventory Management System",
                       font=('Winky Rough', 35, 'bold'), bg='#011A2D', fg='white', anchor='w', padx=40)
    titleLabel.image = bg_image
    titleLabel.place(x=0, y=0, relwidth=1)

    logoutButton = HoverButton(window,text="Logout",font=('Winky Rough', 14, 'bold'),bg='#011A2D',fg='white',
        activebackground='#193B52',activeforeground='white',relief=FLAT,bd=0,highlightthickness=2,highlightbackground='#004d4d',
        highlightcolor='#00cccc',cursor='hand2',command=logout)
    logoutButton.place(x=1420, y=20)

    # ABOUT DEVELOPER FRAME
    developer_button = HoverButton(window, text='About Developer', font=('Winky Rough', 10, 'bold'), bg='#5B4842',
                                fg='white', command=lambda : show_form(developer_form))
    developer_button.place(x=1390, y=130)






    subtitleLabel = Label(window, text="", font=('times new roman', 12), bg='#011A2D', fg='white')
    subtitleLabel.place(x=0, y=808, relwidth=1)
    update_datetime()

    # TOP MENU BARS
    top_frame = Frame(window)
    top_frame.place(x=0, y=73, width=1528, height=50)

    menuLabel = Label(top_frame, text="Menu", font=('Winky Rough', 20, 'bold'), bg="#ACB1CA", fg='black', height=2,
                      width=12)
    menuLabel.pack(side=LEFT)

    def add_menu_button(icon_file, text, command_func, width=190):
        icon = PhotoImage(file=icon_file)
        menu_button = HoverButton(top_frame, image=icon, compound=LEFT, text=text,
                          font=('Winky Rough', 20, 'bold'), height=67, width=width, anchor='w', padx=1,
                          bg='#ACB1CA', fg='black', activebackground='#4783C2', activeforeground='white',
                          relief=FLAT, bd=0, highlightthickness=2, highlightbackground='#004d4d',
                          highlightcolor='#00cccc', cursor='hand2', command=command_func)
        menu_button.image = icon
        menu_button.pack(side=LEFT)

    add_menu_button('images/employee24.png', " Employees", lambda: show_form(employee_form))
    add_menu_button('images/supplier24.png', " Suppliers", lambda: show_form(supplier_form))
    add_menu_button('images/category24.png', " Categories", lambda: show_form(category_form))
    add_menu_button('images/product24.png', " Products", lambda: show_form(product_form))
    add_menu_button('images/sales.png', " Sales", lambda: show_form(sales_form))
    add_menu_button('images/bag.png', " Reports", lambda:show_form(reports_form), width=180)
    add_menu_button('images/exit.png', " Exit", exit_window, width=180)



    # Dashboard Cards
    # CREATING A DICTIONARY TO STORE LABELS FOR EACY ACCESS
    dashboard_labels = {}
    def create_card(x, image_file, text, key=None):
        # Create the main frame
        frame = Frame(window, bg='#193B52', bd=2, relief=RIDGE, highlightbackground="#00cccc", highlightthickness=2)
        frame.place(x=x, y=620, width=250, height=120)

        # LOADING THE ICON LABEL
        icon = PhotoImage(file=image_file)
        icon_label = Label(frame, image=icon, bg='#193B52')
        icon_label.image = icon  # Keep a reference
        icon_label.place(x=20, y=30)

        # CREATING TEXT LABEL
        text_label = Label(frame, text=text, bg='#193B52', fg='white',
                           font=('Winky Rough', 16, 'bold'))
        text_label.place(x=80, y=20)

        # CREATING COUNT LABEL
        count_label = Label(frame, text="0", bg='#193B52', fg='#00cccc',
                            font=('Winky Rough', 25, 'bold'))
        count_label.place(x=80, y=50)

        # STORING REFERENCES IF KEY IS PROVIDED
        if key:
            dashboard_labels[key] = count_label

        # HOVER FUNCTIONS THAT UPDATE ALL CHILD WIDGETS
        def on_enter(e):
            frame.config(bg='#1E4D6B')
            # Update all child widgets' backgrounds
            for child in frame.winfo_children():
                if isinstance(child, Label):
                    child.config(bg='#1E4D6B')

        def on_leave(e):
            frame.config(bg='#193B52')
            # UPDATING ALL CHILD WIDGETS' BACKGROUNDS
            for child in frame.winfo_children():
                if isinstance(child, Label):
                    child.config(bg='#193B52')

        # BINDING ALL HOVER EFFECTS
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        # ALSO BINDING HOVER EVENTS TO ALL CHILD WIDGETS IN THE WINDOW OF DASHBOARD
        for child in frame.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

        if key:
            dashboard_labels[key] = count_label  # STORING REFERENCES TO THE LABELS
        return count_label

    total_emp_count_label = create_card(60, 'images/total_emp.png', "Total Employees")
    total_sup_count_label = create_card(345, 'images/supplier64.png', "Total Suppliers")
    total_cat_count_label = create_card(630, 'images/category64.png', "Total Categories")
    total_prod_count_label = create_card(915, 'images/total_prod.png', "Total Products")
    total_sales_count_label = create_card(1200, 'images/total_sales.png', 'Total Sales', key='sales')



    # UNUSED FUNCTION (WILL BE UPGRADED AFTER THE PRESENTATION)
    def get_sales_subtotal():
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_management_system')
            cursor.execute("SELECT COALESCE(SUM(sub_total), 0) FROM sales_data")  # Ensures result is never None
            subtotal = cursor.fetchone()[0]

        except Exception as e:
            print(f"DEBUG: Error fetching sales subtotal - {e}")
            subtotal = "Error"
        finally:
            cursor.close()
            connection.close()

        return subtotal

    def update_dashboard():
        """Update sales subtotal dynamically."""
        sales_total = get_sales_subtotal()
        if "sales" in dashboard_labels:
            dashboard_labels["sales"].config(text=str(sales_total))
            dashboard_labels["sales"].update()  # Force UI refresh
        window.after(500, update_dashboard)  # Update every 5 seconds
    update_dashboard()


    # ALL KEYBOARD SHORTCUTS REGARDING THE DASHBOARD WINDOW IS GETTING BIND USING BELOW FUNCTION (add_shortcuts).
    def add_shortcuts():
        window.bind("<Control-e>", lambda e: show_form(employee_form))
        window.bind("<Control-s>", lambda e: show_form(supplier_form))
        window.bind("<Control-c>", lambda e: show_form(category_form))
        window.bind("<Control-p>", lambda e: show_form(product_form))
        window.bind("<Control-l>", lambda e: show_form(sales_form))
        window.bind("<Control-r>", lambda e: show_form(reports_form))
        window.bind("<Alt-F4>", lambda e: exit_window())
        window.bind("<Escape>", lambda e: logout())

    add_shortcuts()


    window.after(1000, update_dashboard_counts)


