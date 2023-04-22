import sqlite3
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot


def print_candles(dfs):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    fig = fig.add_trace(
        go.Candlestick(
            x=dfs[0].index,
            open=dfs[0].open,
            high=dfs[0].high,
            low=dfs[0].low,
            close=dfs[0].close,
        ),
        row=1,
        col=1,
    )

    fig = fig.add_trace(
        go.Candlestick(
            x=dfs[1].index,
            open=dfs[1].open,
            high=dfs[1].high,
            low=dfs[1].low,
            close=dfs[1].close,
        ),
        row=2,
        col=1,
    )

    fig.update_xaxes(rangeslider_visible=False)
    # fig.show()

    plot(fig, auto_open=True)


def agregate_by_time(df, time):
    df = df.resample(time).agg(["max", "min", "first", "last"])
    df.columns = ["high", "low", "open", "close"]
    return df


# Connect to the SQLite database
con = sqlite3.connect("tick_btcusdt.db")

# Read a table from the database into a pandas dataframe
df = pd.read_sql_query("SELECT * FROM btcusdt", con)

# Close the database connection
con.close()

# Display the dataframe
df.time = pd.to_datetime(df.time, unit="ms")
df.set_index("time", inplace=True)

df["qty"] = df["qty"].astype(float)
df["price"] = df["price"].astype(float)
df["is_mm"] = df["is_mm"].astype(bool)

df["buy_vol"] = df.qty * (1 - df["is_mm"])
df["sell_vol"] = df.qty * df["is_mm"]
df["vol_delta"] = df["buy_vol"] - df["sell_vol"]

vol_delta = df["vol_delta"]

cvd = vol_delta.groupby(pd.Grouper(freq="7D")).cumsum()

cvd = agregate_by_time(cvd, "5T")
price = agregate_by_time(df.price, "5T")


print_candles([price, cvd])
