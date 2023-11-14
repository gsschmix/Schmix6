from coinbase.wallet.client import Client
import cbpro
import pandas as pd
import tkinter as tk
from interactions import CoinbaseTransactions, prices, asset_usd_amount, \
    find_all_crypto
import time
import matplotlib.pyplot as plt
from Historic_Crypto import HistoricalData
import http.client
import matplotlib.dates as mdate
from cbpro import PublicClient
from datetime import datetime
import dateutil.relativedelta
from pytz import timezone
today_date = datetime.now(timezone('UTC')).date()


month_time = (today_date + dateutil.relativedelta.
                  relativedelta(months=-1)).strftime("%Y-%m-%d")

crypto = find_all_crypto()

x = CoinbaseTransactions()
crypto_account = x.client.get_account("USD")
account = pd.DataFrame(crypto_account)
account_id = account["id"].values[0]
transactions = pd.DataFrame(x.client.get_transactions(account_id)['data'])
# create a sorted list of transactions based on when they were created
sorted_list = transactions.sort_values(by="created_at", ascending=False)


combinded_list = asset_usd_amount(crypto[0], month_time, 86400, today_date)
# get all of the crypto amounts in USD
for i in crypto[1:]:
    try:
        old_crypto = combinded_list
        new_list = asset_usd_amount(i, month_time, 86400, today_date)
        combinded_list = new_list.astype(float) + old_crypto.astype(float)
        print(combinded_list)
    except:
        continue




