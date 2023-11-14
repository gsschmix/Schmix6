import tkinter as tk

# function used to create a button
def create_button(container, txt):
    # return a fully created button
    btn = tk.Button(container, text=txt, bg="lightgray",
                    font=('Times', 15), width=15)

    return btn


# this function creates a new window
def create_window(name):
    # create a new window that will raise above any other
    # windows
    win1 = tk.Toplevel()
    win1.configure(bg="black")
    win1.title(name)

    # create a variables for the screen width and height
    screen_width = int(win1.winfo_screenwidth() * 4 / 5)
    screen_height = int(win1.winfo_screenheight() * 4 / 5)

    # find the center of the computer's screen
    centerx = int(win1.winfo_screenwidth() / 2 - screen_width / 2)
    centery = int(win1.winfo_screenheight() / 2 - screen_height / 2)

    # configure window
    win1.geometry(f'{screen_width}x{screen_height}+{centerx}+{centery}')
    win1.resizable(False, False)

    return win1