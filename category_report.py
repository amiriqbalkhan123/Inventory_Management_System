from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta




class HoverButton(Button):
    def __init__(self, master=None, **kw):
        self.default_bg = kw.get('bg', '#011A2D')  # BACKGROUND COLOR OF THE HOVER BUTTON WHICH IS LATER APPLIED ON THE BUTTONS.
        self.hover_bg = kw.get('activebackground', '#145470')
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







def category_report_window(reports):
    category_report_frame = Frame(reports, bg='#ACB1CA', width=1300, height=650)
    category_report_frame.place(x=200, y=50)

    # DATABASE CONNECTION (UNUSED, FOR UPGRADING PURPOSE WRITTEN TO THIS SCRIPT).
    def connect_db():
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amir@12345",
                database="inventory_management_system"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            return None

    # A FRAME FOR CHARTS WITH SCROLLBAR
    chart_container = Frame(category_report_frame, bg='#ACB1CA')
    chart_container.place(x=20, y=20, width=1260, height=320)

    # CANVAS, AND SCROLLBAR IN THIS SECTION
    chart_canvas = Canvas(chart_container, bg='#ACB1CA', highlightthickness=0)
    chart_scrollbar = ttk.Scrollbar(chart_container, orient="horizontal", command=chart_canvas.xview)
    chart_scrollable_frame = Frame(chart_canvas, bg='#ACB1CA')

    chart_scrollable_frame.bind(
        "<Configure>",
        lambda e: chart_canvas.configure(scrollregion=chart_canvas.bbox("all"))
    )

    chart_canvas.create_window((0, 0), window=chart_scrollable_frame, anchor="nw")
    chart_canvas.configure(xscrollcommand=chart_scrollbar.set)

    chart_canvas.pack(side="top", fill="both", expand=True,pady=(0, 15))
    chart_scrollbar.pack(side="bottom", fill="x", pady=(18,2))

    # FRAME FOR TABLES AND LISTS
    data_frame = Frame(category_report_frame, bg='#ACB1CA')
    data_frame.place(x=20, y=342, width=1260, height=288)

    # NOTEBOOK FOR MULTIPLE TABS
    notebook = ttk.Notebook(data_frame)
    notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use('default')
    # COMPLETE NOTEBOOK STYLE FIX
    style.configure("TNotebook",
                    background='#ACB1CA',  # THE COLOR OF THE AREA BEHIND THE TABS
                    borderwidth=0,
                    tabmargins=[0, 0, 0, 0])

    style.configure("TNotebook.Tab",
                    background='#011A2D',  # UNSELECTED TAB COLOR
                    foreground='white',
                    font=("Winky Rough", 12, "bold"),
                    padding=[15, 5],  # HORIZONTAL, VERTICAL PADDING
                    borderwidth=0,
                    focuscolor='#ACB1CA')

    style.map("TNotebook.Tab",
              background=[("selected", '#193B52')],  # THIS IS THE TAB COLOR
              foreground=[("selected", "white")],
              relief=[("selected", "flat")])
    notebook.config(style="TNotebook")
    notebook.pack(fill=BOTH, expand=True, padx=0, pady=0)
    # Create tabs
    tab1 = Frame(notebook, bg='#ACB1CA')
    tab2 = Frame(notebook, bg='#ACB1CA')
    tab3 = Frame(notebook, bg='#ACB1CA')

    notebook.add(tab1, text="Performance Metrics")
    notebook.add(tab2, text="Low Stock & No Products")
    notebook.add(tab3, text="Low Sales Categories")

    # FETCHING THE DATA FROM THE DATABASE THROUGH THE BELOW FUNCTION WHICH CONNECTS TO THE DATABASE.
    def fetch_data():
        conn = connect_db()
        if not conn:
            return None, None, None, None, None

        cursor = conn.cursor(dictionary=True)
        data = {
            'products_per_category': [],
            'stock_value': [],
            'units_sold': [],
            'revenue': [],
            'no_products': [],
            'no_recent_sales': [],
            'low_stock': []
        }

        try:
            # 1. NUMBER OF PRODUCTS PER CATEGORY
            cursor.execute("""
                SELECT c.name AS category, COUNT(p.id) AS product_count
                FROM category_data c
                LEFT JOIN product_data p ON c.name = p.category
                GROUP BY c.name
                ORDER BY product_count DESC
            """)
            data['products_per_category'] = cursor.fetchall()

            # 2. TOTAL STOCK VALUE PER CATEGORY
            cursor.execute("""
                SELECT c.name AS category, 
                       COALESCE(SUM(p.price * p.quantity), 0) AS total_value
                FROM category_data c
                LEFT JOIN product_data p ON c.name = p.category
                GROUP BY c.name
                ORDER BY total_value DESC
            """)
            data['stock_value'] = cursor.fetchall()

            # 3. TOTAL UNITS SOLD PER CATEGORY
            cursor.execute("""
                SELECT category, SUM(CAST(quantity AS UNSIGNED)) AS total_sold
                FROM sales_data
                GROUP BY category
                ORDER BY total_sold DESC
            """)
            data['units_sold'] = cursor.fetchall()

            # 4. TOTAL REVENUE PER CATEGORY
            cursor.execute("""
                SELECT category, SUM(CAST(sub_total AS DECIMAL(10,2))) AS total_revenue
                FROM sales_data
                GROUP BY category
                ORDER BY total_revenue DESC
            """)
            data['revenue'] = cursor.fetchall()

            # 5. BEST PERFORMING CATEGORY
            best_category = data['revenue'][0] if data['revenue'] else None

            # 6. CATEGORIES WITH NO PRODUCTS
            cursor.execute("""
                SELECT c.name AS category
                FROM category_data c
                LEFT JOIN product_data p ON c.name = p.category
                WHERE p.id IS NULL
            """)
            data['no_products'] = cursor.fetchall()

            # 7. CATEGORIES WITH NO RECENT SALES - USING sales_id as proxy for time
            try:
                # GETTING THE MOST RECENT sales_id as proxy for time
                cursor.execute("SELECT MAX(sales_id) AS max_id FROM sales_data")
                max_id = cursor.fetchone()['max_id']
                recent_threshold = max_id - 100 if max_id else 0

                cursor.execute("""
                    SELECT c.name AS category
                    FROM category_data c
                    WHERE c.name NOT IN (
                        SELECT DISTINCT category 
                        FROM sales_data 
                        WHERE sales_id >= %s
                    )
                """, (recent_threshold,))
                data['no_recent_sales'] = cursor.fetchall()
            except:
                data['no_recent_sales'] = []

            # 8. CATEGORIES WITH LOW STOCK (QUANTITY < 10)
            cursor.execute("""
                SELECT DISTINCT p.category
                FROM product_data p
                WHERE p.quantity < 10
            """)
            data['low_stock'] = cursor.fetchall()

            return data, best_category, data['no_products'], data['no_recent_sales'], data['low_stock']

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")
            return None, None, None, None, None
        finally:
            cursor.close()
            conn.close()

    # IN THIS SECTION, I WILL CREATE CHARTS

    def create_charts():
        data, best_category, no_products, no_recent_sales, low_stock = fetch_data()

        # CLEARING THE PREVIOUS CHARTS
        for widget in chart_scrollable_frame.winfo_children():
            widget.destroy()

        if not data:
            Label(chart_scrollable_frame, text="Error loading data", fg="white", bg="#2c3e50").pack()
            return

        # CREATING A WIDER FIGURE WITH MORE SPACE BETWEEN THE 4 CHARTS (ALL)
        fig = Figure(figsize=(24, 2.8), dpi=100, facecolor='#ACB1CA')

        # INCREASING THE SPACE BETWEEN THE CHARTS INSIDE CATEGORY REPORTS
        fig.subplots_adjust(wspace=1.4, left=0.10, right=0.95)

        # CHART 1: NUMBER OF PRODUCTS PER CATEGORY
        ax1 = fig.add_subplot(141)  # 1 row, 4 columns, 1st chart
        categories = [item['category'] for item in data['products_per_category']]
        counts = [item['product_count'] for item in data['products_per_category']]

        # HORIZONTAL BAR CHART
        bars = ax1.barh(categories, counts, color='#3498db', height=0.6)
        ax1.set_title('Products per Category', color='black', fontsize=12)


        ax1.tick_params(axis='y', colors='black', labelsize=8)
        ax1.tick_params(axis='x', colors='black', labelsize=8)
        ax1.set_facecolor('#ACB1CA')


        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.spines['left'].set_color('black')
        ax1.spines['bottom'].set_color('black')

        # ADDING VALUE LABELS
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax1.text(count + 0.2, bar.get_y() + bar.get_height() / 2,
                     str(count), color='black', va='center', fontsize=8)

        # CHART 2: TOTAL STOCK VALUE PER CATEGORY SECTION
        ax2 = fig.add_subplot(142)  # 1 row, 4 columns, 2nd chart
        categories = [item['category'] for item in data['stock_value']]
        values = [float(item['total_value']) for item in data['stock_value']]

        bars = ax2.barh(categories, values, color='#2ecc71', height=0.6)
        ax2.set_title('Stock Value per Category', color='black', fontsize=12)
        ax2.tick_params(axis='y', colors='black', labelsize=8)
        ax2.tick_params(axis='x', colors='black', labelsize=8)
        ax2.set_facecolor('#ACB1CA')

        ax2.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax2.spines['left'].set_color('black')
        ax2.spines['bottom'].set_color('black')


        # ADDING VALUE LABELS HERE IN THIS SECTION
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax2.text(value + 5, bar.get_y() + bar.get_height() / 2,
                     f'AFN{value:,.0f}', color='black', va='center', fontsize=8)

        # CHART 3: TOTAL UNITS SOLD PER CATEGORY SECTION
        ax3 = fig.add_subplot(143)  # 1 row, 4 columns, 3rd chart
        categories = [item['category'] for item in data['units_sold']]
        sold = [item['total_sold'] for item in data['units_sold']]

        bars = ax3.barh(categories, sold, color='#e74c3c', height=0.6)
        ax3.set_title('Units Sold per Category', color='black', fontsize=12)
        ax3.tick_params(axis='y', colors='black', labelsize=8)
        ax3.tick_params(axis='x', colors='black', labelsize=8)
        ax3.set_facecolor('#ACB1CA')

        ax3.spines['right'].set_visible(False)
        ax3.spines['top'].set_visible(False)
        ax3.spines['left'].set_color('black')
        ax3.spines['bottom'].set_color('black')


        # ADDING VALUE LABELS HERE
        for i, (bar, count) in enumerate(zip(bars, sold)):
            ax3.text(count + 2, bar.get_y() + bar.get_height() / 2,
                     f'{count:,}', color='black', va='center', fontsize=8)

        # CHART 4: TOTAL REVENUE PER CATEGORY
        ax4 = fig.add_subplot(144)  # 1 row, 4 columns, 4th chart
        categories = [item['category'] for item in data['revenue']]
        revenue = [float(item['total_revenue']) for item in data['revenue']]

        bars = ax4.barh(categories, revenue, color='#f39c12', height=0.6)
        ax4.set_title('Revenue per Category', color='black', fontsize=12)
        ax4.tick_params(axis='y', colors='black', labelsize=8)
        ax4.tick_params(axis='x', colors='black', labelsize=8)
        ax4.set_facecolor('#ACB1CA')

        ax4.spines['right'].set_visible(False)
        ax4.spines['top'].set_visible(False)
        ax4.spines['left'].set_color('black')
        ax4.spines['bottom'].set_color('black')


        # ADDING VALUE LABELS HERE
        for i, (bar, value) in enumerate(zip(bars, revenue)):
            ax4.text(value + 5, bar.get_y() + bar.get_height() / 2,
                     f'AFN{value:,.0f}', color='black', va='center', fontsize=8)

        # EMBEDING THE CHART IN TKINTER USING CANVAS
        canvas = FigureCanvasTkAgg(fig, master=chart_scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # CLEARING PREVIOUS DATA
        for widget in tab1.winfo_children():
            widget.destroy()
        for widget in tab2.winfo_children():
            widget.destroy()
        for widget in tab3.winfo_children():
            widget.destroy()

        # TAB 1: PERFORMANCE METRICS SECTION
        metrics_frame = Frame(tab1, bg='#ACB1CA')
        metrics_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # BEST PERFORMING CATEGORY SECTION
        best_frame = Frame(metrics_frame, bg='#ACB1CA', bd=1, relief=SOLID)
        best_frame.pack(fill=X, pady=5)
        Label(best_frame, text="BEST PERFORMING CATEGORY",
              font=("Winky Rough", 15, "bold"), bg="#ACB1CA", fg="black").pack(pady=(5, 0))

        if best_category:
            best_text = f"{best_category['category']} - AFN {best_category['total_revenue']:,.2f} revenue"
            Label(best_frame, text=best_text, font=("Winky Rough", 13),
                  bg="#ACB1CA", fg="black").pack(pady=(0, 5))
        else:
            Label(best_frame, text="No sales data available", font=("Winky Rough", 13),
                  bg="#ACB1CA", fg="black").pack(pady=(0, 5))

        # TREEVIEW FOR PERFORMANCE METRICS
        tree_frame = Frame(metrics_frame, bg='#ACB1CA')
        tree_frame.pack(fill=BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("Category", "Products", "Stock Value", "Units Sold", "Revenue"),
                            show="headings", height=8)

        # STYLING OF THE TREEVIEW
        style = ttk.Style()
        style.theme_use('default')  # THIS THEME SUPPORT TREEVIEW HEADING CUSTOMIZATION
        style.configure("Treeview", background="#ACB1CA", fieldbackground="#ACB1CA",
                        foreground="black", font=("Winky Rough", 9))
        style.configure("Treeview.Heading", background="#ACB1CA", foreground="black",
                        font=("Winky Rough", 11, "bold"))
        style.map("Treeview",
                  background=[('selected', 'white')],
                  foreground=[('selected', 'black')])

        # Define columns
        tree.heading("Category", text="CATEGORY")
        tree.heading("Products", text="PRODUCTS")
        tree.heading("Stock Value", text="STOCK VALUE (AFN)")
        tree.heading("Units Sold", text="UNITS SOLD")
        tree.heading("Revenue", text="REVENUE (AFN)")

        tree.column("Category", width=150, anchor=W)
        tree.column("Products", width=80, anchor=CENTER)
        tree.column("Stock Value", width=120, anchor=E)
        tree.column("Units Sold", width=100, anchor=E)
        tree.column("Revenue", width=120, anchor=E)



        # SCROLLBAR
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree.pack(fill=BOTH, expand=True)

        # ADDING DATA TO THE TREEVIEW
        for cat in data['products_per_category']:
            category = cat['category']
            products = cat['product_count']

            # FIND MATCHING STOCK VALUE
            stock_val = next((item for item in data['stock_value']
                              if item['category'] == category), {'total_value': 0})

            # FINDING MATCHING UNITS SOLD
            units_sold = next((item for item in data['units_sold']
                               if item['category'] == category), {'total_sold': 0})

            # FINDING MATCHING REVENUE
            revenue = next((item for item in data['revenue']
                            if item['category'] == category), {'total_revenue': 0})

            tree.insert("", "end", values=(
                category,
                products,
                f"{float(stock_val['total_value']):,.2f}",
                f"{units_sold['total_sold']:,}",
                f"{float(revenue['total_revenue']):,.2f}"
            ))

        # Tab 2: LOW STOCK AND NO PRODUCTS
        low_stock_frame = Frame(tab2, bg='#ACB1CA')
        low_stock_frame.pack(fill=BOTH, expand=True, padx=10, pady=2)

        # LOW STOCK CATEGORIES
        Label(low_stock_frame, text="CATEGORIES WITH LOW STOCK (ALERTS)",
              font=("Winky Rough", 10, "bold"), bg="#ACB1CA", fg="black").pack(anchor=W, pady=(5, 0))

        low_listbox = Listbox(low_stock_frame, bg="#ACB1CA", fg="black",
                              font=("Winky Rough", 10), height=4, relief=SOLID, selectbackground='white', selectforeground='black')
        low_listbox.pack(fill=X, pady=(0, 10))

        if low_stock:
            for item in low_stock:
                low_listbox.insert(END, f" • {item['category']}")
        else:
            low_listbox.insert(END, " • No categories with low stock")

        # CATEGORIES WITH NO PRODUCTS
        Label(low_stock_frame, text="CATEGORIES WITH NO PRODUCTS",
              font=("Winky Rough", 10, "bold"), bg="#ACB1CA", fg="black").pack(anchor=W, pady=(0, 0))

        no_products_listbox = Listbox(low_stock_frame, bg="#ACB1CA", fg="black",
                                      font=("Winky Rough", 10), height=7, relief=SOLID, selectbackground='white', selectforeground='black')
        no_products_listbox.pack(fill=X, pady=(0, 1))

        if no_products:
            for item in no_products:
                no_products_listbox.insert(END, f" • {item['category']}")
        else:
            no_products_listbox.insert(END, " • All categories have products assigned")

        # Tab 3: LOW SALES CATEGORIES
        low_sales_frame = Frame(tab3, bg='#ACB1CA')
        low_sales_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # CATEGORIES WITH NO RECENT SALES
        Label(low_sales_frame, text="CATEGORIES WITH NO RECENT SALES",
              font=("Winky Rough", 10, "bold"), bg="#ACB1CA", fg="black").pack(anchor=W, pady=(5, 0))

        no_sales_listbox = Listbox(low_sales_frame, bg="#ACB1CA", fg="black",
                                   font=("Winky Rough", 10), height=8, relief=SOLID, selectbackground='white', selectforeground='black')
        no_sales_listbox.pack(fill=BOTH, pady=(0, 10))

        if no_recent_sales:
            for item in no_recent_sales:
                no_sales_listbox.insert(END, f" • {item['category']}")
        else:
            no_sales_listbox.insert(END, " • All categories have recent sales")

    # A REFRESH BUTTON TO REFRESH THE DATA OF THE CATEGORY REPORTS
    refresh_btn = HoverButton(category_report_frame, text="Refresh Data", command=create_charts,
                         bg="#193B52", fg="white", font=("Winky Rough", 12, "bold"),
                         relief=FLAT, padx=0, height=1)
    refresh_btn.place(x=1200, y=10)

    # INITIAL DATA LOADING
    create_charts()


# BELOW IS USED FOR TESTING PURPOSES (DOESN'T LAST AFTER THE PRESENTATION).
if __name__ == "__main__":
    root = Tk()
    root.geometry("1500x700")
    root.title("Category Reports")
    category_report_window(root)
    root.mainloop()