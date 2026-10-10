import yfinance as yf
import pandas as pd


DAYS_IN_YEAR = 252


def convert_interest_rate(r1, days1, days2):
    """ From assignment 1.
    >>> convert_interest_rate(0.05, 360, 1)
    0.000135...
    >>> convert_interest_rate(0.05, 360, 30)
    0.004074...
    >>> convert_interest_rate(0.05, 360, 180)
    0.024695...
    """

    if days1 == days2:
        return r1

    return (1 + r1) ** (days2 / days1) - 1


def helper_download_prices_yahoo(tickers, start, end):
    if isinstance(tickers, str):
        tickers = [tickers]
    print(f"Downloading data from Yahoo Finance for {len(tickers)} ticker(s)")
    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=True,
        auto_adjust=True,
        threads=True,
    )
    prices = data["Close"]
    if len(tickers) == 1 and isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])
    return prices.sort_index()
