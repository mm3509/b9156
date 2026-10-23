# Pandas summary sheet — Computing for Finance, lectures 3–13

Every Pandas tool used so far in the lectures and their code, grouped by task.
"L4" means "introduced in lecture 4".

NumPy has appeared only for `np.log` (lecture 2): Pandas does all the vector arithmetic, and a square
root is written as `x ** 0.5`.

```python
import pandas as pd
import yfinance as yf
```

## 1. The two objects

| Object | What it is | Excel analogy |
|---|---|---|
| `pd.Series` | One column of values with a label per row (the **index**) | One column |
| `pd.DataFrame` | A table of Series sharing the same index; each column has a name | One sheet |

`df["Close"]` returns one column as a Series; `df` is the whole DataFrame.

## 2. Creating Series and DataFrames

| Code | Result | Lecture |
|---|---|---|
| `pd.Series([10, 20, 30])` | Series from a list; index is 0, 1, 2 | L3 |
| `pd.Series([10, 20, 30]).tolist()` | Back to a plain list (used in doc-tests) | L3 |
| `pd.Series(prices)` | Series from a dict `{date: price}`: keys become the index | L6, L10 |
| `pd.DataFrame({"Close": [45, 55]}, index=["Mon", "Tue"])` | DataFrame from a dict of columns, with row labels | L3, L11 |
| `pd.DataFrame(1 / n, index=prices.index, columns=prices.columns)` | Same shape as `prices`, every cell equal to `1 / n` | L11 |
| `pd.DataFrame(0, index=prices.index, columns=prices.columns)` | Same shape as `prices`, all zeros | L13 |
| `pd.DataFrame([weights] * len(prices), index=prices.index, columns=prices.columns)` | One row of weights repeated on every day | L13 |
| `series.to_frame(name="MSFT")` | Series → one-column DataFrame | L4 |

## 3. Getting data

| Code | What it does | Lecture |
|---|---|---|
| `pd.read_csv("file.csv")` | Read a CSV into a DataFrame | L3 |
| `pd.read_csv(path, index_col=0, parse_dates=True)` | First column becomes the index, parsed as dates | L10 |
| `yf.download(tickers, start=start, end=end)["Close"]` | Closing prices from Yahoo Finance; the index is already dates; `end` is exclusive | L4, L5 |
| `pd.to_datetime(df["Date"])` | Text → dates (a **function** of `pd`) | L4 |
| `df = df.set_index("Date")` | Make a column the index (a **method** of `df`). Reassign: it returns a new DataFrame | L4 |
| `prices.sort_index()` | Sort rows by the index, i.e. by date | L4, L5 |
| `isinstance(prices, pd.DataFrame)` | Check the type, e.g. when Yahoo returns a DataFrame instead of a Series | L5 |

The usual download helper (L5, L10):

```python
def download_prices(ticker, start, end):
    prices = yf.download(ticker, start=start, end=end)["Close"]
    if isinstance(prices, pd.DataFrame):
        prices = prices.iloc[:, 0]  # first column as a Series
    return prices.sort_index()
```

## 4. Inspecting

| Code | Result | Lecture |
|---|---|---|
| `df.head()` / `df.tail()` | First / last 5 rows | L3, L4 |
| `df.shape` | Tuple `(rows, columns)`; `df.shape[0]` is the number of rows | L4, L6 |
| `df.info()` | Column types and non-missing counts | L4 |
| `df.describe()` | Count, mean, std, min, quartiles, max per column | L4 |
| `df.index` | The row labels (often dates) | L6, L11 |
| `df.columns` | The column names (often tickers) | L11, L13 |
| `len(df)`, `len(df.columns)` | Number of rows, number of columns | L11, L13 |

## 5. Selecting and assigning

| Code | Result | Lecture |
|---|---|---|
| `df["Close"]` | One column → Series | L3 |
| `df.loc["Tue"]` | One row by label → Series | L3 |
| `df.loc["2026-05-01"]` | One row by date, once the index holds dates | L4 |
| `df.loc["Tue", "Close"]` | One cell by row label and column name → a number | L3 |
| `df.loc[df["Close"] > 50]` | Rows where the condition is True → DataFrame | L3 |
| `df.loc[df["Close"] > 50, "Close"] = 0` | **Write** into only the matching rows | L3 |
| `df.loc[(df.index >= start) & (df.index < end)] = 1` | Combine conditions with `&` (`|` for or). The parentheses are required | L12 |
| `prices[prices.index < date_threshold]` | Keep rows before a date (in-sample / out-of-sample split) | L6 |
| `pd.Timestamp("2025-01-01")` | A single date to compare against the index | L6 |
| `df.iloc[:, 0]` | First column **by position** | L5 |
| `df["New"] = ...` | Create or overwrite a column | L3 |
| `positions[ticker] = 1` | Set a whole column to one value | L13 |

