from tkinter import Frame, LabelFrame, Label
import os
from coinbase.wallet.client import Client
import pandas as pd
import matplotlib
from cbpro import PublicClient
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')


# find all crypto wallets that the user has
def find_all_crypto():
    # get data and clean it
    client = CoinbaseTransactions().client
    wallet_df = pd.DataFrame(client.get_accounts()['data'])
    clean = wallet_df[wallet_df['created_at'].str.contains("None") == False]
    delete_this = clean[clean['created_at'] == clean["updated_at"]]
    even_cleaner = clean.drop(delete_this.index)
    cleanest = even_cleaner.drop(17)

    # find all the unique names
    crypto_list = cleanest.currency.unique()

    # return a list of crypto
    return crypto_list


# this class is used to get Coinbase Transactions
class CoinbaseTransactions:

    # initialize variables to be used in the class
    def __init__(self):
        self.api_key = os.getenv('CB_KEY_READ')
        self.api_secret = os.getenv('CB_SECRET_READ')
        self.client = Client(self.api_key, self.api_secret)
        self.transaction_df = pd.DataFrame(columns=["Crypto", "Amount", "S/B",
                                                    "Native Amount", "Native",
                                                    "Created", "Updated",
                                                    "Fill", "Status"])
        self.order_id = []

    # this function finds the transactions of a given crypto account.
    def transactions(self, crypto, iterable, num_of_iterations):

        # find the account id of a crypto account
        crypto_account = self.client.get_account(crypto)
        account = pd.DataFrame(crypto_account)
        account_id = account["id"].values[0]

        # load all transactions into the program
        transactions = pd.DataFrame(self.client.get_transactions(account_id)
                                    ['data'])

        # check to see if the number of transactions is less than
        # the desired number of iterations
        if len(transactions) < num_of_iterations:
            num_of_iterations = len(transactions)

        # check how many iterations there are
        if iterable:
            num_of_iterations = len(transactions)

        # get all the individual transactions for a crypto account
        for r in range(0, num_of_iterations):
            # get each individual transaction id and get the transaction
            # associated with it
            transaction_id = transactions['id'].values[r]
            transaction_temp = pd.DataFrame(self.client.get_transaction
                                            (account_id, transaction_id))

            # get values for each column in self.transaction_df
            created = (str(transaction_temp['created_at']
                           .values[0]).split("T"))[0]
            updated = (str(transaction_temp['updated_at']
                           .values[0]).split("T"))[0]
            amount = str(transaction_temp['amount']
                         .values[0]).replace('-', '')
            sellingAmount = str(transaction_temp['native_amount']
                                .values[0]).replace('-', '')
            native = transaction_temp['native_amount'].values[1]
            status = transaction_temp['status'].values[0]

            # if the transaction type is advanced trade fill, get these values
            if transaction_temp['type'].values[0] == 'advanced_trade_fill':
                bOS = transaction_temp['advanced_trade_fill'].values[6]
                fill = transaction_temp['advanced_trade_fill'].values[2]
                cryptoName = (str(transaction_temp['advanced_trade_fill']
                                  .values[3]).split("-"))[0]

                # if the account is USD, get the amount of crypto by dividing
                # the native amount from the fill amount
                if transaction_temp['amount'].values[1] == "USD":
                    price = str(round(
                        float(transaction_temp['native_amount'].values[0])
                        / float(fill), 6))
                    amount = price.replace('-', '')

            # else, get these values
            else:
                bOS = transaction_temp['type'].values[0]
                fill = transaction_temp['details'].values[5]
                cryptoName = (transaction_temp['amount'].values[1])

            # configure the transaction list and append it to
            # the transaction dataframe
            transaction = [cryptoName, amount, bOS, sellingAmount,
                           native, created, updated, fill, status]
            self.transaction_df.loc[len(self.transaction_df)] = transaction

    # this function is used to get a list of transactions
    def list_of_transactions(self, frame, crypto, iterable, num_of_iterations):
        # trList acts as the frame to hold the information
        trList = LabelFrame(frame, text='Most Recent', bg="black",
                            fg="blue", relief="raised", borderwidth=5)

        # for the crypto list passed to this function,
        # get each crypto account's transactions
        for i in crypto:
            self.transactions(i, iterable, num_of_iterations)

        # sort the transactions by when the were updated and created
        sorted_transactions = self.transaction_df\
            .sort_values(by=['Updated', "Created"], ascending=False)

        # create the frame to hold the column names
        trFrame = Frame(trList, bg="white", relief="raised", borderwidth=1)
        trFrame.grid(column=0, row=0, pady=2)

        # initialize column value to 0
        cn = 0
        for i in sorted_transactions.columns:
            Label(trFrame, text=i, anchor="center", font=('Times', 11),
                  bg="#262629", fg="white", width=11).grid(column=cn, row=0)
            cn = cn + 1

        # check if the list is iterable. If it is,
        # list all available transactions
        if iterable or len(self.transaction_df) < num_of_iterations:
            num_of_iterations = len(self.transaction_df)

        # create frames for each row in the transaction table
        for j in range(0, num_of_iterations):

            trFrame = Frame(trList, bg="white", relief="groove", borderwidth=1)
            trFrame.grid(column=0, row=j+1, pady=2)

            # initialize column value to 0
            cn = 0

            # get the values associated with each transaction
            for i in sorted_transactions.columns:
                # get the text associated with the list value
                s = sorted_transactions[i].values[j]

                # create label for the information
                Label(trFrame, text=s, anchor="center", font=('Times', 11),
                      bg="#262629", fg="white", width=11).grid(column=cn, row=0)

                # increment column counter
                cn = cn + 1

        return trList


