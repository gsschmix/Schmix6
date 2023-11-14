import tkinter as tk
import webbrowser
from cryptocurrencies import cryptocurrencies
from start_up import home
from interactions import find_all_crypto
from assets import my_assets
from backtest import backtesting
from documentation import doc


# function used to access Coinbase directly
def web_access():
    webbrowser.open('https://www.coinbase.com/', autoraise=True)


# function used to create button frame and
# declare the frame to be used when the button is clicked
def button_frame(win1, first_call):

    # initialize variables to be used in the function
    crypto = find_all_crypto()
    letter_color = '#d6d6d6'

    # create frame to hold button widgets
    bframe = tk.Frame(win1, bg="gray", relief="raised", borderwidth=5)
    bframe.grid(column=0, row=0, sticky='N', rowspan=2, pady=10, padx=10)

    # load home screen when program is first started
    if first_call:
        home_frame = home(win1, letter_color)
        first_call = False

    # create Home button and configure it on the button frame
    homeb = tk.Button(bframe, text='Schmix6', bg="gray",
                      relief="flat", font=('Castellar', 25),
                      command=lambda: home_frame.tkraise())
    homeb.grid(column=0, row=0)

    # create Cryptocurrencies button and configure it on the button frame
    cryptob = tk.Button(bframe, text='Cryptocurrencies', bg="lightgray",
                        font=('Times', 15), width=15, command=lambda:
                        cryptocurrencies(win1, letter_color, crypto))
    cryptob.grid(column=0, row=1)

    # create My Assets button and configure it on the button frame
    assetsb = tk.Button(bframe, text='My Assets', bg="lightgray",
                        font=('Times', 15), width=15,
                        command=lambda: my_assets(win1, letter_color, crypto))
    assetsb.grid(column=0, row=2)

    # create Backtest button and configure it on the button frame
    backtestb = tk.Button(bframe, text='Backtest', bg="lightgray",
                          font=('Times', 15), width=15,
                          command=lambda: backtesting(win1, letter_color,
                                                      crypto))
    backtestb.grid(column=0, row=3)

    # create Documentation button and configure it on the button frame
    documentb = tk.Button(bframe, text='Documentation', bg="lightgray",
                          font=('Times', 15), width=15,
                          command=lambda: doc(win1, letter_color))
    documentb.grid(column=0, row=4)

    # create Website button and configure it on the button frame
    websiteb = tk.Button(bframe, text='Coinbase', bg="lightgray",
                         command=web_access, font=('Times', 15), width=15)
    websiteb.grid(column=0, row=5)

    # add additional arguments to all the button grids
    for widget in bframe.winfo_children():
        widget.grid(padx=5, pady=5, sticky="w")

    win1.mainloop()


# function for creating a new window
def new_start():
    # create window to house button frames and other frames
    win1 = tk.Tk()
    win1.configure(bg="black")
    win1.title("CrytpoBot Trading")

    # create a variables for the screen width and height
    screen_width = int(win1.winfo_screenwidth() * 4 / 5)
    screen_height = int(win1.winfo_screenheight() * 4 / 5)

    # find the center of the computer's screen
    centerx = int(win1.winfo_screenwidth() / 2 - screen_width / 2)
    centery = int(win1.winfo_screenheight() / 2 - screen_height / 2)

    # configure window
    win1.geometry(f'{screen_width}x{screen_height}+{centerx}+{centery}')
    win1.resizable(False, False)
    # configure the columns
    win1.columnconfigure(0, weight=0)
    win1.columnconfigure(1, weight=5)

    # call button_frame function to create a new frame
    button_frame(win1, True)
