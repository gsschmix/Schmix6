import tkinter as tk
import frames
from tkinter.messagebox import showinfo
import os


# function to call the password and username from the user
def startup(root):
    # create new frame to be used in root
    start = tk.Frame(root, height=300, width=200, borderwidth=10, bg='gray',
                     relief='raised')
    start.grid(column=0, row=0, padx=20, pady=40)

    # configure columns of start
    start.columnconfigure(0, weight=1)
    start.columnconfigure(1, weight=3)

    # add labels to start
    tk.Label(start, text="Schmix6", bg='gray',
             fg='aqua', font=("Castellar", 50))\
        .grid(columnspan=2, column=0, row=1)
    tk.Label(start, text="Welcome!", bg='gray', fg='white',
             font=("Times", 45)).grid(columnspan=2, column=0, row=0)
    tk.Label(start, text="V.1.0", bg='gray', font=("Times", 10))\
        .grid(column=1, row=2, sticky="se")
    tk.Label(start, text="2023", bg='gray', font=("Times", 10))\
        .grid(column=0, row=2, sticky="sw")

    # add continue button to start
    tk.Button(start, text="Press to continue...", font=("Times", 20),
              bg='gray', fg='white', command=lambda: swap(start, root))\
        .grid(columnspan=2, column=0, row=2, sticky="s")


# function used to create a frame for login
def credentials(root):
    # Sign in frame
    signin = tk.Frame(root, bg="grey")
    signin.pack(padx=10, pady=10, fill='x', expand=True)

    # variables to store user input
    username = tk.StringVar()
    password = tk.StringVar()

    def login_clicked(event):
        # if the username and password match their respective values,
        # open home page. These values are gotten from the OS
        if (username.get() == os.environ.get('USER') and
                password.get() == os.environ.get('PASS*****')):
            root.destroy()
            frames.new_start()

        # else, prompt for reentry in a new window
        else:
            msg = f'Your password and/or your username is incorrect'
            showinfo(
                title='Information',
                message=msg
            )

    # username prompt
    username_label = tk.Label(signin, text="Username:", bg="grey")
    username_label.pack(expand=True, anchor="w")

    # username entry
    username_entry = tk.Entry(signin, textvariable=username)
    username_entry.pack(fill='x', expand=True)
    username_entry.focus()

    # password prompt
    password_label = tk.Label(signin, text="Password:", bg="grey")
    password_label.pack(expand=True, anchor="w")

    # password entry
    password_entry = tk.Entry(signin, textvariable=password, show="*")
    password_entry.pack(fill='x', expand=True)

    # login button
    login_button = tk.Button(signin)
    login_button.configure(text="Enter",
                           command=lambda: login_clicked('<Return>'),
                           bg="lightgrey", border=2, activebackground="grey")
    login_button.pack(fill='x', expand=True, pady=10)
    signin.bind_all('<Return>', login_clicked)

    # return signin frame to the original function
    return signin


# this function destroys the original frame, and
# calls the next frame
def swap(start, root):
    start.destroy()
    credentials(root)


def win():
    # create root window
    root = tk.Tk()
    root.configure(bg="grey")
    root.title("Login")
    root.geometry("400x300+450+150")
    root.resizable(False, False)

    # call startup to create a frame within root
    startup(root)

    # run root
    root.mainloop()


# start program
if __name__ == '__main__':
    win()
