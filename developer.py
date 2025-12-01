from tkinter import *
from tkinter import ttk
from tkinter.ttk import Scrollbar


def developer_form(window):
    # MAIN FRAME CONFIGURATION
    developer_frame = Frame(window, bg='#ACB1CA', width=1530, height=685)
    developer_frame.place(x=0, y=123)

    # COLOR SCHEME
    SECTION_COLOR = '#193B52'
    BG_COLOR = '#ACB1CA'
    TEXT_COLOR = '#2c3e50'
    LIGHT_TEXT = '#7f8c8d'

    # FONT STYLE
    TITLE_FONT = ('Winky Rough', 16, 'bold')
    SECTION_FONT = ('Winky Rough', 18, 'bold')
    CONTENT_FONT = ('Winky Rough', 9, 'bold')
    BULLET_FONT = ('Winky Rough', 14, 'bold')
    SUB_BULLET_FONT = ('Winky Rough', 11, 'bold')

    # HEADER SECTION
    heading_label = Label(developer_frame,
                          text="Developer Profile",
                          font=TITLE_FONT,
                          bg='#193B52',
                          fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # CONTENT FRAME
    content_frame = Frame(developer_frame, bg=BG_COLOR)
    content_frame.place(x=0, y=40, relwidth=1, height=645)

    # LEFT COLUMN (MY SCROLLABLE CONTENT)
    left_canvas = Canvas(content_frame, bg=BG_COLOR, highlightthickness=0)
    left_canvas.place(x=60, y=0, width=1000, height=580)

    style = ttk.Style()
    style.theme_use("default")

    scrollbar = Scrollbar(content_frame, orient=VERTICAL, command=left_canvas.yview, style='Vertical.TScrollbar')
    scrollbar.place(x=1060, y=0, height=580)

    left_column = Frame(left_canvas, bg=BG_COLOR)
    left_canvas.create_window((0, 0), window=left_column, anchor='nw')

    def configure_scroll(event):
        left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        left_canvas.configure(yscrollcommand=scrollbar.set)

    left_column.bind("<Configure>", configure_scroll)

    # RIGHT COLUMN (FOR IMAGE)
    right_column = Frame(content_frame, bg=BG_COLOR)
    right_column.place(x=1100, y=0, width=380, height=600)

    # LOADING AND DISPLAYING IMAGES
    try:
        global developer_image
        developer_image = PhotoImage(file="images/fg.png")
        Label(right_column,
              image=developer_image,
              bg=BG_COLOR).pack(pady=50, padx=20)
    except:
        Label(right_column,
              text="Image not loaded",
              bg=BG_COLOR, fg='red').pack(pady=50)

    # SECTION FUNCTION CREATION
    def create_section(parent, title, items, is_bulleted=True):
        section_frame = Frame(parent, bg=BG_COLOR)
        section_frame.pack(fill=BOTH, pady=(8, 0))

        Label(section_frame,
              text=title,
              font=SECTION_FONT,
              bg=BG_COLOR,
              fg=SECTION_COLOR).pack(anchor='w')

        content_frame = Frame(section_frame, bg=BG_COLOR)
        content_frame.pack(fill=BOTH, padx=5, pady=2)

        for item in items:
            if is_bulleted:
                Label(content_frame,
                      text=f"• {item}",
                      font=BULLET_FONT,
                      bg=BG_COLOR,
                      fg=TEXT_COLOR,
                      anchor='w').pack(fill=BOTH, pady=0)
            else:
                Label(content_frame,
                      text=item,
                      font=CONTENT_FONT,
                      bg=BG_COLOR,
                      fg=TEXT_COLOR,
                      anchor='w').pack(fill=BOTH, pady=0)
        return section_frame

    # ADDING ALL THE SECTIONS HERE
    create_section(left_column, "PROFESSIONAL SUMMARY", [
        "Senior Backend Developer at JACK Organization - Kabul, Afghanistan",
        "Junior Data Analyst (delivered 17 end-to-end data-analysis projects)"
    ])

    create_section(left_column, "WORK EXPERIENCE", [
        "Senior Backend Developer, JACK Organization, Kabul, Afghanistan",
        "Network Engineer, multiple national & international enterprises",
        "IT Assistant, Corvit Institution, Lahore, Pakistan",
        "IT Marketing Lead, PNY Institute, Lahore, Pakistan"
    ])

    create_section(left_column, "CERTIFICATIONS", [
        "Cisco CCIE #310**",
        "CCNA 200-301",
        "CCNP Enterprise (ENCORE)",
        "CompTIA S+, N+, A+",
        "Microsoft Certified Solutions Associate",
        "Microsoft Certified Solutions Expert"
        "Microsoft Azure Fundamentals (AZ-900)",
        "CEHv11",
        "Linux Certified"
    ])


    # PROJECT HIGHLIGHTS
    projects_frame = create_section(left_column, "PROJECT HIGHLIGHTS", [], False)

    project_categories = [
        ("Network & Infrastructure",
         "Designed & delivered 350+ network-infrastructure implementations (routing, switching, security)"),
        ("Desktop Applications (Python/Tkinter)",
         "Delivered 89+ custom Desktop - Applications for Inventories, Money Exchanging Offices, Grocery Stores, \n"
         "Industrial Corporations, and factories"),
        ("Database & SQL",
         "Built 37+ SQL-based modules: complex queries, stored procedures, reporting dashboards")
    ]

    for category, details in project_categories:
        Label(projects_frame,
              text=f"• {category}",
              font=BULLET_FONT,
              bg=BG_COLOR,
              fg=SECTION_COLOR,
              anchor='w').pack(fill=BOTH, pady=1)

        Label(projects_frame,
              text=f"  {details}",
              font=SUB_BULLET_FONT,
              bg=BG_COLOR,
              fg=TEXT_COLOR,
              anchor='w').pack(fill=BOTH, padx=10, pady=0)
    # DATA ANALYSIS PROJECTS IN COMPACT FORMAT
    Label(projects_frame,
          text="• Data Analysis (17 Projects):",
          font=BULLET_FONT,
          bg=BG_COLOR,
          fg=SECTION_COLOR,
          anchor='w').pack(fill=BOTH, pady=1)

    analysis_projects = [
        "China's CO production, IMDB trends, Boeing analysis",
        "India's population, UAE automotive, Tesla stocks"
    ]

    for proj in analysis_projects:
        Label(projects_frame,
              text=f"  - {proj}",
              font=SUB_BULLET_FONT,
              bg=BG_COLOR,
              fg=TEXT_COLOR,
              anchor='w').pack(fill=BOTH, padx=10, pady=0)

    # OTHER SECTIONS
    create_section(left_column, "PROFESSIONAL MEMBERSHIPS", [
        "Corvit Event Organizers, Lahore - PAK (Member)",
        "IT Standards & Telecommunication Agency, Islamabad - PAK (Member)",
        "Kardan University Success Center, Kabul - AFG (Member)"
    ])

    education_frame = create_section(left_column, "EDUCATION", [], False)
    Label(education_frame,
          text="• B.Sc. Ongoing (3rd Semester), Kardan University",
          font=BULLET_FONT,
          bg=BG_COLOR,
          fg=TEXT_COLOR,
          anchor='w').pack(fill=BOTH, pady=1)

    Label(education_frame,
          text="  - 4.00 GPA; 149/150 in most recent MT exams",
          font=SUB_BULLET_FONT,
          bg=BG_COLOR,
          fg=TEXT_COLOR,
          anchor='w').pack(fill=BOTH, padx=10, pady=0)

    # CLOSING BUTTON
    close_btn = Button(developer_frame,
                       text="Close",
                       font=('Arial', 10),
                       bg='#193B52',
                       fg='white',
                       activebackground='#2C5E7A',
                       command=developer_frame.destroy)
    close_btn.place(x=1400, y=640, width=80, height=30)