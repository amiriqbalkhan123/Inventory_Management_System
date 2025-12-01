from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import matplotlib.font_manager as fm


def supplier_report_window(reports):
    supplier_report_frame = Frame(reports, bg='#ACB1CA', width=1335, height=630)
    supplier_report_frame.place(x=170, y=50)


    # 🔤 Load custom font
    try:
        custom_font_path = "WinkyRough-VariableFont_wght.ttf"  # Ensure this file exists
        winky_font = fm.FontProperties(fname=custom_font_path)
    except Exception as e:
        print(f"Error loading custom font: {e}")
        return

    df = pd.DataFrame()
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amir@12345",
            database="inventory_management_system"
        )
        query = """
        SELECT name, COUNT(*) as total_invoices
        FROM supplier_data
        GROUP BY name
        """
        cursor = conn.cursor()
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=['name', 'total_invoices'])


    except Exception as e:
        print(f"Database connection or query failed: {e}")
        return

    finally:
        if conn:
            conn.close()

    if df.empty:
        print("No supplier data found.")
        return

    # Chart setup
    fig, ax = plt.subplots(figsize=(10, 5), dpi=100, facecolor='#ACB1CA')

    df = df.sort_values(by='total_invoices', ascending=True)
    bar_colors = [
        '#1c2463',  # Coral
        '#1728ad',  # Deep violet
        '#020729',  # Apple green
        '#022905',  # Soft pink
        '#102412',  # Lavender blue (matches well)
        '#241d09',  # Bright salmon
        '#2f0b4f',  # Rich blue
        '#460b7a',  # Warm yellow-orange
        '#0c3d21',  # Orchid purple
        '#0c5069'  # Mint teal
    ]
    colors = bar_colors[:len(df)]

    bars = ax.barh(df['name'], df['total_invoices'], color=colors)

    # Annotate bars with values (not bold)
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2,
                f'{int(width)}', va='center',
                fontsize=10, fontproperties=winky_font, fontweight='normal', color='black')

    # Set labels and styles
    title_obj = ax.set_title('Top Suppliers by Number of Invoices', pad=15, color='black')
    title_obj.set_fontproperties(winky_font)
    title_obj.set_fontsize(20)
    title_obj.set_fontweight('bold')

    ax.set_xlabel('Total Invoices', fontsize=12, color='black', fontproperties=winky_font)

    # Y-labels (supplier names)
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['name'], fontproperties=winky_font, fontsize=9, color='black')

    ax.set_facecolor('#ACB1CA')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(1.5)  # Bold left spine

    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(1.5)  # Bold bottom spine

    fig.patch.set_facecolor('#ACB1CA')
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=supplier_report_frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=50, y=20, width=1200, height=450)
