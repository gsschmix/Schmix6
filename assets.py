import tkinter as tk
import datetime
import dateutil.relativedelta
from cryptocurrencies import create_window, call_more_transactions
from interactions import CoinbaseTransactions, asset_usd_amount, price_graph, \
    get_balance
from datetime import datetime
import dateutil.relativedelta
from pytz import timezone


# function used to create a window for assets
def asset_win(crypto, letter_color, month_time, week_time,
              yesterday_time, today_date):

    # create new window and configure it
    win2 = create_window(crypto)
    win2.rowconfigure(0, weight=1)
    win2.rowconfigure(1, weight=4)
    win2.rowconfigure(2, weight=2)
    win2.columnconfigure(0, weight=5)
    win2.columnconfigure(1, weight=1)

    # initialize variables for later use
    value = 0
    do = True
    inc_dec = "None within the past month."
    fg_col = "black"

    # create a new object from Coinbase Transactions
    tr_object = CoinbaseTransactions()

    # get amount of used assets
    new_list = asset_usd_amount(crypto, month_time, 86400, today_date)

    # greate a graph of the assets and put it on the grid
    new_graph = price_graph(win2, new_list)
    new_graph.get_tk_widget().grid(column=0, row=1)

    # create labels for the frame and put them on the grid
    tk.Label(win2, bg="Black", fg=letter_color, text="Monthly High: $"
             + str(round(new_list.max(), 4)), font=('Castellar', 15),
             relief="raised").grid(column=0, row=0, sticky="SE")
    tk.Label(win2, bg="Black", fg=letter_color, text="Weekly High: $"
             + str(round(new_list[new_list.index > week_time].max(), 4)),
             font=('Castellar', 15), relief="raised")\
        .grid(column=0, row=0, sticky="E")
    tk.Label(win2, bg="Black", fg=letter_color, text="Daily High: $"
             + str(round(new_list[new_list.index > yesterday_time].max(), 4)),
             font=('Castellar', 15), relief="raised")\
        .grid(column=0, row=0, sticky="NE")
    tk.Label(win2, bg="#262629", fg=letter_color, text=crypto, relief="raised",
             anchor='w', font=('Castellar', 50))\
        .grid(column=0, row=0, pady=2, padx=2, sticky="W")
    percentLabel = tk.Label(win2, bg="#262629", height=4)

    # check to see if the list is full of null values
    for i in range(0, len(new_list)):
        if new_list[i] > 0:
            value = i
            break
        elif new_list[len(new_list)-1] == 0:
            do = False

    # if there are values for which new_list is not null, calculate
    # the increase/decrease
    if do:
        inc_dec = ((new_list[len(new_list) - 1]-new_list[value])
                   / new_list[value])
        if inc_dec < 0:
            fg_col = "red"
        else:
            fg_col = "green"
        inc_dec = inc_dec * 100

    # configure the percent label to include the text and color of the
    # increase/decrease and add it to the grid
    percentLabel.configure(text="%" + str(inc_dec),
                           font="Castellar", fg=fg_col, relief="raised")
    percentLabel.grid(column=0, row=0, pady=2)

    # get a list of 3 transactions
    trList = tr_object.list_of_transactions(win2, [crypto], False, 3)
    trList.configure(bg="#262629")
    trList.grid(column=0, row=2, pady=2, padx=3, sticky="SW")

    # button used to get more transactions
    tk.Button(win2, text="More", bg="#262629", fg=letter_color,
              font=("Castellar", 20),
              command=lambda: call_more_transactions(crypto, tr_object))\
        .grid(column=0, row=2, pady=2, sticky="E")

    # mainloop
    win2.mainloop()


