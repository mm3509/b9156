import pandas as pd
import yfinance as yf


def helper_download_prices_yahoo(ticker, start, end):
    prices = yf.download(ticker, start=start, end=end, progress=False)["Close"]
    if isinstance(prices, pd.DataFrame):
        prices = prices[ticker]
    return prices.sort_index()


class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy

    def load_prices_from_yahoo(self, ticker, start, end):
        self.prices = helper_download_prices_yahoo(ticker, start, end)

    def load_prices_from_file(self, file_path):
        self.prices = pd.read_csv(file_path, index_col=0, parse_dates=True)

    def load_prices_from_series(self, prices):
        if isinstance(prices, pd.Series):
            self.prices = prices
        else:
            self.prices = pd.Series(prices)
        self.prices = self.prices.sort_index()

    def get_returns(self):
        return self.prices.pct_change()

    def strategy_returns(self, positions):
        return positions * self.get_returns()

    def total_return(self, returns):
        return float((1 + returns).prod() - 1)

    def run(self):
        positions = self.strategy.generate_positions(self.prices)
        portfolio_returns = self.strategy_returns(positions)
        return self.total_return(portfolio_returns)