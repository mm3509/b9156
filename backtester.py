import pandas as pd


import utils
from utils import DAYS_IN_YEAR


def average_annual_return(returns):
    total_return = (1 + returns).prod() - 1
    return utils.convert_interest_rate(total_return, len(returns.index), DAYS_IN_YEAR)


def daily_returns(prices):
    # Passing fill_method=None fills the first day with NaN and avoids a warning.
    return prices.pct_change(fill_method=None)


class BacktestMetrics:
    def set_returns(self, returns):
        self.returns = returns
        self.compute_st_dev()
        self.compute_annual_return()

    def compute_st_dev(self):
        daily_st_dev = self.returns.std()
        self.annual_st_dev = daily_st_dev * (DAYS_IN_YEAR ** 0.5)

    def compute_annual_return(self):
        total_return = (1 + self.returns).prod() - 1
        self.annual_return = utils.convert_interest_rate(total_return,
                                                         len(self.returns.index),
                                                         DAYS_IN_YEAR)
    def print_metrics(self):
        print(f"Annual return: {self.annual_return:.1%}")
        print(f"Annual st-dev: {self.annual_st_dev:.1%}")


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
        self.strategy_metrics = BacktestMetrics()
        self.strategy_metrics.set_returns(strategy_returns)

    def compute_benchmark_returns(self):
        benchmark_df = utils.helper_download_prices_yahoo(self.benchmark_ticker, self.start, self.end)
        benchmark_series = benchmark_df[self.benchmark_ticker]
        returns = daily_returns(benchmark_series)
        self.benchmark_metrics = BacktestMetrics()
        self.benchmark_metrics.set_returns(returns)

    def run(self, run_benchmark=True):
        self.run_benchmark = run_benchmark
        if self.run_benchmark:
            self.compute_benchmark_returns()
        self.compute_strategy_returns()

    def print_results(self):
        print(f"Strategy results")
        self.strategy_metrics.print_metrics()

        if not self.run_benchmark:
            return
        print(f"Benchmark results ({self.benchmark_ticker})")
        self.benchmark_strategy.print_metrics()
