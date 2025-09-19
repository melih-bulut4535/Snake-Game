# Name&Surname: Melih Bulut
# Date: 14.09.2022
# SNAKE GAME
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

connection = mysql.connector.connect(host='localhost', user='root', port='3306',
                                     password='We1ih.Bu1ut', database='pythongui')
c = connection.cursor()

W = 1000
H = 600

root = Tk()
root.geometry("1000x600")

background_image = ImageTk.PhotoImage(file="background.jpg")
my_canvas = Canvas(root, width=W, height=H, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=background_image, anchor="nw")

image = Image.open("snake_logo.jpg")
test = ImageTk.PhotoImage(image)
label1 = Label(image=test)
label1.image = test
label1.place(x=45, y=50)

# ----------- Login Page ------------- #

my_canvas.create_rectangle(550, 50, 950, 550, outline="#203354", fill="#203354", width=2)
my_canvas.pack()


def login_page():
    global title_label, username_label, password_label, password_entry, username_entry, password_entry \
        , login_button, go_register_label
    title_label = Label(root, text='LOGIN TO SNAKE GAME', bg='#203354', fg='white', font=('Tahoma', 24))
    my_canvas.create_window(565, 80, anchor="nw", window=title_label)

    username_label = Label(root, text='Username:', font=('Verdana', 10), fg="white", bg="#203354")
    password_label = Label(root, text='Password:', font=('Verdana', 10), fg="white", bg="#203354")

    my_canvas.create_window(570, 150, anchor="nw", window=username_label)
    my_canvas.create_window(570, 240, anchor="nw", window=password_label)

    username_entry = Entry(root, font=('Verdana', 16), width=14, fg="#336d92")
    password_entry = Entry(root, font=('Verdana', 16), width=14, fg="#336d92")

    username_entry.insert(0, "Username")
    password_entry.insert(0, "Password")

    my_canvas.create_window(570, 180, anchor="nw", window=username_entry)
    my_canvas.create_window(570, 270, anchor="nw", window=password_entry)

    login_button = Button(root, text="Login", font=('Verdana', 16), bg='#2980b9', fg='#fff', padx=10, pady=5, width=10)
    my_canvas.create_window(640, 470, anchor="nw", window=login_button)

    go_register_label = Label(root, text=">> Don't have an account? Create one", bg="#203354", font=('Verdana', 10),
                              fg='white')
    my_canvas.create_window(570, 370, anchor="nw", window=go_register_label)

    username_entry.bind("<Button-1>", entry_clear)
    password_entry.bind("<Button-1>", entry_clear)
    login_button['command'] = login
    root.bind('<Return>', lambda event: login())
    go_register_label.bind("<Button-1>", lambda page: go_to_register())


def entry_clear(e):
    if username_entry.get() == "Username":
        username_entry.delete(0, END)
    elif password_entry.get() == "Password":
        password_entry.delete(0, END)
        password_entry.config(show="*")


# create a function to make the user login
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    vals = (username, password,)
    select_query = "SELECT * FROM `users` WHERE `username` = %s and `password` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        root.destroy()
        add_username = open("username_score.txt", "a+")
        write_username = open("username.txt", "w")
        f1 = open("user_score.txt", 'a+')
        f1.writelines("\n")
        write_username.write(str(username))
        add_username.write(str(username) + "\n")
        f1.close()
        add_username.close()
        write_username.close()
        import main
        main.MAIN().draw_score()

    else:
        messagebox.showwarning('Error', 'wrong username or password')


def go_to_register():
    title_label.destroy()
    username_label.destroy()
    password_label.destroy()
    username_entry.destroy()
    password_entry.destroy()
    login_button.destroy()
    go_register_label.destroy()
    register_page()


