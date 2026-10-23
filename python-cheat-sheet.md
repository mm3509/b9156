# Python cheat sheet — Computing for Finance

The everyday Python syntax used in this course. "L7" means "introduced in
lecture 7"; entries without a lecture are standard Python worth knowing.
For Pandas, see `pandas-cheat-sheet.md`.

## 1. Variables, numbers, and arithmetic

```python
price = 101.5            # float
shares = 10              # int
ticker = "MSFT"          # str
is_long = True           # bool: True / False
missing = None           # "no value yet"
nan = float("nan")       # "not a number", used for missing data (L3)
```

* Dynamic typing: a variable's type comes from its current value (L2).
  `a = 24` is an int, then `a = "24"` makes it a str, then `a = 3 * 8.0` a float.
* Casting converts between types (L2): `int("24")` → `24`, `str(24)` → `"24"`, `bool(0.24)` → `True`.
  Python casts implicitly only between numbers: `24 + 0.24` → `24.24`, but `"24" + 24` is a `TypeError`.

| Operator | Meaning | Example → result |
|---|---|---|
| `+ - * /` | Arithmetic; `/` always gives a float | `7 / 2` → `3.5` |
| `//` | Integer division | `7 // 2` → `3` |
| `%` | Remainder (modulo) | `2024 % 4` → `0` |
| `**` | Power, **not** `^`; `** 0.5` is a square root (L2) | `2 ** 10` → `1024` |
| `+=`, `-=`, `*=` | Update in place | `total += x` |
| `round(x, 2)` | Round to 2 decimals | `round(3.14159, 2)` → `3.14` |
| `abs(x)` | Absolute value | `abs(-0.02)` → `0.02` |
| `int()`, `float()`, `str()` | Convert type | `float("1.5")` → `1.5` |
| `type(x)` | The type of a value | `type(1.5)` → `float` |

## 2. Comparisons and logic

| Code | Meaning |
|---|---|
| `== != < <= > >=` | Compare, giving `True` or `False` |
| `and`, `or`, `not` | Combine plain booleans (for Pandas Series, use `&`, `\|`, `~`) |
| `x in items`, `x not in items` | Membership in a list, dict (keys), or string |
| `x is None` | Check for `None` (use `is`, not `==`) |
| `isinstance(x, float)` | Check the type (L5) |
| `if x:` | Truthiness (L2): `0`, `0.0`, `""`, `[]`, `{}`, `()` and `None` count as False; everything else as True |

## 3. Strings and printing

```python
ticker = "MSFT"
ret = 0.0734
value = 1234567.891
print(f"{ticker} returned {ret:.1%}")   # MSFT returned 7.3%
print(f"{ret:.4f}")                     # 0.0734
print(f"${value:,.0f}")                # $1,234,568
print(f"{ret = }")                      # ret = 0.0734 (quick debugging)
print("a", "b", sep="\n")               # one item per line (L11)
tickers = "AAPL, MSFT, NVDA".split(", ")  # ['AAPL', 'MSFT', 'NVDA'] (L6)
print(", ".join(tickers))               # AAPL, MSFT, NVDA
print(ticker.lower(), " MSFT ".strip(), len(ticker))
```

| Format | Example → result |
|---|---|
| `:.1%` | `0.0734` → `7.3%` |
| `:.2f` | `3.14159` → `3.14` |
| `:,.0f` | `1234567.8` → `1,234,568` |
| `:>10` | Right-align in 10 characters |

## 4. Lists

```python
prices = [100, 102, 99, 105]
prices[0]             # 100: first item (indices start at 0)
prices[-1]            # 105: last item (L13)
prices[1:3]           # [102, 99]: items 1 and 2 (end excluded)
prices[:-1]           # all but the last (L13)
len(prices)           # 4
prices.append(110)    # add at the end (L8)
first = prices.pop(0) # remove and return the first item (L8)
sum(prices), max(prices), min(prices)
sorted(prices)                # new sorted list
sorted(prices, reverse=True)  # largest first
[0.3, 0.7] * 3        # [0.3, 0.7, 0.3, 0.7, 0.3, 0.7] (L13)
[[0.3, 0.7]] * 3      # [[0.3, 0.7], [0.3, 0.7], [0.3, 0.7]] (L13)
```

