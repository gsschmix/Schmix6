from tkinter import ttk
import tkinter as tk
from interactions import CoinbaseTransactions, prices, price_graph
from datetime import datetime
import dateutil.relativedelta
from pytz import timezone
from creation import create_window


# this function is used to get additional transactions from the
# provided Coinbase account
def call_more_transactions(crypto, tr_object):
    # create a new window
    win2 = create_window(crypto)

    # create a new canvas to hold all the new transactions
    canvas = tk.Canvas(win2, bg="#262629")

    # get a list of 10 transactions and at it to the canvas
    trList = tr_object.list_of_transactions(canvas, [crypto], False, 10)
    trList.grid(column=0, row=0, pady=5)
    canvas.grid(column=0, row=0)

    # mainloop to run the window
    win2.mainloop()


# this is used to create a new window to view the specified cryptocurrency
def crypto_win(crypto, letter_color):
    # create and initialize new window
    win1 = create_window(crypto)
    win1.rowconfigure(0, weight=1)
    win1.rowconfigure(1, weight=4)
    win1.rowconfigure(2, weight=2)
    win1.columnconfigure(0, weight=5)
    win1.columnconfigure(1, weight=1)

    # initialize variables to hold times for previous month, week, and day
    today_date = datetime.now(timezone('UTC')).date()
    yesterday_time = (today_date + dateutil.relativedelta
                      .relativedelta(days=-1)).strftime("%Y-%m-%d")
    week_time = (today_date + dateutil.relativedelta
                 .relativedelta(weeks=-1)).strftime("%Y-%m-%d")
    month_time = (today_date + dateutil.relativedelta
                  .relativedelta(months=-1)).strftime("%Y-%m-%d")

    # create a new object from Coinbase Transactions
    tr_object = CoinbaseTransactions()

    # create a label for the crypto name
    tk.Label(win1, bg="#262629", fg=letter_color, text=crypto, relief="raised",
             anchor='w', font=('Castellar', 50))\
        .grid(column=0, row=0, pady=2, padx=2, sticky="W")

    # create a variable for the timeFrame selection
    time_frame = tk.StringVar()

    # create a combobox with timeFrame as it's text variable
    time_selector = ttk.Combobox(win1, textvariable=time_frame)

    # initialize values of the combobox, and set the initial value to Month
    time_selector["values"] = ["Day", "Week", "Month"]
    time_selector.current(2)

    # prevent typing a value
    time_selector['state'] = 'readonly'

    # add time selector to the grid
    time_selector.grid(column=1, row=1, padx=2, sticky="N")

    # get prices from each timeframe
    month_list = (prices(crypto, month_time, 86400, today_date))
    week_list = (prices(crypto, week_time, 3600, today_date))
    day_list = (prices(crypto, yesterday_time, 300, today_date))
    graph_frame = tk.Frame(win1)

    # create a label that will hold the percent of increase or decrease
    percent_label = tk.Label(win1, bg="#262629", width=20, height=4)

    # create the initial graph to be shown upon startup
    coin_graph = price_graph(graph_frame, month_list)
    coin_graph.get_tk_widget().grid(column=0, row=0, pady=2, sticky="W")
    inc_dec = ((month_list[len(month_list) - 1] - month_list[0]) /
               month_list[0]) * 100

    # if it is a decrement, make the color red
    if inc_dec < 0:
        fg_col = "red"

    # if it is an increment, make it green
    else:
        fg_col = "green"

    # plot the percent
    percent_label.configure(text="%" + str(inc_dec), font="Castellar",
                            fg=fg_col)

    percent_label.grid_propagate(False)

    # grid the widgets
    graph_frame.grid(column=0, row=1, sticky="W")
    percent_label.grid(column=0, row=0, pady=2)

    # definition used to call a graph
    def call_graph(event):
        # forget any previous percent_label
        percent_label.grid_forget()

        # initialize variables
        inc_dec = None
        coin_graph = None

        # forget any widgets in graph_frame
        for widget in graph_frame.winfo_children():
            widget.grid_forget()

        # if the time in timeframe is a month
        if time_frame.get() == "Month":
            # create a price_graph
            coin_graph = price_graph(graph_frame, month_list)

            # get the increment or decrement for the month
            inc_dec = ((month_list[len(month_list) - 1] - month_list[0]) /
                       month_list[0]) * 100

        # if the time in timeframe is a week
        elif time_frame.get() == "Week":
            # create a price_graph
            coin_graph = price_graph(graph_frame, week_list)

            # get the increment or decrement for the week
            inc_dec = ((week_list[len(week_list) - 1] - week_list[0]) /
                       week_list[0]) * 100

        # if the time in timeframe is a day
        elif time_frame.get() == "Day":
            # create a price_graph
            coin_graph = price_graph(graph_frame, day_list)

            # get the increment or decrement for the day
            inc_dec = ((day_list[len(day_list) - 1] - day_list[0]) /
                       day_list[0]) * 100

        # if it is a decrement, make the color red
        if inc_dec < 0:
            fg_col = "red"

        # if it is an increment, make it green
        else:
            fg_col = "green"

        # plot the percent
        percent_label.configure(text="%" + str(inc_dec), font="Castellar",
                                fg=fg_col)

        # grid any widgets
        coin_graph.get_tk_widget().grid(column=0, row=0, pady=2, padx=2,
                                        sticky="W")
        percent_label.grid(column=0, row=0, pady=2)

    # bind the timeframe selector to the function
    time_selector.bind("<<ComboboxSelected>>", call_graph)

    # create a new transaction list
    tr_list = tr_object.list_of_transactions(win1, [crypto], False, 3)
    tr_list.configure(bg="#262629")
    tr_list.grid(column=0, row=2, pady=2, padx=3, sticky="SW")

    # create a button to show more transactions
    tk.Button(win1, text="More", bg="#262629", fg=letter_color,
              font=("Castellar", 20),
              command=lambda: call_more_transactions(crypto, tr_object)).grid(
        column=0, row=2, pady=2, sticky="E")

    # mainloop
    win1.mainloop()


def cryptocurrencies(win1, letter_color, crypto_list):
    # create a new frame to be used
    crypto_currencies = tk.Frame(win1, bg="#262629", width=900, height=650,
                                 borderwidth=5, relief="raised")
    crypto_currencies.grid(column=1, row=0, pady=20)
    crypto_currencies.grid_propagate(False)

    # create a new label
    tk.Label(crypto_currencies, bg=crypto_currencies["bg"], fg=letter_color,
             text="Cryptocurrencies", font=('Castellar', 50))\
        .grid(column=0, row=0)

    # create a frame for the crypto list
    crypto_frame = tk.Frame(crypto_currencies, bg="#262629", width=800,
                            height=250, borderwidth=5, relief="raised")
    crypto_frame.grid(column=0, row=7)

    # create a listbox for all the cryptocurrencies
    listbox = tk.Listbox(crypto_frame, font=["Castellar", 20], bg="black",
                         fg="white", height=6, selectmode=tk.SINGLE)

    # initialize the values of the listbox
    n = 0
    for i in crypto_list:
        listbox.insert(n, i)
        n = n + 1

    # event function
    def items_selected():
        crypto_win(str(listbox.get(listbox.curselection())), letter_color)

    # create a button to call a new crypto window
    btn = tk.Button(crypto_frame, text='Open Window', command=items_selected)
    btn.grid(columnspan=2, column=0, row=1, pady=3)

    # put the listbox on the grid
    listbox.grid(column=0, row=0, padx=3, pady=3)

    # raise the frame
    crypto_currencies.tkraise()
