import tkinter as tk
from tkinter.messagebox import askretrycancel
from urllib.request import urlopen as ureq
from urllib.parse import urljoin as urjo
from bs4 import BeautifulSoup as soup
import webbrowser
from interactions import CoinbaseTransactions


# This function is used to check the connection to the internet by
# loading a URL and checking if it can be reached
def connect():
    host = 'http://google.com'
    try:
        ureq(host)
        return True  # Python 3.x
    except:
        return False


# this function creates the home_screen frame
def home(win1, letter_color):

    # create the home frame, and initialize it
    home_screen = tk.Frame(win1, bg="#262629", width=900, height=650,
                           borderwidth=5, relief="raised")
    home_screen.grid(column=1, row=0, pady=20)
    home_screen.grid_propagate(False)

    # call an instance of Coinbase Transactions
    tr_object = CoinbaseTransactions()

    # create labels for each header in the frame
    tk.Label(home_screen, bg=home_screen["bg"], fg=letter_color, text="Home",
             anchor='w', font=('Castellar', 50)).grid(column=0, row=1)
    tk.Label(home_screen, bg=home_screen["bg"], fg=letter_color, text="News: ",
             anchor='w', font=('Castellar', 20)).grid(column=0, row=2)
    tk.Label(home_screen, bg=home_screen["bg"], fg=letter_color,
             text="Transactions: ", anchor='w', font=('Castellar', 20))\
        .grid(column=0, row=6)

    # if we can connect to the internet
    if connect():
        # get articles from coindesk, crypto news, and coin_market_cap
        coindesk = news_articles("https://www.coindesk.com/markets/", "h3",
                                 "class",
                                 "typography__StyledTypography-owin6q-0 diBymZ",
                                 "a", home_screen)
        crypto_news = news_articles("https://cryptonews.net/news/top/",
                                    "div", "class", "row news-item start-xs",
                                    "div", home_screen)
        coin_market = news_articles("https://coinmarketcap.com/headlines/news/",
                                    "div", "class", "sc-aef7b723-0 coCmGz",
                                    "a", home_screen)

        # display each of the articles
        coindesk.grid(column=1, row=3)
        crypto_news.grid(column=1, row=4)
        coin_market.grid(column=1, row=5)
        for widget in home_screen.winfo_children():
            widget.grid(columnspan=4, padx=5, pady=5, sticky="we")

        # get a List of transactions from the function, then display it
        trList = tr_object.list_of_transactions(home_screen, ["USD"], False, 5)
        trList.grid(columnspan=5, column=0, row=7, padx=2)

        # return the home_screen
        return home_screen

    # if no internet connection
    else:
        # display a message to the user to restart their internet connection
        txt = "Check your internet connection and click " \
              "retry when your connection is reset"
        answer = askretrycancel(title="No-Connection",
                                message=txt)

        # when the user presses retry
        if answer:
            home(win1, letter_color)


# this function is used to get the top story from news websites
def news_articles(url, header, class_type, specific, find_title, home_screen,):

    # initialize variables needed for later
    client = ureq(url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html5lib")
    articles = page_soup.find(header, {class_type: specific})
    txt = None

    # find the title and url
    new_url = urjo(url, articles.a['href'])
    if find_title == "div":
        txt = articles.div.text
    elif find_title == "a":
        txt = articles.a.text
    if len(txt) > 50:
        txt = txt.split()[:10]
        txt.append("...")

    # create a button with the article title, and have it call the url
    btn = tk.Button(home_screen, text=txt, bg="lightgray", font=('Times', 15),
                    command=lambda: webbrowser.open(new_url, autoraise=True))

    # return the btn
    return btn
