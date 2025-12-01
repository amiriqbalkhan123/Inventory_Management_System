# This page is for the category page inside the Category Button
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from PIL import ImageTk

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
    # AUTO - CLOSING THE POPUP AFTER 5 SECONDS (5000 MS)
    popup.after(2000, popup.destroy)





def select_data(id_entry, category_name_entry, description_text, treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected!')
        return

    content = treeview.item(index)
    actual_content = content['values']

    if not actual_content:
        messagebox.showerror('Error', 'No data available in the selected row!')
        return

    # CLEARING EXISTING FIELD VALUES (ENTRIES)
    id_entry.delete(0, END)
    category_name_entry.delete(0, END)
    description_text.delete(1.0, END)

    # INSERTING SELECTED ROW VALUES INTO FIELDS (ENTRIES)
    id_entry.insert(0, actual_content[0])
    category_name_entry.insert(0, actual_content[1])
    description_text.insert(1.0, actual_content[2])





def delete_category(treeview):
    from dashboard import update_dashboard_counts
    # prior to deletion we will ensure that the user has selected a row or not
    index = treeview.selection() #checking the index of the treeview, if there is no index, means that the user doesn't selected any row.
    content=treeview.item(index)
    row=content['values']
    id=row[0]
    if not index:
        messagebox.showerror('Error', 'No Row is Selected!')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('DELETE FROM category_data WHERE id=%s', (id,))
        connection.commit() # this will commit the changes
        update_dashboard_counts()
        treeview_data(treeview) # this will display the updated data in the treeview
        messagebox.showinfo('Info', 'Record has been Successfully Deleted!')
    except Exception as e:
        messagebox.showerror('Error', f'Due to {e}')
    finally:
        cursor.close()
        connection.close()


def clear(id_entry, category_name_entry, description_text):
    id_entry.delete(0, END)
    category_name_entry.delete(0, END)
    description_text.delete(1.0, END)









def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_management_system')
        cursor.execute('SELECT * FROM category_data')
        records = cursor.fetchall()
        treeview.delete(* treeview.get_children()) # this will delete the old data inside the treeview
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e: # this will handle any exceptions inside the code
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()











def add_category(id, name, description, treeview):
    from dashboard import update_dashboard_counts
    if id == '' or name == '' or description == '':
        messagebox.showerror('Error', 'All Fields are Required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_management_system')
            cursor.execute('CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, name VARCHAR(30), description TEXT)')

            # To check if the ID Already Exists or Not

            cursor.execute('SELECT * FROM category_data WHERE id=%s',(id,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'ID Already Exists!')
                return
            cursor.execute('INSERT INTO category_data VALUES(%s,%s,%s)',(id,name,description))
            connection.commit()
            update_dashboard_counts()
            messagebox.showinfo('Info', 'Data has been Successfully Inserted')
            treeview_data(treeview)
        except Exception as e:  # this will handle any exceptions inside the code
            messagebox.showerror('Error', f'Error due to {e}')

        finally:
            cursor.close()
            connection.close()





















def category_form(window):
    global back_image, logo, logo_image
    category_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    category_frame.place(x=0, y=123)

    heading_label = Label(category_frame, text="Manage Category Details", font=('Winky Rough', 16, 'bold'), bg='#193B52', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='images/back.png')
    back_button = Button(category_frame, image=back_image, bd=0, cursor='hand2', command=lambda: category_frame.place_forget(), bg='#ACB1CA', activebackground='#ACB1CA')
    back_button.place(x=10, y=37)

    """logo = PhotoImage(file='back_cat.jpg')
    label = Label(category_frame,image=logo, bg='white')
    label.place(x=30, y=100)"""

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(category_frame, image=information_image, bd=0, cursor='hand2',
                                command=lambda: show_info_popup(information_button), bg='#193B52', activebackground='#193B52')
    information_button.image = information_image  # prevent garbage collection
    information_button.place(x=10, y=8)  # or .grid(...) as per your layout

    details_frame = Frame(category_frame, bg='#ACB1CA', relief=SUNKEN, bd=2, height=200, width=180)
    details_frame.place(x=80, y=100)

    """logo_image = PhotoImage(file='cat555.png')
    logo_label = Label(category_frame, image=logo_image, bg='#ACB1CA')
    logo_label.place(x=900, y=80)"""

    title_label = Label(details_frame, text='Categories', font=('Winky Rough', 22, 'bold'), bg='#193B52', fg='white')
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky='ew')

    id_label = Label(details_frame, text="ID", font=('Winky Rough', 14, 'bold'), bg='#ACB1CA', fg='black')
    id_label.grid(row=1, column=0, padx=20, sticky='w')
    id_entry = Entry(details_frame, font=('Winky Rough', 14, 'bold'), bg='white')
    id_entry.grid(row=1, column=1)

    category_name_label = Label(details_frame, text='Category Name', font=('Winky Rough', 14, 'bold'),bg='#ACB1CA')
    category_name_label.grid(row=2, column=0, padx=20, sticky='w')
    category_name_entry = Entry(details_frame, font=('Winky Rough', 14, 'bold'),bg='white')
    category_name_entry.grid(row=2, column=1, pady=20)

    description_label = Label(details_frame, text='Description', font=('Winky Rough', 14, 'bold'), bg='#ACB1CA')
    description_label.grid(row=3, column=0, padx=20, sticky='nw')
    description_text = Text(details_frame, width=25, height=6, bd=2, bg='white')
    description_text.grid(row=3, column=1)

    button_frame = Frame(category_frame, bg='#ACB1CA')
    button_frame.place(x=80, y=400)

    add_button = HoverButton(button_frame, text='Add', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2', fg='white',bg='#193B52',command=lambda: add_category(id_entry.get(), category_name_entry.get(),
                                                     description_text.get("1.0", "end-1c"), treeview))
    add_button.grid(row=0, column=0, padx=20)

    def on_ctrl_a(event):
        add_button.invoke()
        return "break"
    window.bind('<Control-a>', on_ctrl_a)


    delete_button = HoverButton(button_frame, text='Delete', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2',
                           fg='white', bg='#193B52', command=lambda: delete_category(treeview))
    delete_button.grid(row=0, column=1, padx=20)
    def on_ctrl_d(event):
        delete_button.invoke()
        return "break"

    window.bind('<Control-d>', on_ctrl_d)

    clear_button = HoverButton(button_frame, text='Clear', font=('Winky Rough', 14, 'bold'), width=8, cursor='hand2',
                           fg='white', bg='#193B52', command=lambda:clear(id_entry, category_name_entry, description_text))
    clear_button.grid(row=0, column=2, padx=20)
    def on_ctrl_c(event):
        clear_button.invoke()
        return "break"

    window.bind('<Control-c>', on_ctrl_c)

    treeview_frame = Frame(category_frame)
    treeview_frame.place(x=600, y=100, height=400, width=800)
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview.Heading", background="#ACB1CA", foreground="black", font=("Winky Rough", 12, "bold"))

    vertical_scrollbar = ttk.Scrollbar(treeview_frame, orient=VERTICAL)
    horizontal_scrollbar = ttk.Scrollbar(treeview_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(treeview_frame, columns=('id', 'name', 'description'), show='headings', yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    # PACKING THE SCROLL BARS
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)

    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('name', text='Category Name')
    treeview.heading('description', text='Description')

    treeview.column('id', width=120)
    treeview.column('name', width=150)
    treeview.column('description', width=250)
    treeview_data(treeview)

    treeview.bind(
        '<ButtonRelease-1>',
        lambda event: select_data(id_entry, category_name_entry, description_text, treeview)
    )

    def close_category_frame(event=None):
        category_frame.place_forget()
    window.bind("<Escape>", close_category_frame)

    return category_frame