# this function is used to get historic crypto prices
def prices(crypto, time, sec, today_date, all=False):
    # add to get the crypto-USD pair
    crypto += "-USD"

    # create a new public client
    c = PublicClient()
    # get the historical data from cbpro
    historical = pd.DataFrame(c.get_product_historic_rates(product_id=crypto,
                                                           granularity=sec,
                                                           start=time,
                                                           end=today_date))
    historical.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    historical['Date'] = pd.to_datetime(historical['Date'], unit='s')
    historical.set_index('Date', inplace=True)
    historical.sort_values(by='Date', ascending=True, inplace=True)

    # if the user wants all values in the dataframe
    if all:
        return historical

    # if the user only wants the column ["open"]
    else:
        return historical["Open"]


# this function creates a graph from a dataframe
def price_graph(win1, crypto_list):
    # create a new figure
    figure = Figure(figsize=(10, 3.5), dpi=120, facecolor="#262629")

    # create a new subplot and initialize it
    ax = figure.add_subplot()
    ax.tick_params(axis='x', colors='aqua', which="both")
    ax.tick_params(axis='y', colors='aqua')

    # add the dataframe values to the subplot
    crypto_list.plot(ax=ax)

    # create a canvas to interact with tkinter
    figure_canvas = FigureCanvasTkAgg(figure, win1)

    # return the canvas
    return figure_canvas


# check the amount of assets being used
def asset_usd_amount(crypto, time, sec, today_date):
    # create client
    client = CoinbaseTransactions().client

    # get the transaction ids.
    crypto_account = client.get_account(crypto)
    account = pd.DataFrame(crypto_account)
    account_id = account["id"].values[0]
    transactions = pd.DataFrame(client.get_transactions(account_id)['data'])

    # check if transactions exist for this account
    if "created_at" not in transactions.columns:
        return None

    # create a sorted list of transactions based on when they were created
    sorted_list = transactions.sort_values(by="created_at", ascending=False)

    # initialize variables/arrays to be used later on
    crypto_amount = [account["balance"].values[0]]
    updated_times = []

    # this for loop is used to find the historical amounts of the crypto
    # based on transactions that happened
    for i in range(0, len(sorted_list)):
        # create variables for the for loop
        him = sorted_list["amount"].values[i]
        hit = sorted_list["advanced_trade_fill"].values[i]

        # if the type is advanced_trade_fill, and the order is a sell
        # this adds the commission that was taken away from the trade
        if sorted_list["type"].values[i] == "advanced_trade_fill" \
                and hit["order_side"] == "sell":

            # add the new amount to the existing array
            crypto_amount.append(float(crypto_amount[i]) - float(him['amount'])
                                 + float(hit["commission"]))

        else:
            # append amount without commission
            crypto_amount.append(float(crypto_amount[i]) - float(him['amount']))

        # get the date of transaction in terms of date and time
        string_date = (str(sorted_list["created_at"].values[i])
                       .replace("Z", "").split("T"))
        string_date = string_date[0] + " " + string_date[1]

        # add the new date to updated_times
        updated_times.append(string_date)

    # add the last date to the updated_times
    string_date = (str(account["created_at"].values[0])
                   .replace("Z", "").split("T"))
    string_date = string_date[0] + " " + string_date[1]
    updated_times.append(string_date)

    # create a dataframe based on the updated_times and the crypto_amount
    crypto_df = pd.DataFrame({"Date": updated_times, "Amount": crypto_amount})

    # make the date the index
    crypto_df["Date"] = pd.to_datetime(crypto_df["Date"])
    crypto_df.set_index('Date', inplace=True)

    # organize the crypto_df by index (ascending = True)
    organized_list = crypto_df[crypto_df.index > time]["Amount"]

    # get the price range in USD fo the given times
    price_range = (prices(crypto, time, sec, today_date))\
        .sort_index(ascending=False)

    # create a new dataframe that will hold the price ranges of the
    # crypto
    price_ranges = price_range.multiply(float(crypto_df.values[0]))
    # if the organized list has items
    if len(organized_list) > 0:
        # multiply the price range by the crypto in the initial time_frame
        price_ranges = price_range\
            .multiply(float(crypto_df.values[len(organized_list)]))

        # multiply the price range by the crypto across all time_frames
        for i in range(1, len(organized_list)):
            old_price = price_ranges
            price_ranges = price_range[price_range.index >
                                       organized_list.index[1]] \
                .multiply(float(organized_list.values[len(organized_list)-i-1]))
            price_ranges = price_ranges.combine_first(old_price)

    # return the new dataframe
    return price_ranges


# function used to get the balance of an account
def get_balance(crypto):
    x = CoinbaseTransactions()
    crypto_account = x.client.get_account(crypto)
    account = pd.DataFrame(crypto_account)
    balance_of_account = account["balance"].values[0]

    return balance_of_account

