import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def animate_number(label, new_value, duration=3000, steps=60):
    try:
        current = int(label.cget('text'))
    except ValueError:
        current = 0

    delta = new_value - current
    interval = max(duration // steps, 1)
    step = delta / steps
    counter = 0

    def update():
        nonlocal current, counter
        counter += 1
        current += step
        label.config(text=str(round(current)))
        if counter < steps:
            label.after(interval, update)
        else:
            label.config(text=str(new_value))

    update()

def animate_currency(label, new_value, duration=3000, steps=60):
    try:
        current = float(label.cget('text'))
    except ValueError:
        current = 0.0

    delta = new_value - current
    interval = max(duration // steps, 1)
    step = delta / steps
    counter = 0

    def update():
        nonlocal current, counter
        counter += 1
        current += step
        label.config(text=f"{current:.2f}")
        if counter < steps:
            label.after(interval, update)
        else:
            label.config(text=f"{new_value:.2f}")

    update()

def flash_color(label, is_positive):
    original = label.cget("fg")
    highlight = "white" if is_positive else "white"
    label.config(fg=highlight)
    label.after(500, lambda: label.config(fg=original))











# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Amir@12345",
    database="inventory_management_system"
)
cursor = conn.cursor()


# Fetch top-selling product data
def fetch_sales_data():
    cursor.execute("""
        SELECT product_name, SUM(quantity) AS total_sold
        FROM sales_data
        GROUP BY product_name
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    return pd.DataFrame(cursor.fetchall(), columns=["Product", "Quantity Sold"])


# Fetch stock data for 15 active products
def fetch_stock_data():
    cursor.execute("""
        SELECT name, quantity
        FROM product_data
        WHERE status = 'Active'
        ORDER BY quantity DESC
        LIMIT 15
    """)
    return pd.DataFrame(cursor.fetchall(), columns=["Product", "Quantity"])


# Global dataframes
df_sales = fetch_sales_data()
df_stock = fetch_stock_data()


# Plot top 5 selling products
def plot_top_five_products(canvas, fig, ax):
    ax.clear()
    ax.bar(range(len(df_sales["Product"])), df_sales["Quantity Sold"], color="#1F2041")
    ax.set_title("Top 5 Selling Products", fontsize=14, color="black")
    ax.set_xlabel("Products", fontsize=10, color="black")
    ax.set_ylabel("Quantity Sold", fontsize=10, color="black", labelpad=15)
    ax.set_xticks(range(len(df_sales["Product"])))
    ax.set_xticklabels(df_sales["Product"], rotation=60, ha='right')
    ax.set_facecolor("#ACB1CA")
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(1.5)  # Bold left spine

    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(1.5)  # Bold bottom spine
    ax.tick_params(axis='x', colors="black", labelsize=9)
    ax.tick_params(axis='y', colors="black", labelsize=9)

    fig.subplots_adjust(left=0.18, right=0.97, top=0.88, bottom=0.4)
    canvas.draw()


# Plot stock availability chart
def plot_stock_availability(canvas, fig, ax):
    ax.clear()
    ax.bar(range(len(df_stock["Product"])), df_stock["Quantity"], color="#3E92CC")
    ax.set_title("Stock Availability (Top 15 Active Products)", fontsize=12, color="black")
    ax.set_xlabel("Products", fontsize=10, color="black", labelpad=50)
    ax.xaxis.set_label_coords(0.5, -0.6)
    ax.set_ylabel("Quantity in Stock", fontsize=10, color="black", labelpad=15)
    ax.set_xticks(range(len(df_stock["Product"])))
    ax.set_xticklabels(df_stock["Product"], rotation=60, ha='right')
    ax.set_facecolor("#ACB1CA")
    ax.spines["bottom"].set_color("black")
    ax.spines["left"].set_color("black")
    ax.tick_params(axis='x', colors="black", labelsize=9)
    ax.tick_params(axis='y', colors="black", labelsize=9)

    fig.subplots_adjust(left=0.18, right=0.97, top=0.88, bottom=0.4)
    canvas.draw()


# Update both charts live
def update_charts(canvas1, fig1, ax1, canvas2, fig2, ax2):
    global df_sales, df_stock
    df_sales = fetch_sales_data()
    df_stock = fetch_stock_data()

    plot_top_five_products(canvas1, fig1, ax1)
    plot_stock_availability(canvas2, fig2, ax2)

    # Call again after 1 second
    canvas1.get_tk_widget().after(1000, lambda: update_charts(canvas1, fig1, ax1, canvas2, fig2, ax2))


# GUI layout
def sales_report_window(reports):
    def pulse_border(widget, colors=['#1589F0', '#0E6BA8'], interval=600, index=0):
        widget.config(highlightbackground=colors[index], highlightthickness=2)
        next_index = (index + 1) % len(colors)
        widget.after(interval, pulse_border, widget, colors, interval, next_index)

    def add_hover_effects(frame, label_widgets, side_bar=None):
        def on_enter(e):
            frame.config(bg='#1589F0')
            for lbl in label_widgets:
                lbl.config(bg='#1589F0')
            if side_bar:
                side_bar.config(bg='#063970')

        def on_leave(e):
            frame.config(bg='#0E6BA8')
            for lbl in label_widgets:
                lbl.config(bg='#0E6BA8')
            if side_bar:
                side_bar.config(bg='#001C55')

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        for lbl in label_widgets:
            lbl.bind("<Enter>", on_enter)
            lbl.bind("<Leave>", on_leave)
        if side_bar:
            side_bar.bind("<Enter>", on_enter)
            side_bar.bind("<Leave>", on_leave)

    def update_units_sold_label():
        try:
            cursor.execute("SELECT SUM(CAST(quantity AS UNSIGNED)) FROM sales_data")
            result = cursor.fetchone()
            total = result[0] if result[0] is not None else 0
            animate_number(units_sold_count_label, total)
            flash_color(units_sold_count_label, total >= 0)
        except Exception as e:
            print("Error updating units sold label:", e)

    def update_customers_count_label():
        try:
            cursor.execute("SELECT COUNT(*) FROM customer_data")
            result = cursor.fetchone()
            total = result[0] if result[0] is not None else 0
            animate_number(customers_count_label, total)
            flash_color(customers_count_label, total >= 0)
        except Exception as e:
            print("Error updating customers count label:", e)

    def update_products_available_label():
        try:
            cursor.execute("SELECT COUNT(*) FROM product_data WHERE status = 'Active'")
            result = cursor.fetchone()
            count = result[0] if result else 0
            animate_number(products_available_count_label, count)
            flash_color(products_available_count_label, count >= 0)
        except Exception as e:
            print("Error updating available products:", e)

    def update_sales_amount_label():
        try:
            cursor.execute("SELECT SUM(CAST(sub_total AS DECIMAL(10, 2))) FROM sales_data")
            result = cursor.fetchone()
            amount = float(result[0]) if result[0] else 0.0
            animate_currency(sales_amount_count_label, amount)
            flash_color(sales_amount_count_label, amount >= 0)
        except Exception as e:
            print("Error updating sales amount:", e)

    def update_profit_loss_label():
        try:
            cursor.execute("""
                SELECT SUM(
                    (CAST(selling_price AS DECIMAL(10,2)) - CAST(purchase_price AS DECIMAL(10,2)))
                    * CAST(quantity AS DECIMAL(10,2))
                )
                FROM sales_data
            """)
            result = cursor.fetchone()
            profit = float(result[0]) if result[0] else 0.0
            animate_currency(profit_loss_count_label, profit)
            flash_color(profit_loss_count_label, profit >= 0)
        except Exception as e:
            print("Error updating profit/loss:", e)

    def update_stock_amount_label():
        try:
            cursor.execute("""
                SELECT SUM(discounted_price * quantity)
                FROM product_data
                WHERE status = 'Active' AND quantity > 0
            """)
            result = cursor.fetchone()
            stock = float(result[0]) if result[0] else 0.0
            animate_currency(stock_amount_count_label, stock)
            flash_color(stock_amount_count_label, stock >= 0)
        except Exception as e:
            print("Error updating stock amount:", e)

    def update_purchase_amount_label():
        try:
            cursor.execute("SELECT SUM(discounted_price * quantity) FROM product_data")
            result = cursor.fetchone()
            purchase = float(result[0]) if result[0] else 0.0
            animate_currency(purchase_amount_count_label, purchase)
            flash_color(purchase_amount_count_label, purchase >= 0)
        except Exception as e:
            print("Error updating purchase amount:", e)

    sales_report_frame = tk.Frame(reports, bg='#ACB1CA', width=1300, height=625)
    sales_report_frame.place(x=200, y=55)

    # Info frames
    units_sold_frame = tk.Frame(sales_report_frame, bg='#0E6BA8', width=150, height=70)
    units_sold_frame.place(x=30, y=15)

    units_sold_frame_mini = tk.Frame(units_sold_frame, bg='#001C55', width=22, height=70)
    units_sold_frame_mini.place(x=0, y=0)

    units_sold_label = tk.Label(units_sold_frame, bg='#0E6BA8', fg='white',text='📦 Units Sold', font=('Winky Rough', 12, 'bold'))
    units_sold_label.place(x=35, y=3)

    units_sold_count_label = tk.Label(units_sold_frame, bg='#0E6BA8', fg='white', text='0', font=('Winky Rough', 12, 'bold'))
    units_sold_count_label.place(x=55, y=30)
    update_units_sold_label() # Calling the total number of products sold through the function update_units_sold_label
    add_hover_effects(units_sold_frame, [units_sold_label, units_sold_count_label], units_sold_frame_mini)
    pulse_border(units_sold_frame)



    total_customers_frame = tk.Frame(sales_report_frame, bg='#0E6BA8', width=150, height=70)
    total_customers_frame.place(x=250, y=15)

    total_customers_frame_mini = tk.Frame(total_customers_frame, bg='#001C55', width=22, height=70)
    total_customers_frame_mini.place(x=0, y=0)

    customers_label = tk.Label(total_customers_frame, bg='#0E6BA8', fg='white', text='Customers',
                                font=('Winky Rough', 12, 'bold'))
    customers_label.place(x=40, y=3)

    customers_count_label = tk.Label(total_customers_frame, bg='#0E6BA8', fg='white', text='0',
                                      font=('Winky Rough', 12, 'bold'))
    customers_count_label.place(x=70, y=30)
    update_customers_count_label()
    add_hover_effects(total_customers_frame, [customers_label, customers_count_label], total_customers_frame_mini)
    pulse_border(total_customers_frame)


    products_available_frame = tk.Frame(sales_report_frame, bg='#0E6BA8', width=150, height=70)
    products_available_frame.place(x=470, y=15)

    products_available_frame_mini = tk.Frame(products_available_frame, bg='#001C55', width=22, height=70)
    products_available_frame_mini.place(x=0, y=0)

    products_available_label = tk.Label(products_available_frame, bg='#0E6BA8', fg='white', text='Available Products',
                                font=('Winky Rough', 10, 'bold'))
    products_available_label.place(x=26, y=3)

    products_available_count_label = tk.Label(products_available_frame, bg='#0E6BA8', fg='white', text='0',
                                      font=('Winky Rough', 12, 'bold'))
    products_available_count_label.place(x=70, y=30)
    update_products_available_label()
    add_hover_effects(products_available_frame, [products_available_label, products_available_count_label],
                      products_available_frame_mini)
    pulse_border(products_available_frame)

    purchase_amount_frame = tk.Frame(sales_report_frame, bg='#0E6BA8', width=150, height=70)
    purchase_amount_frame.place(x=690, y=15)

    purchase_amount_frame_mini = tk.Frame(purchase_amount_frame, bg='#001C55', width=22, height=70)
    purchase_amount_frame_mini.place(x=0, y=0)

    purchase_amount_label = tk.Label(purchase_amount_frame, bg='#0E6BA8', fg='white', text='Purchase Amt',
                                font=('Winky Rough', 12, 'bold'))
    purchase_amount_label.place(x=28, y=3)

    purchase_amount_count_label = tk.Label(purchase_amount_frame, bg='#0E6BA8', fg='white', text='0',
                                      font=('Winky Rough', 12, 'bold'))
    purchase_amount_count_label.place(x=28, y=30)
    update_purchase_amount_label()
    add_hover_effects(purchase_amount_frame, [purchase_amount_label, purchase_amount_count_label],
                      purchase_amount_frame_mini)

    pulse_border(purchase_amount_frame)

    sales_amount_frame = tk.Frame(sales_report_frame, bg='#0E6BA8', width=150, height=70)
    sales_amount_frame.place(x=910, y=15)

    sales_amount_frame_mini = tk.Frame(sales_amount_frame, bg='#001C55', width=22, height=70)
    sales_amount_frame_mini.place(x=0, y=0)

    sales_amount_label= tk.Label(sales_amount_frame, bg='#0E6BA8', fg='white', text='Sales Amt',
                                font=('Winky Rough', 12, 'bold'))
    sales_amount_label.place(x=28, y=3)

    sales_amount_count_label = tk.Label(sales_amount_frame, bg='#0E6BA8', fg='white', text='0',
                                           font=('Winky Rough', 12, 'bold'))
    sales_amount_count_label.place(x=28, y=30)
    update_sales_amount_label()
    add_hover_effects(sales_amount_frame, [sales_amount_label, sales_amount_count_label], sales_amount_frame_mini)
    pulse_border(sales_amount_frame)


    profit_loss_frame = tk.Frame(sales_report_frame, bg='#0E6BA8', width=150, height=70)
    profit_loss_frame.place(x=1130, y=15)

    profit_loss_frame_mini = tk.Frame(profit_loss_frame, bg='#001C55', width=22, height=70)
    profit_loss_frame_mini.place(x=0, y=0)

    profit_loss_label = tk.Label(profit_loss_frame, bg='#0E6BA8', fg='white', text='Profit/Loss',
                                font=('Winky Rough', 12, 'bold'))
    profit_loss_label.place(x=28, y=3)

    profit_loss_count_label = tk.Label(profit_loss_frame, bg='#0E6BA8', fg='white', text='0',
                                           font=('Winky Rough', 12, 'bold'))
    profit_loss_count_label.place(x=28, y=30)
    update_profit_loss_label()
    add_hover_effects(profit_loss_frame, [profit_loss_label, profit_loss_count_label], profit_loss_frame_mini)
    pulse_border(profit_loss_frame)

    stock_amount_frame = tk.Frame(sales_report_frame, bg='#0E6BA8', width=150, height=70)
    stock_amount_frame.place(x=1130, y=130)

    stock_amount_frame_mini = tk.Frame(stock_amount_frame, bg='#001C55', width=22, height=70)
    stock_amount_frame_mini.place(x=0, y=0)

    stock_amount_label = tk.Label(stock_amount_frame, bg='#0E6BA8', fg='white', text='Stock Amt',
                                font=('Winky Rough', 12, 'bold'))
    stock_amount_label.place(x=28, y=3)

    stock_amount_count_label = tk.Label(stock_amount_frame, bg='#0E6BA8', fg='white', text='0',
                                       font=('Winky Rough', 12, 'bold'))
    stock_amount_count_label.place(x=28, y=30)
    update_stock_amount_label()
    add_hover_effects(stock_amount_frame, [stock_amount_label, stock_amount_count_label], stock_amount_frame_mini)

    pulse_border(stock_amount_frame)


    # First chart: Top 5 Sales
    fig1, ax1 = plt.subplots(figsize=(6.5, 4), facecolor='#ACB1CA')
    canvas1 = FigureCanvasTkAgg(fig1, sales_report_frame)
    canvas1_widget = canvas1.get_tk_widget()
    canvas1_widget.place(x=40, y=130, width=500, height=300)

    # Second chart: Stock Availability
    fig2, ax2 = plt.subplots(figsize=(6.5, 4), facecolor='#ACB1CA')
    canvas2 = FigureCanvasTkAgg(fig2, sales_report_frame)
    canvas2_widget = canvas2.get_tk_widget()
    canvas2_widget.place(x=580, y=130, width=500, height=300)

    # Start live chart updates
    update_charts(canvas1, fig1, ax1, canvas2, fig2, ax2)

    def auto_update_all_metrics():
        update_units_sold_label()
        update_customers_count_label()
        update_products_available_label()
        update_purchase_amount_label()  # ✅ New
        update_sales_amount_label()
        update_profit_loss_label()
        update_stock_amount_label()
        sales_report_frame.after(1000, auto_update_all_metrics)

    auto_update_all_metrics()


    return sales_report_frame