# this function is used to create the my_assets frame
def my_assets(win1, letter_color, crypto):
    # create the my_assets frame and configure it
    assets_frame = tk.Frame(win1, bg="#262629", width=900, height=650,
                            borderwidth=5, relief="raised")
    assets_frame.grid(column=1, row=0, pady=20)
    assets_frame.grid_propagate(False)
    assets_frame.rowconfigure(0, weight=1)
    assets_frame.rowconfigure(1, weight=4)
    assets_frame.rowconfigure(2, weight=2)
    assets_frame.columnconfigure(0, weight=5)
    assets_frame.columnconfigure(1, weight=1)

    # get USD balance
    usd_balance = get_balance("USD")

    # initialize starting variables to be used for later
    today_date = datetime.now(timezone('UTC')).date()
    yesterday_time = (today_date + dateutil.relativedelta.
                      relativedelta(days=-1)).strftime("%Y-%m-%d")
    week_time = (today_date + dateutil.relativedelta.
                 relativedelta(weeks=-1)).strftime("%Y-%m-%d")
    month_time = (today_date + dateutil.relativedelta.
                  relativedelta(months=-1)).strftime("%Y-%m-%d")

    # initialize lists
    combined_list = asset_usd_amount(crypto[0], month_time, 86400, today_date)
    crypto_balances = [get_balance(crypto[0])]
    # get all the crypto amounts in USD and their balances
    for i in crypto[1:]:
        try:
            crypto_balances.append(get_balance(i))
            old_crypto = combined_list
            new_list = asset_usd_amount(i, month_time, 86400, today_date)
            combined_list = new_list.astype(float) + old_crypto.astype(float)
        except AttributeError:
            continue

    # create a name label for the frame
    tk.Label(assets_frame, bg=assets_frame["bg"], fg=letter_color,
             text="My Assets", font=('Castellar', 50))\
        .grid(column=0, row=0, sticky="W")

    # create labels for the monthly, weekly, and daily highs
    tk.Label(assets_frame, bg="Black", fg=letter_color,
             text="Monthly High: $" + str(round(combined_list.max(), 2)),
             font=('Castellar', 15), relief="raised")\
        .grid(column=0, row=0, sticky="SE")
    tk.Label(assets_frame, bg="Black", fg=letter_color,
             text="Weekly High: $" + str(round(
                 combined_list[combined_list.index > week_time].max(), 2)),
             font=('Castellar', 15), relief="raised") \
        .grid(column=0, row=0, sticky="E")
    tk.Label(assets_frame, bg="Black", fg=letter_color,
             text="Daily High: $" + str(round(
                 combined_list[combined_list.index > yesterday_time].max(), 2)),
             font=('Castellar', 15), relief="raised") \
        .grid(column=0, row=0, sticky="NE")

    # create labels for available crypto and USD
    tk.Label(assets_frame, bg="Black", fg=letter_color,
             text="Available USD:\n$" + str(usd_balance),
             font=('Castellar', 15), relief="raised")\
        .grid(column=0, row=7, sticky='N')
    tk.Label(assets_frame, bg="Black", fg=letter_color,
             text="Available Crypto:\n$"
                  + str(combined_list.values[len(combined_list)-1]),
             font=('Castellar', 15), relief="raised")\
        .grid(column=0, row=7, sticky="S")

    # create a new graph based on the USD crypto amounts
    new_graph = price_graph(assets_frame, combined_list)
    new_graph.get_tk_widget().grid(column=0, row=1)

    # create a new frame to hold a listbox
    crypto_list = tk.Frame(assets_frame, bg="#262629",
                           borderwidth=5, relief="raised")
    crypto_list.grid(column=0, row=7, sticky="E")

    # create a listbox
    listbox = tk.Listbox(crypto_list, font=["Castellar", 20], bg="black",
                         width=10, fg="white", height=2, selectmode=tk.SINGLE)

    # initialize the listbox
    n = 0
    for i in crypto:
        listbox.insert(n, i)
        n = n + 1

    # create a text area to hold the balances of the cryptocurrencies
    txt_area = tk.Text(assets_frame, bg="black", fg="cyan", width=25, height=5)

    # get the values for the balances, and add the text to the text area
    for i in range(0, len(crypto)):
        text = (str(crypto[i]) + " Balance:" + str(crypto_balances[i]) + "\n")
        txt_area.insert(tk.END, text)

    # function used to call a new window
    def items_selected():
        asset_win(str(listbox.get(listbox.curselection())), letter_color,
                  month_time, week_time, yesterday_time, today_date)

    # button used to open the new window
    btn = tk.Button(crypto_list, text='Open Window', command=items_selected)
    btn.grid(columnspan=2, column=0, row=1, pady=3)

    # add the listbox and text area to the grid
    listbox.grid(column=0, row=0, padx=3, pady=3)
    txt_area.grid(column=0, row=7, sticky="W")

    # raise frame above other frames
    assets_frame.tkraise()

