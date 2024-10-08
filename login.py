from customtkinter import *
from tkinter import messagebox
from PIL import Image
import sqlite3

# Db
conn = sqlite3.connect('lib_users.db')
cursor = conn.cursor()

# Create lib_users
cursor.execute('''CREATE TABLE IF NOT EXISTS lib_users (
                    username TEXT PRIMARY KEY, 
                    password TEXT,
                    mobile TEXT,
                    email TEXT)''')
conn.commit()

# login
def login():
    username = login_usrname_entry.get().strip()
    password = login_passwd_entry.get().strip()

    cursor.execute("SELECT * FROM lib_users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# account creation
def create_account():
    username = signup_usrname_entry.get()
    password = signup_passwd_entry.get()
    mobile = mobile_entry.get()
    email = email_entry.get()

    if username and password and mobile and email:
        try:
            cursor.execute("INSERT INTO lib_users (username, password, mobile, email) VALUES (?, ?, ?, ?)", 
                           (username, password, mobile, email))
            conn.commit()
            messagebox.showinfo("Signup Successful", f"Account created for {username}!")
            show_login_frame()  # Return to login after successful signup
        except sqlite3.IntegrityError:
            messagebox.showerror("Signup Failed", "Username already exists!")
    else:
        messagebox.showerror("Input Error", "Please fill in all fields.")

# forgot password
def forgot_password():
    username = login_usrname_entry.get()

    if username:
        cursor.execute("SELECT password FROM lib_users WHERE username=?", (username,))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Password Recovery", f"Your password is: {result[0]}")
        else:
            messagebox.showerror("Error", "Username not found!")
    else:
        messagebox.showerror("Input Error", "Please enter your username.")

# display the signup form
def show_signup_frame():
    frame1.grid_forget()  # Hide  login frame
    frame_signup.grid(row=0, column=1, padx=40)  # Show signup frame

# display the login 
def show_login_frame():
    frame_signup.grid_forget()  # Hide signup frame
    frame1.grid(row=0, column=1, padx=40)  # Show login frame

# Hoverfor Create Account
def on_create_hover(event):
    cr_acc.configure(text_color="blue") 

def on_create_leave(event):
    cr_acc.configure(text_color="#0085FF") 

# Hover for fpw
def on_forgot_hover(event):
    fpw_label.configure(text_color="red") 

def on_forgot_leave(event):
    fpw_label.configure(text_color="#FF4500")  

# Main windw
main = CTk()
main.title("Login/Signup Page")
main.config(bg="white")
main.resizable(False, False)

bg_img = CTkImage(dark_image=Image.open(r"C:\Users\Dell\Downloads\pikaso_texttoimage_library-management-cartoon-story.jpeg"), size=(500, 500))

bg_lab = CTkLabel(main, image=bg_img, text="")
bg_lab.grid(row=0, column=0)

# LoginFrame
frame1 = CTkFrame(main, fg_color="#D9D9D9", bg_color="white", height=400, width=300, corner_radius=20)
frame1.grid(row=0, column=1, padx=40)

title = CTkLabel(frame1, text="Welcome Back! \nLogin to Account", text_color="black", font=("", 35, "bold"))
title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

login_usrname_entry = CTkEntry(frame1, text_color="black", placeholder_text="Username", fg_color="white", 
                         placeholder_text_color="gray", font=("", 16, "bold"), width=200, corner_radius=15, height=45)
login_usrname_entry.grid(row=1, column=0, sticky="nwe", padx=30)

login_passwd_entry = CTkEntry(frame1, text_color="black", placeholder_text="Password", fg_color="white", 
                         placeholder_text_color="gray", font=("", 16, "bold"), width=200, corner_radius=15, height=45, show="*")
login_passwd_entry.grid(row=2, column=0, sticky="nwe", padx =30, pady=20)

# Create account link
cr_acc = CTkLabel(frame1, text="Create Account!", text_color="#0085FF", cursor="hand2", font=("", 15))
cr_acc.grid(row=3, column=0, sticky="w", pady=20, padx=40)
cr_acc.bind("<Enter>", on_create_hover)
cr_acc.bind("<Leave>", on_create_leave)
cr_acc.bind("<Button-1>", lambda e: show_signup_frame())  # Bind click event to show signup form

# Forgot password link
fpw_label = CTkLabel(frame1, text="Forgot Password?", text_color="#FF4500", cursor="hand2", font=("", 15))
fpw_label.grid(row=3, column=0, sticky="e", pady=20, padx=40)
fpw_label.bind("<Enter>", on_forgot_hover)
fpw_label.bind("<Leave>", on_forgot_leave)
fpw_label.bind("<Button-1>", lambda e: forgot_password())  # Bind click event to forgot password

# Loginbtn
l_btn = CTkButton(frame1, text="Login", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                  corner_radius=15, command=login)  # Bind login function
l_btn.grid(row=4, column=0, sticky="ne", pady=20, padx=35)

# Signupframe
frame_signup = CTkFrame(main, fg_color="#D9D9D9", bg_color="white", height=400, width=300, corner_radius=20)

# Back
back_btn = CTkButton(frame_signup, text="← Back", font=("", 15), height=30, width=60, fg_color="gray", cursor="hand2",
                     corner_radius=10, command=show_login_frame)
back_btn.grid(row=0, column=0, sticky="nw", pady=10, padx=10)

title_signup = CTkLabel(frame_signup, text="Create an Account", text_color="black", font=("", 35, "bold"))
title_signup.grid(row=1, column=0, sticky="nw", pady=30, padx=10)

signup_usrname_entry = CTkEntry(frame_signup, text_color="black", placeholder_text="Username", fg_color="white", 
                         placeholder_text_color="gray", font=("", 16, "bold"), width=200, corner_radius=15, height=45)
signup_usrname_entry.grid(row=2, column=0, sticky="nwe", padx=30)

signup_passwd_entry = CTkEntry(frame_signup, text_color="black", placeholder_text="Password", fg_color="white", 
                         placeholder_text_color="gray", font=("", 16, "bold"), width=200, corner_radius=15, height=45, show="*")
signup_passwd_entry.grid(row=3, column=0, sticky="nwe", padx=30, pady=20)

mobile_entry = CTkEntry(frame_signup, text_color="black", placeholder_text="Mobile Number", fg_color="white", 
                        placeholder_text_color="gray", font=("", 16, "bold"), width=200, corner_radius=15, height=45)
mobile_entry.grid(row=4, column=0, sticky="nwe", padx=30, pady=20)

email_entry = CTkEntry(frame_signup, text_color="black", placeholder_text="Email", fg_color="white", 
                        placeholder_text_color="gray", font=("", 16, "bold"), width=200, corner_radius=15, height=45)
email_entry.grid(row=5, column=0, sticky="nwe", padx=30, pady=20)

# Signupbtn
signup_btn = CTkButton(frame_signup, text="Signup", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                       corner_radius=15, command=create_account)
signup_btn.grid(row=6, column=0, sticky="ne", pady=20, padx=35)

main.mainloop()

# Close dbb
conn.close()