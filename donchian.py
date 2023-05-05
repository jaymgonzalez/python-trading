import pandas as pd
import numpy as np
from binance.client import Client


def donchian_breakout(df: pd.DataFrame, lookback: int):
    # input df is assumed to have a close column
    df["upper"] = df["close"].rolling(lookback - 1).max().shift(1)
    df["lower"] = df["close"].rolling(lookback - 1).min().shift(1)
    df["signal"] = np.nan
    df.loc[df["close"] > df["upper"], "signal"] = 1
    df.loc[df["close"] < df["lower"], "signal"] = -1
    df["signal"] = df["signal"].ffill()

    return df


def signal_returns(df: pd.DataFrame, fee_amt: float = 0.001):
    df["log_return"] = np.log(df["close"]).diff().shift(-1)
    df["strategy_return"] = df["signal"] * df["log_return"]

    position_change = df["signal"].diff().abs()
    df["strategy_return"] -= position_change * fee_amt
    df["equity_curve"] = df["strategy_return"].cumsum()

    return df


def performance_metrics(df: pd.DataFrame, n_bars_in_year: int):
    r = df["strategy_return"]

    profit_factor = r[r > 0].sum() / r[r < 0].abs().sum()
    sharpe = r.mean() / r.std()
    sortino = r.mean() / (r[r < 0].std())

    # annualized ratios
    sharpe *= n_bars_in_year**0.5
    sortino *= n_bars_in_year**0.5

    return {
        "Profit factor": profit_factor,
        "Sharpe ratio": sharpe,
        "Sortino ratio": sortino,
    }


def get_binance_data(symbol: str = "BTCUSDT") -> pd.DataFrame:
    client = Client()

    klines = client.get_historical_klines(
        symbol, Client.KLINE_INTERVAL_1HOUR, "2 year ago UTC"
    )

    df = pd.DataFrame(
        klines,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "vol",
            "close_time",
            "quote_vol",
            "trades",
            "taker_base_vol",
            "taker_quote_vol",
            "ignore",
        ],
    )

    df = df[["open_time", "open", "high", "low", "close"]]

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

    df["open"] = df.open.astype(float)
    df["high"] = df.high.astype(float)
    df["low"] = df.low.astype(float)
    df["close"] = df.close.astype(float)

    df.set_index("open_time", inplace=True)

    df.to_csv("BTCUSDT.csv", index=True)

    return df


if __name__ == "__main__":
    # df = get_binance_data()
    df = pd.read_csv("BTCUSDT.csv")
    df = donchian_breakout(df, 72)
    df = signal_returns(df)
    print(performance_metrics(df, 8760))