`.loc` selects by **label**, `.iloc` by **position**.

## 6. Conditions and types

| Code | Result | Lecture |
|---|---|---|
| `df["Close"] < 250` | Series of True/False, one per row | L3 |
| `(short > long).astype(int)` | True/False → 1/0 | L4 |
| `(r < 0).astype(int) - (r > 0).astype(int)` | +1 / −1 / 0 signal from the sign of the return | L6 |
| `float("nan")` | A missing value, `NaN` (Not a Number) | L3 |

## 7. Missing values (NaN)

| Code | Result | Lecture |
|---|---|---|
| `s.ffill()` | Replace each NaN with the last value above it ("carry the last decision forward") | L3 |
| `s.fillna(0)` | Replace NaN with 0 | L3 |
| `s.dropna()` | Drop NaN rows. **Avoid for now**: it can misalign dates | L4 |

`.prod()`, `.sum()` and `.mean()` **ignore NaN**, so the NaN on the first day of returns is harmless (L4).

## 8. Time series

| Code | Result | Lecture |
|---|---|---|
| `s.shift(1)` | Yesterday's value on today's row: trade on yesterday's signal, no look-ahead | L3 |
| `s.shift(-1)` | Tomorrow's value on today's row (lagged correlation) | L6 |
| `prices.pct_change()` | Daily return `p_t / p_{t-1} - 1`; the first row is NaN | L3 |
| `prices.pct_change(fill_method=None)` | Same, without filling gaps (avoids a warning) | L11 |
| `prices.rolling(5).mean()` | 5-day moving average; the first 4 rows are NaN | L4 |

## 9. Aggregating

| Code | Result | Lecture |
|---|---|---|
| `s.mean()`, `s.std()`, `s.sum()` | Average, standard deviation, total | L4, L13 |
| `s.prod()` | Product of all values | L4 |
| `s.cumprod()` | Running product (growth of $1) | L3 |
| `a.corr(b)` | Correlation between two Series | L6 |
| `df.sum(axis=1)` | Sum **across** columns: one number per row (per day) | L11 |
| `s.round(4)` | Round each value (used in doc-tests) | L5 |

`axis=0` goes down the rows (one result per column); `axis=1` goes across the columns (one result per row).

## 10. Broadcasting (L11)

Arithmetic between two DataFrames lines them up by **row and column labels**, not by position:

```python
multiple_returns = positions * individual_returns  # matching day and ticker
strategy_returns = multiple_returns.sum(axis=1) / positions.sum(axis=1)
```

* Cells whose day or ticker exists in only one of them become NaN.
* Positions must have the same index and columns as the prices
  (`index=prices.index, columns=prices.columns`).
* Dividing by `positions.sum(axis=1)` turns positions into weights that add up to 1.

## 11. Looping

| Code | Use | Lecture |
|---|---|---|
| `for ticker, prices in prices_by_ticker.items():` | Loop over a dict of Series | L6 |
| `for ticker in prices.columns:` | Loop over the columns of a DataFrame | L13 |

## 12. Finance recipes

| Quantity | Code | Lecture |
|---|---|---|
| Daily returns | `returns = prices.pct_change()` | L3 |
| Position, no look-ahead | `position = signal.shift(1)` | L3 |
| Strategy returns | `position * market_returns` | L3 |
| Value of $1 over time | `(1 + returns).cumprod()` | L3 |
| Total return | `(1 + returns).prod() - 1` | L4 |
| Annual return | `(1 + total_return) ** (252 / len(returns)) - 1` | L6, L11 |
| Annual st-dev | `returns.std() * 252 ** 0.5` | L13 |
| Moving-average crossover | `(prices.rolling(5).mean() > prices.rolling(20).mean()).astype(int).shift(1)` | L4 |
| Threshold strategy with memory | `df.loc[buy, "Action"] = 1`, `df.loc[sell, "Action"] = 0`, then `df["Action"].ffill().fillna(0)` | L3 |

## 13. Common mistakes

* `df.set_index("Date")` without `df = ...` does nothing to `df`.
* Forgetting `.shift(1)`: trading on today's close with today's signal is look-ahead bias.
* `.dropna()` in the wrong place shifts rows against each other.
* `a > 1 & b < 2` fails: write `(a > 1) & (b < 2)`, and never `and` / `or` on Series.
* Two DataFrames with different labels multiply into NaN (broadcasting aligns labels).