## 5. Tuples and unpacking

```python
pair = ("AAPL", "MSFT")          # like a list, but cannot be changed
leader, follower = pair          # unpacking (L6)
best, corr = None, 2.0           # several assignments on one line (L6)

def market_and_strategy():
    return 0.15, 0.12            # return several values as a tuple (L5)

market, strategy = market_and_strategy()
```

## 6. Dictionaries

```python
prices = {"AAPL": 190.0, "MSFT": 410.0}
prices["MSFT"]                  # 410.0
prices["NVDA"] = 120.0          # add or overwrite
"AAPL" in prices                # True: checks the keys
prices.get("TSLA", 0.0)         # 0.0: default if the key is missing
for ticker, price in prices.items():   # keys and values together (L6)
    print(ticker, price)
for ticker in prices:                  # keys only
    print(ticker)
cache = {}
cache[7] = True                 # dicts as memory for memoization (L7)
```

## 7. Conditionals (L2)

```python
ret = -0.01
if ret > 0:
    action = "buy"
elif ret < 0:
    action = "sell"
else:
    action = "hold"

action = "buy" if ret > 0 else "sell"   # one-line version
```

Use `elif` for alternatives: with two separate `if`s, the `else` attaches only to the second one, so it also runs after the first `if` matched (L2).

## 8. Loops

```python
prices = [100, 102, 99, 105]

for price in prices:               # over items
    print(price)

for i in range(len(prices)):       # over positions: 0, 1, 2, 3 (L7)
    print(i, prices[i])

for i in range(1, len(prices)):    # start at 1 to compare with the previous day
    daily_return = prices[i] / prices[i - 1] - 1

for i, price in enumerate(prices): # position and item together
    print(i, price)

for a, b in zip(prices[:-1], prices[1:]):   # walk two lists side by side
    print(b / a - 1)

for _ in range(3):                 # _ when the loop variable is not needed (L13)
    print("simulate")

n = 0
while n < 3:                       # repeat while a condition holds (L7)
    n += 1

for price in prices:
    if price < 100:
        continue                   # skip to the next item (L6)
    if price > 104:
        break                      # leave the loop (L7)
```

## 9. Comprehensions

```python
prices = [100, 102, 99, 105]
returns = [prices[i] / prices[i - 1] - 1 for i in range(1, len(prices))]  # list (L9)
ups = [r for r in returns if r > 0]                                        # with a filter
squares = {t: len(t) for t in ["AAPL", "MSFT"]}                            # dict (L6)
```

## 10. Functions

```python
def annualized_return(total_return, num_days, trading_days_per_year=252):
    """Converts a total return over num_days into a yearly rate."""
    return (1 + total_return) ** (trading_days_per_year / num_days) - 1

annualized_return(0.10, 504)                             # positional arguments
annualized_return(0.10, 504, trading_days_per_year=365)  # keyword argument
```

* Use `return` to give back a result; `print()` only displays it, and the function then returns `None` (L2).
* Functions are values: `fn = square` then `fn(4)` → `16` (L2).
* Default values (`=252`) make an argument optional.
* Keep functions short and give them one job; test each with doc-tests.

## 11. Scope: local, global, nonlocal (L7, L8)

```python
x = 10
def show_x():
    x = 20        # a NEW local variable; the global x is unchanged
    print(x)

def make_counter():
    count = 0
    def increment():
        nonlocal count   # needed to CHANGE a variable of the enclosing function
        count += 1
        return count
    return increment
```

* Reading an outer variable works without any keyword.
* Assigning to it creates a local variable, unless you declare it `nonlocal` (or `global`).
* Changing a mutable object (`values.append(x)`, `state["total"] += 1`) needs no keyword.

## 12. Closures, function factories, memoization (L7, L8)

```python
def make_tipper(rate):          # function factory: returns a function
    def tip(amount):            # closure: remembers rate
        return round(amount * rate, 2)
    return tip

medium_tip = make_tipper(0.15)
medium_tip(21.25)               # 3.19

def memoize(f):
    cache = {}
    def wrapper(x):
        if x not in cache:
            cache[x] = f(x)     # compute once
        return cache[x]         # afterwards, read from memory
    return wrapper
```