# ----------- Register Page ------------- #
def register_page():
    global fullname_entry_rg, username_entry_rg, password_entry_rg, confirmpass_entry_rg, go_login_label, \
        fullname_label_rg, username_label_rg, password_label_rg, confirmpass_label_rg, gender_label_rg, register_button\
        , male_radiobutton, female_radiobutton, title_label_rg

    title_label_rg = Label(root, text='REGISTER', bg='#203354', fg='white', font=('Tahoma', 24))

    fullname_label_rg = Label(root, text='Fullname:', font=('Verdana', 14), fg="white", bg="#203354")
    username_label_rg = Label(root, text='Username:', font=('Verdana', 14), fg="white", bg="#203354")
    password_label_rg = Label(root, text='Password:', font=('Verdana', 14), fg="white", bg="#203354")
    confirmpass_label_rg = Label(root, text='Re-Password:', font=('Verdana', 14), fg="white", bg="#203354")
    gender_label_rg = Label(root, text='Gender:', font=('Verdana', 14), fg="white", bg="#203354")

    fullname_entry_rg = Entry(root, font=('Verdana', 14), width=22)
    username_entry_rg = Entry(root, font=('Verdana', 14), width=22)
    password_entry_rg = Entry(root, font=('Verdana', 14), width=22, show='*')
    confirmpass_entry_rg = Entry(root, font=('Verdana', 14), width=22, show='*')

    gender = StringVar()
    gender.set('Male')
    male_radiobutton = Radiobutton(root, text='Male', font=('Verdana', 14), variable=gender, value='Male',
                                   fg="white", bg="#203354")
    female_radiobutton = Radiobutton(root, text='Female', font=('Verdana', 14), variable=gender, value='Female',
                                     fg="white", bg="#203354")

    register_button = Button(root, text="Register", font=('Verdana', 16), bg='#2980b9', fg='#fff', padx=15,
                             pady=5, width=15)

    go_login_label = Label(root, text=">> Already have an account? Sign in", bg="#203354", font=('Verdana', 10),
                           fg='white')

    my_canvas.create_window(565, 80, anchor="nw", window=title_label_rg)

    my_canvas.create_window(570, 130, anchor="nw", window=fullname_label_rg)
    my_canvas.create_window(570, 190, anchor="nw", window=username_label_rg)
    my_canvas.create_window(570, 270, anchor="nw", window=password_label_rg)
    my_canvas.create_window(570, 350, anchor="nw", window=confirmpass_label_rg)

    my_canvas.create_window(570, 160, anchor="nw", window=fullname_entry_rg)
    my_canvas.create_window(570, 220, anchor="nw", window=username_entry_rg)
    my_canvas.create_window(570, 300, anchor="nw", window=password_entry_rg)
    my_canvas.create_window(570, 380, anchor="nw", window=confirmpass_entry_rg)

    my_canvas.create_window(570, 430, anchor="nw", window=gender_label_rg)
    my_canvas.create_window(690, 430, anchor="nw", window=male_radiobutton)
    my_canvas.create_window(820, 430, anchor="nw", window=female_radiobutton)

    my_canvas.create_window(570, 460, anchor="nw", window=go_login_label)

    my_canvas.create_window(650, 490, anchor="nw", window=register_button)

    go_login_label.bind("<Button-1>", lambda page: go_to_login())
    register_button['command'] = register


# create a function to display the login frame
def go_to_login():
    title_label_rg.destroy()
    fullname_label_rg.destroy()
    username_label_rg.destroy()
    password_label_rg.destroy()
    confirmpass_label_rg.destroy()
    gender_label_rg.destroy()
    fullname_entry_rg.destroy()
    username_entry_rg.destroy()
    password_entry_rg.destroy()
    confirmpass_entry_rg.destroy()
    gender_label_rg.destroy()
    male_radiobutton.destroy()
    female_radiobutton.destroy()
    go_login_label.destroy()
    register_button.destroy()
    login_page()


# create a function to check if the username already exists
def check_username():
    username = username_entry_rg.get().strip()
    vals = (username,)
    select_query = "SELECT * FROM `users` WHERE `username` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        return True
    else:
        return False


# create a function to register a new user
def register():
    fullname = fullname_entry_rg.get().strip()  # remove white space
    username = username_entry_rg.get().strip()
    password = password_entry_rg.get().strip()
    confirm_password = confirmpass_entry_rg.get().strip()

    if len(fullname) > 0 and len(username) > 0 and len(password) > 0:
        if not check_username():
            if password == confirm_password:
                vals = (fullname, username, password)
                insert_query = "INSERT INTO users(fullname, username, password) VALUES( %s, %s, %s)"
                c.execute(insert_query, vals)
                connection.commit()
                messagebox.showinfo('Register', 'your account has been created successfully')
            else:
                messagebox.showwarning('Password', 'incorrect password confirmation')

        else:
            messagebox.showwarning('Duplicate Username', 'This Username Already Exists,try another one')
    else:
        messagebox.showwarning('Empty Fields', 'make sure to enter all the information')


login_page()
root.mainloop()
