PROGRAMMER: Gideon Schmickle

VERSION: 1.0.0

-------------------------------------------------------------------------------

SCHMIX6

PURPOSE: To act as an interface between Coinbase and trading strategies.

FILES:

    - main.py: This file is used to create an initial welcome and login screen.
        After one has successfully logged in, they are taken to frames.py

    - frames.py: This file is used to create a new window that holds the
        buttons to be used by the program to access the other frames. Each
        respective button connects to the respective frame, including
        start_up.py (Schmix6), cryptocurrencies.py (Cryptocurrencies),
        assets.py (My Assets), backtest.py (Backtest), documentation.py
        (Documentation), and the website of Coinbase (Coinbase).

    - start_up.py: This file creates a new frame containing articles to three
        different news sources and the most recent transactions (which are
        gotten from interactions.py).

    - cryptocurrencies.py: This file creates a new frame containing a a list of
        all the cryptocurrencies that one owns. A selection of a button will
        create a new window showing the selected cryptocurrency. This window
        contains a graph of the price of the cryptocurrency, recent
        transactions with the cryptocurrency, percent increase or decrease of
        the cryptocurrency, and a button allowing for access to more
        transactions. Additionally, there is a combobox for selecting a
        timeframe from which to view the cryptocurrency and its
        increase/decrease. Information is processed through interactions.py.

    - assets.py: This file creates a new frame with a graph with all of the
        owned crypto in terms of USD, labels for daily, weekly, and monthly
        highs; a list of any cryptocurrency that has been traded at any point
        previously, and total amounts of USD and crypto in terms of USD
        currently possessed. The list of cryptocurrencies is selectable, and
        creates a new window when selected. The new window displays a graph of
        possessed cryptocurrency over a month in terms of USD, labels for daily,
        weekly, and monthly highs; a list of three recent transactions, and a
        button to view more than three transactions

    - backtest.py: This file creates a new frame to backtest historical data.
        By utilizing the 10-day Simple Moving Average (SMA) and the 5-day
        Exponential Moving Average (EMA), the program takes historical data
        from the past day to calculate a model based on these indicators.
        There is a list to choose a cryptocurrency, and get an indicator for
        the crypto should be sold, sold soon, bought soon, or bought.
        Additionally, a graph displaying the indicator will be shown in a
        pop-up window.

    - documentation.py: This file creates a frame to hold the documentation
        about the program.

    - interactions.py: This file holds functions for getting price data, account
        data, transaction data, and a client object.

    - creation.py: This file holds functions that act as a baseplate for
        windows and buttons.

CONTINUING:

    Crypto Trading Bot: In the following months, I will be developing an
        algorithm that will trade cryptocurrencies. I will be including the
        current backtesting strategies.

    Faster processing: Additionally, I will be searching for ways to make data
        processing go faster in this program. Possibilities include: cleaner
        code and multithreading.
