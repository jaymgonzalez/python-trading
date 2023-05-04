import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG


# Define strategy class
class FiboStrategy(Strategy):
    def init(self):
        # Request hourly candle data from yfinance
        hist = yf.download(self.data.ticker, interval="60m")
        # Set data to match PineScript variables
        self.hourClose = hist["Close"]
        self.hourOpen = hist["Open"]
        self.prevHourClose = self.hourClose.shift(1)
        self.prevHourOpen = self.hourOpen.shift(1)
        # Calculate other variables
        self.barsInHour = 60 // self.data._interval.seconds
        self.lastSignalCandle = None
        self.signalCandleHigh = None
        self.signalCandleLow = None
        self.downfibo = False
        self.upFibo = False

    def next(self):
        # Candle setup
        openBarPrevious = self.prevHourOpen[-1]
        closeBarPrevious = self.prevHourClose[-1]
        openBarCurrent = self.hourOpen[-1]
        closeBarCurrent = self.hourClose[-1]

        bullishEngulfing = (
            (openBarCurrent <= closeBarPrevious)
            and (openBarCurrent < openBarPrevious)
            and (closeBarCurrent > openBarPrevious)
        )
        bearishEngulfing = (
            (openBarCurrent >= closeBarPrevious)
            and (openBarCurrent > openBarPrevious)
            and (closeBarCurrent < openBarPrevious)
        )

        # Signals
        bullEng = (
            bullishEngulfing
            and self.hourClose[-1]
            > SMA(self.hourClose, self.args[0] * self.barsInHour)[-1]
        )
        bearEng = (
            bearishEngulfing
            and self.hourClose[-1]
            < SMA(self.hourClose, self.args[0] * self.barsInHour)[-1]
        )

        self.downfibo = bearEng
        self.upFibo = bullEng

        # Get high and low of signal candle
        for i in range(-1, -1000, -1):
            if bullEng[i] or bearEng[i]:
                self.lastSignalCandle = i

                j = i
                while self.data.index[j].minute != 0:
                    if (
                        self.signalCandleHigh is None
                        or self.signalCandleHigh < self.data["High"][j]
                    ):
                        self.signalCandleHigh = self.data["High"][j]
                    if (
                        self.signalCandleLow is None
                        or self.signalCandleLow > self.data["Low"][j]
                    ):
                        self.signalCandleLow = self.data["Low"][j]
                    j += 1

                if (
                    self.signalCandleHigh is None
                    or self.signalCandleHigh < self.data["High"][j]
                ):
                    self.signalCandleHigh = self.data["High"][j]
                if (
                    self.signalCandleLow is None
                    or self.signalCandleLow > self.data["Low"][j]
                ):
                    self.signalCandleLow = self.data["Low"][j]

                break

        # Set fib data
        F0 = (
            self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            if self.upFibo
            else 0
        )
        F500 = (
            self.signalCandleLow + (self.signalCandleHigh - self.signalCandleLow) * 0.5
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * 0.5
            if self.upFibo
            else 0
        )

        FM272 = (
            (self.signalCandleHigh - self.signalCandleLow) * -0.272
            + self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * -0.272
            if self.upFibo
            else 0
        )
        FM618 = (
            (self.signalCandleHigh - self.signalCandleLow) * -0.618
            + self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * -0.618
            if self.upFibo
            else 0
        )
        F618 = (
            (self.signalCandleHigh - self.signalCandleLow) * 0.618
            + self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * 0.618
            if self.upFibo
            else 0
        )
        F660 = (
            (self.signalCandleHigh - self.signalCandleLow) * 0.66 + self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * 0.66
            if self.upFibo
            else 0
        )
        F882 = (
            (self.signalCandleHigh - self.signalCandleLow) * 0.882
            + self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * 0.882
            if self.upFibo
            else 0
        )
        F382 = (
            (self.signalCandleHigh - self.signalCandleLow) * 0.382
            + self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * 0.382
            if self.upFibo
            else 0
        )
        F1000 = (
            (self.signalCandleHigh - self.signalCandleLow) * 1.000
            + self.signalCandleLow
            if self.downfibo
            else self.signalCandleHigh
            - (self.signalCandleHigh - self.signalCandleLow) * 1.000
            if self.upFibo
            else 0
        )
