import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Frame, Button
from fpdf import FPDF
import mysql.connector
from sales_report import sales_report_window
from suppliers_report import supplier_report_window
from category_report import category_report_window
from inventory_report import inventory_report_window
from employee_report import employee_report_window

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Amir@12345",
        database="inventory_management_system"
    )

# Fetch Sale Data
def fetch_sale_data(sale_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT sales_id, product_name, price_per_unit, selling_price
        FROM sales_data
        WHERE sales_id = %s
    """
    cursor.execute(query, (sale_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Download PDF Function
def download_pdf(data, sale_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Sales Report for Sale ID: {sale_id}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_fill_color(200, 220, 255)
    pdf.cell(40, 10, "Sale ID", 1, 0, 'C', 1)
    pdf.cell(80, 10, "Product Name", 1, 0, 'C', 1)
    pdf.cell(35, 10, "Actual Price", 1, 0, 'C', 1)
    pdf.cell(35, 10, "Discounted Price", 1, 1, 'C', 1)

    for row in data:
        pdf.cell(40, 10, str(row[0]), 1)
        pdf.cell(80, 10, row[1], 1)
        pdf.cell(35, 10, str(row[2]), 1)
        pdf.cell(35, 10, str(row[3]), 1)
        pdf.ln()

    filename = f"Sales_Report_{sale_id}.pdf"
    pdf.output(filename)
    messagebox.showinfo("PDF Downloaded", f"PDF saved as {filename}")

# Hover Button Class
class HoverButton(Button):
    def __init__(self, master, **kw):
        super().__init__(master=master, **kw)
        self.default_bg = self['background']
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = '#145470'

    def on_leave(self, e):
        self['background'] = self.default_bg

# Info Popup
def show_info_popup(anchor_widget):
    for widget in anchor_widget.master.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "InfoPopup":
            widget.destroy()

    popup = tk.Toplevel(anchor_widget)
    popup.title("InfoPopup")
    popup.overrideredirect(True)
    popup.attributes('-topmost', True)

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
        justify='left',
        bg="white",
        bd=1,
        relief="solid",
        padx=10,
        pady=10
    )
    info_label.pack()

# Reports Form
def reports_form(window):

    def generate_sales_pdf():
        from fpdf import FPDF
        from tkinter import filedialog

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # GETTING SALES SUMMARY DATA
            cursor.execute("""
                SELECT 
                    category,
                    COUNT(*) AS total_sales,
                    SUM(quantity) AS total_units,
                    SUM(sub_total) AS total_revenue
                FROM sales_data
                GROUP BY category
                ORDER BY total_revenue DESC
            """)
            sales_data = cursor.fetchall()

            # GETTING TOP PRODUCTS
            cursor.execute("""
                SELECT product_name, SUM(quantity) AS total_sold
                FROM sales_data
                GROUP BY product_name
                ORDER BY total_sold DESC
                LIMIT 10
            """)
            top_products = cursor.fetchall()

            # CREATING PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Sales Report Summary", 0, 1, 'C')
            pdf.ln(10)

            # SALES BY MONTH TABLE
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Monthly Sales Summary", 0, 1)
            pdf.set_font("Arial", size=10)

            # HEADER OF THE TABLE
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(40, 10, "Month", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Total Sales", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Units Sold", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Revenue (AFN)", 1, 1, 'C', 1)

            # TABLE DATA
            pdf.set_fill_color(255, 255, 255)
            for row in sales_data:
                pdf.cell(40, 10, str(row[0]), 1)
                pdf.cell(40, 10, str(row[1]), 1)
                pdf.cell(40, 10, str(row[2]), 1)
                pdf.cell(40, 10, f"{float(row[3]):,.2f}", 1)
                pdf.ln()

            # TOP PRODUCTS SECTION
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Top Selling Products", 0, 1)
            pdf.set_font("Arial", size=10)

            # TOP PRODUCTS TABLE
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(100, 10, "Product Name", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Units Sold", 1, 1, 'C', 1)

            pdf.set_fill_color(255, 255, 255)
            for product in top_products:
                pdf.cell(100, 10, product[0], 1)
                pdf.cell(40, 10, str(product[1]), 1)
                pdf.ln()

            # ASKING FOR DOWNLOADING DIRECTORY IN THE PC
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save As: "
            )

            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("Success", f"Sales Report Saved Successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
        finally:
            if conn:
                conn.close()

    def generate_suppliers_pdf():
        from fpdf import FPDF
        from tkinter import filedialog

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # GETTING SUPPLIER DATA
            cursor.execute("""
                SELECT 
                    invoice,
                    name, 
                    contact, 
                    description
                FROM supplier_data
                ORDER BY name
            """)
            suppliers = cursor.fetchall()

            # CREATING PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Suppliers Report", 0, 1, 'C')
            pdf.ln(10)

            # SUPPLIER TABLE
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Supplier Information", 0, 1)
            pdf.set_font("Arial", size=10)

            # HEADER OF THE TABLE
            # UPDATING THE TABLE HEADER
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(30, 10, "Invoice #", 1, 0, 'C', 1)
            pdf.cell(60, 10, "Supplier Name", 1, 0, 'C', 1)
            pdf.cell(50, 10, "Contact", 1, 0, 'C', 1)
            pdf.cell(50, 10, "Description", 1, 1, 'C', 1)

            # UPDATING THE TABLE DATA ROWS
            pdf.set_fill_color(255, 255, 255)
            for supplier in suppliers:
                pdf.cell(30, 10, str(supplier[0]), 1)  # INVOICE
                pdf.cell(60, 10, supplier[1], 1)  # NAME
                pdf.cell(50, 10, supplier[2], 1)  # CONTACT
                pdf.cell(50, 10, supplier[3], 1)  # DESCRIPTION
                pdf.ln()

            # ASKING FOR DOWNLOADING DIRECTORY IN THE PC
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Suppliers Report As"
            )

            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("Success", f"Suppliers Report Saved Successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
        finally:
            if conn:
                conn.close()

    def generate_categories_pdf():
        from fpdf import FPDF
        from tkinter import filedialog

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            # Get category data
            cursor.execute("""
                SELECT 
                    c.name AS category,
                    COUNT(p.id) AS product_count,
                    SUM(p.price * p.quantity) AS stock_value,
                    (SELECT SUM(quantity) FROM sales_data WHERE category = c.name) AS units_sold,
                    (SELECT SUM(sub_total) FROM sales_data WHERE category = c.name) AS revenue
                FROM category_data c
                LEFT JOIN product_data p ON c.name = p.category
                GROUP BY c.name
                ORDER BY revenue DESC
            """)
            categories = cursor.fetchall()

            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Categories Report", 0, 1, 'C')
            pdf.ln(10)

            # Category table
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Category Performance", 0, 1)
            pdf.set_font("Arial", size=10)

            # Table header
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(50, 10, "Category", 1, 0, 'C', 1)
            pdf.cell(30, 10, "Products", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Stock Value (AFN)", 1, 0, 'C', 1)
            pdf.cell(30, 10, "Units Sold", 1, 0, 'C', 1)
            pdf.cell(40, 10, "Revenue (AFN)", 1, 1, 'C', 1)

            # Table data
            pdf.set_fill_color(255, 255, 255)
            for cat in categories:
                pdf.cell(50, 10, cat['category'], 1)
                pdf.cell(30, 10, str(cat['product_count']), 1)
                pdf.cell(40, 10, f"{float(cat['stock_value'] or 0):,.2f}", 1)
                pdf.cell(30, 10, str(cat['units_sold'] or 0), 1)
                pdf.cell(40, 10, f"{float(cat['revenue'] or 0):,.2f}", 1)
                pdf.ln()

            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Categories Report As"
            )

            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("Success", f"Categories Report Saved Successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
        finally:
            if conn:
                conn.close()

    global back_image, information_image

    reports_frame = Frame(window, width=1530, height=685, bg='#ACB1CA')
    reports_frame.place(x=0, y=123)

    heading_label = Label(reports_frame, text="All Reports Here", font=('Winky Rough', 16, 'bold'), bg='#193B52', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='images/back.png')
    back_button = Button(reports_frame, image=back_image, bd=0, cursor='hand2', command=lambda: reports_frame.place_forget(), bg='#ACB1CA', activebackground='#ACB1CA')
    back_button.place(x=10, y=37)

    information_image = PhotoImage(file='images/information.png')
    information_button = Button(reports_frame, image=information_image, bd=0, cursor='hand2', command=lambda: show_info_popup(information_button), bg='#193B52', activebackground='#193B52')
    information_button.image = information_image
    information_button.place(x=10, y=8)

    left_menu_frame = Frame(reports_frame, bg='#ACB1CA', width=180, height=600, relief='ridge')
    left_menu_frame.place(x=0, y=82)

    button_frame = Frame(left_menu_frame, bg='#ACB1CA')
    button_frame.grid(padx=10, pady=20)


    blocked_frame = Frame(reports_frame, bg='#ACB1CA', width=1100, height=385)
    blocked_frame.place(x=260, y=115)

    blocked_label = Label(blocked_frame, text='Access Denied ! This Section of the IMS will \n be designed Based on Organization Specific Inventory Details \n Thanks, \n\n Developer', bg='#ACB1CA', fg='#0a1a73', font=('Winky Rough', 30, 'bold'))
    blocked_label.place(x=30, y=30)


    button_font = ('Winky Rough', 12, 'bold')
    button_bg = '#193B52'
    button_fg = 'white'
    button_width = 18
    button_height = 1
    pady_value = 8




    HoverButton(button_frame, text='Sales Reports', font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, command=lambda: sales_report_window(reports_frame)).grid(row=0, column=0, pady=pady_value)
    HoverButton(button_frame, text='Supplier Reports', font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, command=lambda: supplier_report_window(reports_frame)).grid(row=1, column=0, pady=pady_value)
    HoverButton(button_frame, text='Category Reports', font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, command=lambda: category_report_window(reports_frame)).grid(row=2, column=0, pady=pady_value)
    HoverButton(button_frame, text='Save Sales PDF', font=button_font, bg=button_bg, fg=button_fg,
                width=button_width, height=button_height, command=generate_sales_pdf).grid(row=3, column=0,
                                                                                           pady=pady_value)
    HoverButton(button_frame, text='Save Suppliers PDF', font=button_font, bg=button_bg, fg=button_fg,
                width=button_width, height=button_height, command=generate_suppliers_pdf).grid(row=4, column=0,
                                                                                               pady=pady_value)
    HoverButton(button_frame, text='Save Categories PDF', font=button_font, bg=button_bg, fg=button_fg,
                width=button_width, height=button_height, command=generate_categories_pdf).grid(row=5, column=0,
                                                                                                pady=pady_value)




    def close_reports_frame(event=None):
        reports_frame.place_forget()

    window.bind("<Escape>", close_reports_frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reports Window")
    root.geometry("1350x700")
    reports_form(root)
    root.mainloop()
