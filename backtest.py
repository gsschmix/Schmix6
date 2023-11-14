from datetime import datetime
import dateutil.relativedelta
from pytz import timezone
from interactions import prices
import matplotlib.pyplot as plt
import tkinter as tk
from creation import create_button


def datatest(container, indicator, crypto_type):
    # initialize time variables for the function
    today_date = datetime.now(timezone('UTC')).date()
    yesterday_time = (today_date + dateutil.relativedelta
                      .relativedelta(days=-1)).strftime("%Y-%m-%d")

    # get price data
    coinMonthList = prices(crypto_type, yesterday_time, 300, today_date, True)

    # create other variables for function
    signaling = "0"
    signal_color = "black"

    # add indicators
    coinMonthList["SMA_10"] = coinMonthList['Close'].rolling(10).mean()
    coinMonthList["EMA_5"] = coinMonthList['Close'].ewm(span=5).mean()

    # create variables based on price data to be used in this function
    # and configure the variables to the EMA
    latest = coinMonthList["EMA_5"].values[len(coinMonthList) - 1]
    price_latest = coinMonthList["Close"].values[len(coinMonthList) - 1]
    previous = coinMonthList["EMA_5"].values[len(coinMonthList) - 2]
    price_previous = coinMonthList["Close"].values[len(coinMonthList) - 2]

    # create and configure new plot
    plt.figure(figsize=(10, 7), facecolor="gray")
    plt.title('Moving Average', color="cyan")
    plt.xlabel('Date', color="cyan")
    plt.ylabel('Price', color="cyan")
    ax = plt.gca()
    ax.set_facecolor("#262629")

    # Plot close price and moving averages
    plt.plot(coinMonthList["Close"], color="red", lw=1, label='Close Price')

    # if the indicator being used is the SMA
    if indicator == "SMA":
        # plot the indicator line
        plt.plot(coinMonthList["SMA_10"], 'cyan', lw=1, label='10-day SMA')

        # set variables equal to indicator values
        latest = coinMonthList["SMA_10"].values[len(coinMonthList) - 1]
        previous = coinMonthList["SMA_10"].values[len(coinMonthList) - 2]

    # else if indicator is the EMA
    elif indicator == "EMA":
        # plot the indicator line
        plt.plot(coinMonthList["EMA_5"], 'cyan', lw=1, label='EMA_5')

    # if else statements to see if one should buy or sell their crypto
    if price_latest > latest:
        signaling = "buy soon..."
        signal_color = "green"
    elif price_latest < latest:
        signaling = "sell soon..."
        signal_color = "red"
    elif price_latest == latest:
        if price_previous > previous:
            signaling = "buy"
            signal_color = "green"
        elif price_previous < previous:
            signaling = "sell"
            signal_color = "red"

    # add a legend to the axis and plot the graph
    plt.legend(labelcolor="cyan", facecolor="#262629")
    plt.show()

    # create a label with the decision about whether to buy
    tk.Label(container, bg="Black", text=signaling,
             fg=signal_color, font=('Castellar', 50))\
        .grid(column=0, row=5, pady=2, padx=2)


# function used to create a backtesting frame
def backtesting(win1, letter_color, crypto_list):

    # create a frame for backtest
    backtest_frame = tk.Frame(win1)
    backtest_frame.configure(bg="#262629", width=900, height=650,
                             borderwidth=5, relief="raised")
    backtest_frame.grid(column=1, row=0, pady=20)
    backtest_frame.grid_propagate(False)

    # create a backtest label
    tk.Label(backtest_frame, bg=backtest_frame["bg"], fg=letter_color,
             text="Backtest", font=('Castellar', 50)).grid(column=0, row=0)

    # create a listbox to select a cryptocurrency to analyze
    listbox = tk.Listbox(backtest_frame, font=["Castellar", 20], bg="black",
                         fg="white", height=5, selectmode=tk.SINGLE)

    # initialize the listbox selections
    n = 0
    for i in crypto_list:
        listbox.insert(n, i)
        n = n + 1

    # put the listbox on the frame
    listbox.grid(column=0, row=1)

    # create and configure buttons
    btn1 = create_button(backtest_frame, "SMA")
    btn1.configure(command=lambda: datatest(
        backtest_frame, "SMA", str(listbox.get(listbox.curselection()))))
    btn2 = create_button(backtest_frame, "EMA")
    btn2.configure(command=lambda: datatest(
        backtest_frame, "EMA", str(listbox.get(listbox.curselection()))))
    btn1.grid(column=0, row=2, padx=2, pady=2, sticky="W")
    btn2.grid(column=0, row=2, padx=2, pady=2, sticky="E")

    # raise the frame above any other frames
    backtest_frame.tkraise()
