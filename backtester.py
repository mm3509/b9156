import pandas as pd


import utils
from utils import DAYS_IN_YEAR


def average_annual_return(returns):
    total_return = (1 + returns).prod() - 1
    return utils.convert_interest_rate(total_return, len(returns.index), DAYS_IN_YEAR)


def daily_returns(prices):
    # Passing fill_method=None fills the first day with NaN and avoids a warning.
    return prices.pct_change(fill_method=None)


class Backtester:

    def set_benchmark(self, ticker):
        self.benchmark_ticker = ticker

    def set_strategy(self, strategy):
        self.strategy = strategy

    def load_prices_from_yahoo(self, tickers, start, end):
        self.start = start
        self.end = end
        self.prices = utils.helper_download_prices_yahoo(tickers, start, end)

    def load_prices_from_file(self, file_path):
        self.prices = pd.read_csv(file_path, index_col=0, parse_dates=True)

    def load_prices_from_series(self, prices):
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices)
        prices = prices.sort_index()
        prices_df = pd.DataFrame(prices, columns=["Close"])
        self.prices = prices_df

    def compute_strategy_returns(self):
        individual_returns = daily_returns(self.prices)
        positions = self.strategy.generate_positions(self.prices)
        multiple_returns = positions * individual_returns  # Broadcasting
        strategy_returns = multiple_returns.sum(axis=1) / positions.sum(axis=1)
        self.strategy_annual_return = average_annual_return(strategy_returns)

    def compute_benchmark_returns(self):
        benchmark_df = utils.helper_download_prices_yahoo(self.benchmark_ticker, self.start, self.end)
        benchmark_series = benchmark_df[self.benchmark_ticker]
        returns = daily_returns(benchmark_series)
        self.benchmark_annual_return = average_annual_return(returns)

    def run(self):
        self.compute_benchmark_returns()
        self.compute_strategy_returns()

    def print_results(self):
        print(f"Strategy annual return: {self.strategy_annual_return:.1%}")

        print(f"Benchmark ({self.benchmark_ticker})"
              f" annual return: {self.benchmark_annual_return:.1%}")