Writing `@memoize` above `def f(...)` is shorthand for `f = memoize(f)` (a decorator).

## 13. Classes and objects (L9, L10, L13)

```python
class Account:
    def __init__(self, balance=0):   # runs when the object is created
        self.balance = balance       # an attribute, stored on the object

    def deposit(self, amount):       # a method: a function attached to the object
        self.balance += amount

    def set_balance(self, balance):  # setter style used in the backtester
        self.balance = balance

account = Account(100)       # create an object (an instance of the class)
account.deposit(50)          # Python passes account as self
account.balance              # 150
```

* `self` is the object the method was called on.
* Classes group data (attributes) and the functions that use them (methods).
* A strategy is any object with a `generate_positions(prices)` method (L10, L11).

## 14. Modules and imports

```python
import math                      # whole module (L2)
math.log(math.e)                 # 1.0: natural logarithm (L2)
import numpy as np               # with a short alias (L2)
np.log(np.e)                     # 1.0
import random                    # random.random()
import pandas as pd
from utils import DAYS_IN_YEAR   # one name from your own file utils.py (L10)

random.random()                  # float in [0, 1) (L13)
random.randrange(2)              # 0 or 1 (L13)
weights = [0.2, 0.3, 0.5]
random.shuffle(weights)          # shuffles the list in place (L13)
```

## 15. Doc-tests and running a file (L2)

```python
import math


def years_to_double(interest_rate):
    """
    >>> years_to_double(0.05)
    14.206...
    >>> years_to_double(0.1)
    7.272...
    """
    return math.log(2) / math.log(1 + interest_rate)


if '__main__' == __name__:
    import doctest
    tests_failed, tests_run = doctest.testmod(optionflags=doctest.ELLIPSIS)
    if 0 == tests_run:
        print('Unable to run doc-tests, please see Miguel!')
    else:
        assert 0 == tests_failed, 'Some doc-tests failed, exiting...'
        print('Your doc-tests pass, congratulations!')
```

* A **doc-string** is the triple-quoted string right after `def`; a **doc-test** is a line in it starting with `>>>`, and the next line is the documented result.
* Python compares the documented and actual results **as text**: strings must be shown with single quotes, e.g. `'abcdabcd'`, not `"abcdabcd"`.
* `...` (ellipsis) ignores everything after it, which absorbs rounding error across computers.
* `assert condition, "message"` continues if the condition is truthy, and otherwise stops with an `AssertionError` and the message.
* `__name__` ("dunder name") equals `"__main__"` when you run the file, and the module's name when another file (e.g. Autograder) imports it; so the block above runs only on your computer.
* From a terminal: `python -m doctest -o=ELLIPSIS file.py`.

## 16. Errors

```python
try:
    value = float("abc")
except ValueError:
    value = None
```

| Error | Usual cause |
|---|---|
| `SyntaxError` | Typo, missing `:` or bracket |
| `IndentationError` | Inconsistent indentation: use 4 spaces |
| `NameError` | Variable not defined or misspelled, or a function from a module not imported, e.g. `log(10)` (L2) |
| `TypeError` | Wrong type, e.g. `"5" + 1` |
| `IndexError` | List index past the end |
| `KeyError` | Missing dictionary key (or DataFrame column) |
| `AttributeError` | Method or attribute that the object does not have |
| `UnboundLocalError` | Assigning to an outer variable without `nonlocal` (L8) |
| `AssertionError` | An `assert` failed, e.g. a doc-test (L2) |

## 17. Common mistakes

* `=` assigns, `==` compares.
* `^` is not a power: use `**`.
* `print()` instead of `return` in a graded function.
* Changing a function's name or its doc-tests: Autograder relies on both.
* Indices start at 0, and slices exclude the end: `prices[1:3]` has 2 items.
* `range(5)` is 0 to 4.
* Forgetting `return`: the function returns `None`.
* Forgetting `self` in a method definition, or `self.` before an attribute.
* Changing a list while looping over it.
* Floats are approximate: `0.1 + 0.2 == 0.3` is False; compare with `round()` or use `...` in doc-tests.
