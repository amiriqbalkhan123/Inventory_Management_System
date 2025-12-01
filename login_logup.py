import mysql.connector
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import dashboard
import re
import hashlib
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_ADDRESS = "amiriqbalk2022@gmail.com"
EMAIL_PASSWORD = "tjwj qjjj ovrr klky"


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x700')
        self.root.title('Login / Logup to Inventory Management System')
        self.root.config(bg='#290025')

        self.icon = tk.PhotoImage(file="images/AIK.png")
        self.root.iconphoto(False, self.icon)

        self.logo = tk.PhotoImage(file="images/789.png")

        title_frame = tk.Frame(self.root, bg='#011638', width=1200, height=80)
        title_frame.place(x=0, y=0, relwidth=1)

        title_label = tk.Label(title_frame, text='Log In / Log Up to I M S', font=('Winky Rough', 30, 'bold'),
                               bg="#011638", fg='white')
        title_label.place(x=0, y=10, relwidth=1)

        self.logo_label = tk.Label(title_label, image=self.logo, bg='#011638')
        self.logo_label.place(x=20, y=1)

        self.bg_image = Image.open("images/loginback.png")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        new_height = int(screen_height * 0.9)
        self.bg_image = self.bg_image.resize((screen_width, new_height), Image.Resampling.LANCZOS)
        self.back_g = ImageTk.PhotoImage(self.bg_image)

        self.background_label = tk.Label(self.root, image=self.back_g)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()

        content_frame = tk.Frame(self.root, bg='#1F2041', width=400, height=400)
        content_frame.place(x=405, y=220)

        content_frame_title = tk.Label(content_frame, text='Enter Credentials to Login',
                                       font=('Winky Rough', 18, 'bold'), bg='#19647E', fg='white')
        content_frame_title.place(x=0, y=0, relwidth=1)

        username_label = tk.Label(content_frame, bg='#1F2041', text='Username :',
                                  font=('Winky Rough', 16, 'bold'), fg='white')
        username_label.place(x=30, y=70)
        self.username_entry = tk.Entry(content_frame, bg='white', fg='black',
                                       font=('Winky Rough', 16, 'bold'), width=16)
        self.username_entry.place(x=150, y=70)

        password_label = tk.Label(content_frame, bg='#1F2041', text='Password :',
                                  font=('Winky Rough', 16, 'bold'), fg='white')
        password_label.place(x=30, y=160)
        self.password_entry = tk.Entry(content_frame, bg='white', fg='black',
                                       font=('Winky Rough', 16, 'bold'), width=16, show='*')
        self.password_entry.place(x=150, y=160)

        login_button = tk.Button(content_frame, text='Login', width=12, height=1,
                                 font=('Winky Rough', 16, 'bold'), bg="#1F2041", fg="white",
                                 activebackground="#81ABBC", activeforeground="black", bd=3,
                                 relief="raised", cursor="hand2", command=self.validate_login)
        login_button.place(x=150, y=220)

        signup_label = tk.Label(content_frame, text="Don't have an account?", fg="white", cursor="hand2",
                                font=('Winky Rough', 10), bg='#1F2041')
        signup_label.place(x=155, y=280)
        signup_label.bind("<Button-1>", lambda e: self.on_signup_click())

        reset_label = tk.Label(content_frame, text="Reset Password?", fg="white", cursor="hand2",
                               font=('Winky Rough', 10), bg='#1F2041')
        reset_label.place(x=170, y=310)
        reset_label.bind("<Button-1>",
                         lambda e: self.on_reset_password_click())

        # BINDING ALL KEYS TOGETHER HERE IN THIS SECTION
        self.root.bind('<Return>', self.handle_enter_key)

        def on_enter_login(event):
            login_button.config(bg="#81ABBC", fg="black")

        def on_leave_login(event):
            login_button.config(bg="#1F2041", fg="white")

        login_button.bind("<Enter>", on_enter_login)
        login_button.bind("<Leave>", on_leave_login)

    def on_reset_password_click(self):
        reset_window = tk.Toplevel(self.root)
        reset_window.title("Reset Password")
        reset_window.geometry("400x300")
        reset_window.config(bg='#44839F')
        reset_window.grab_set()

        tk.Label(reset_window, text="Enter your registered email:",
                 font=('Winky Rough', 14), bg='#44839F', fg='white').pack(pady=10)
        email_entry = tk.Entry(reset_window, font=('Winky Rough', 14), width=30)
        email_entry.pack(pady=5)

        def send_reset_otp(to_email):
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to_email
            msg['Subject'] = 'IMS Password Reset OTP'
            body = f'Your OTP for password reset is: {otp}'
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                server.quit()
                return otp
            except Exception as e:
                messagebox.showerror("Email Error", f"Failed to send OTP:\n{str(e)}", parent=reset_window)
                return None

        def open_otp_verification():
            email = email_entry.get()
            if not email:
                messagebox.showerror("Input Error", "Please enter your email.", parent=reset_window)
                return

            connection = self.connect_database()
            if not connection:
                return

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM registration_credentials WHERE email=%s", (email,))
            user = cursor.fetchone()
            connection.close()

            if not user:
                messagebox.showerror("Not Found", "This email is not registered.", parent=reset_window)
                return

            otp = send_reset_otp(email)
            if not otp:
                return

            otp_window = tk.Toplevel(reset_window)
            otp_window.title("Verify OTP & Reset")
            otp_window.geometry("400x300")
            otp_window.config(bg='#1F2041')
            otp_window.grab_set()

            tk.Label(otp_window, text="Enter OTP sent to your email:", font=('Winky Rough', 12),
                     bg='#1F2041', fg='white').pack(pady=10)
            otp_entry = tk.Entry(otp_window, font=('Winky Rough', 14), width=20)
            otp_entry.pack(pady=5)

            tk.Label(otp_window, text="New Password:", font=('Winky Rough', 12),
                     bg='#1F2041', fg='white').pack(pady=5)
            new_password_entry = tk.Entry(otp_window, font=('Winky Rough', 14), width=20, show='*')
            new_password_entry.pack(pady=5)

            tk.Label(otp_window, text="Confirm Password:", font=('Winky Rough', 12),
                     bg='#1F2041', fg='white').pack(pady=5)
            confirm_password_entry = tk.Entry(otp_window, font=('Winky Rough', 14), width=20, show='*')
            confirm_password_entry.pack(pady=5)

            def update_password():
                entered_otp = otp_entry.get()
                new_password = new_password_entry.get()
                confirm_password = confirm_password_entry.get()

                if entered_otp != otp:
                    messagebox.showerror("Invalid OTP", "OTP does not match!", parent=otp_window)
                    return

                if new_password != confirm_password:
                    messagebox.showerror("Mismatch", "Passwords do not match.", parent=otp_window)
                    return

                if len(new_password) < 8:
                    messagebox.showerror("Weak Password", "Password must be at least 8 characters.", parent=otp_window)
                    return

                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

                try:
                    connection = self.connect_database()
                    if not connection:
                        return
                    cursor = connection.cursor()
                    cursor.execute("UPDATE registration_credentials SET password=%s WHERE email=%s",
                                   (hashed_password, email))
                    connection.commit()
                    connection.close()

                    messagebox.showinfo("Success", "Password updated successfully!", parent=otp_window)
                    otp_window.destroy()
                    reset_window.destroy()

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}", parent=otp_window)

            tk.Button(otp_window, text="Submit", font=('Winky Rough', 12),
                      bg="white", fg="black", command=update_password).pack(pady=15)

        tk.Button(reset_window, text="Send OTP", font=('Winky Rough', 14),
                  bg="white", fg="black", command=open_otp_verification).pack(pady=20)

    def handle_enter_key(self, event):
        self.validate_login()

    def connect_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amir@12345",
                database="inventory_management_system"
            )
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Failed", f"Error: {err}")
            return None

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        connection = self.connect_database()
        if not connection:
            return

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM registration_credentials WHERE username=%s AND password=%s",
                       (username, hashed_password))
        result = cursor.fetchone()
        connection.close()

        if result:
            messagebox.showinfo("Login Success", "Welcome to the Dashboard!")
            self.root.withdraw()
            try:
                import dashboard
                dashboard.open_dashboard(self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Dashboard failed: {e}")

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def on_signup_click(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Create Account")
        signup_window.geometry("500x400")
        signup_window.config(bg='#1F2041')
        signup_window.grab_set()

        title_label = tk.Label(signup_window, text="Create Your Account",
                               font=('Winky Rough', 20, 'bold'), bg='#1F2041', fg='white')
        title_label.pack(pady=20)

        email_label = tk.Label(signup_window, text="Email :", font=('Winky Rough', 16, 'bold'), bg='#1F2041',
                               fg='white')
        email_label.pack()
        email_entry = tk.Entry(signup_window, font=('Winky Rough', 14), width=30)
        email_entry.pack(pady=5)

        username_label = tk.Label(signup_window, text="Username :", font=('Winky Rough', 16, 'bold'), bg='#1F2041',
                                  fg='white')
        username_label.pack()
        username_entry = tk.Entry(signup_window, font=('Winky Rough', 14), width=30)
        username_entry.pack(pady=5)

        password_label = tk.Label(signup_window, text="Password :", font=('Winky Rough', 16, 'bold'), bg='#1F2041',
                                  fg='white')
        password_label.pack()
        password_entry = tk.Entry(signup_window, font=('Winky Rough', 14), width=30, show='*')
        password_entry.pack(pady=5)

        def send_otp(to_email):
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to_email
            msg['Subject'] = 'Your OTP for IMS Registration'

            body = f'Your 6-digit OTP is: {otp}\n\nPlease enter this in the registration window to continue.'
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                server.quit()
                return otp
            except Exception as e:
                messagebox.showerror("Email Error", f"Failed to send OTP:\n{str(e)}", parent=signup_window)
                return None

        def verify_and_register(email, username, password, user_otp, real_otp):
            if user_otp != real_otp:
                messagebox.showerror("OTP Failed", "Incorrect OTP entered.", parent=signup_window)
                return

            try:
                connection = self.connect_database()
                if not connection:
                    return
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM registration_credentials WHERE email=%s OR username=%s",
                               (email, username))
                if cursor.fetchone():
                    messagebox.showerror("Duplicate", "Username or Email already exists.", parent=signup_window)
                    return

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                cursor.execute("INSERT INTO registration_credentials (email, username, password) VALUES (%s, %s, %s)",
                               (email, username, hashed_password))
                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Account created successfully!", parent=signup_window)
                signup_window.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}", parent=signup_window)

        def register_user():
            email = email_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not email or not username or not password:
                messagebox.showwarning("Input Error", "All fields are required!", parent=signup_window)
                return

            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                messagebox.showerror("Invalid Email", "Please enter a valid email address.", parent=signup_window)
                return

            if not is_strong_password(password):
                messagebox.showerror("Weak Password",
                                     "Password must be at least 8 characters and include uppercase, lowercase, number, and special character.",
                                     parent=signup_window)
                return

            otp = send_otp(email)
            if not otp:
                return

            # OTP INPUT DIALOG
            otp_popup = tk.Toplevel(signup_window)
            otp_popup.title("Email Verification")
            otp_popup.geometry("300x150")
            otp_popup.config(bg='#19647E')
            otp_popup.grab_set()

            tk.Label(otp_popup, text="Enter OTP sent to email:",
                     font=('Winky Rough', 12), bg='#19647E', fg='white').pack(pady=10)
            otp_entry = tk.Entry(otp_popup, font=('Winky Rough', 14), width=15)
            otp_entry.pack(pady=5)

            def confirm_otp():
                user_otp = otp_entry.get()
                verify_and_register(email, username, password, user_otp, otp)
                otp_popup.destroy()

            tk.Button(otp_popup, text="Verify", font=('Winky Rough', 12),
                      bg="white", fg="black", command=confirm_otp).pack(pady=10)

        register_button = tk.Button(signup_window, text="Register", font=('Winky Rough', 16, 'bold')
                                              , bg = "#1F2041", fg = "white",
                                                activebackground = "#81ABBC", activeforeground = "black",
                                    width=12, height=1, bd=3, relief="raised", cursor="hand2", command=register_user)
        register_button.pack(pady=20)

        def is_strong_password(pwd):
            return (
                    len(pwd) >= 8 and
                    any(c.islower() for c in pwd) and
                    any(c.isupper() for c in pwd) and
                    any(c.isdigit() for c in pwd) and
                    any(c in "!@#$%^&*()-_=+[{]}|;:',<.>/?`~" for c in pwd)
            )

        def register_user():
            email = email_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not email or not username or not password:
                messagebox.showwarning("Input Error", "All fields are required!", parent=signup_window)
                return

            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                messagebox.showerror("Invalid Email", "Please enter a valid email address.", parent=signup_window)
                return

            if not is_strong_password(password):
                messagebox.showerror("Weak Password",
                                     "Password must be at least 8 characters and include uppercase, lowercase, number, and special character.",
                                     parent=signup_window)
                return

            try:
                connection = self.connect_database()
                if not connection:
                    return
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM registration_credentials WHERE email=%s OR username=%s",
                               (email, username))
                if cursor.fetchone():
                    messagebox.showerror("Duplicate", "Username or Email already exists.", parent=signup_window)
                    return

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                cursor.execute("INSERT INTO registration_credentials (email, username, password) VALUES (%s, %s, %s)",
                               (email, username, hashed_password))
                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Account created successfully!", parent=signup_window)
                signup_window.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}", parent=signup_window)

        register_button = tk.Button(signup_window, text="Register", font=('Winky Rough', 16, 'bold'),
                                    bg="#4783C2", fg="white", activebackground="#81ABBC", activeforeground="black",
                                    width=12, height=1, bd=3, relief="raised", cursor="hand2", command=register_user)
        register_button.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()





