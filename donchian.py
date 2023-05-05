import pandas as pd
import numpy as np


def donchian_breakout(df: pd.DataFrame, lookback: int):
    # input df is assumed to have a close column
    df["upper"] = df["close"].rolling(lookback - 1).max().shift(1)
    df["lower"] = df["close"].rolling(lookback - 1).min().shift(1)
    df["signal"] = np.nan
    df.loc[df["close"] > df["upper"], "signal"] = 1
    df.loc[df["close"] < df["lower"], "signal"] = -1
    df["signal"] = df["signal"].ffill()


def signal_returns(df: pd.DataFrame, fee_amt: float = 0.001):
    df["log_return"] = np.log(df["close"]).diff().shift(-1)
    df["strategy_return"] = df["signal"] * df["log_return"]

    position_change = df["signal"].diff().abs()
    df["strategy_return"] -= position_change * fee_amt
    df["equity_curve"] = df["strategy_return"].cumsum()


def performance_metrics(df: pd.DataFrame, n_bars_in_year: int):
    r = df["strategy_return"]

    profit_factor = r[r > 0].sum() / r[r < 0].abs().sum()
    sharpe = r.mean() / r.std()
    sortino = r.mean() / (r[r < 0].std())

    # annualized ratios
    sharpe *= n_bars_in_year**0.5
    sortino *= n_bars_in_year**0.5
