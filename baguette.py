import ta

# Get hourly candle data
hour_close = request_security(syminfo.tickerid, "60", close, gaps=barmerge.gaps_on)
hour_open = request_security(syminfo.tickerid, "60", open, gaps=barmerge.gaps_on)
prev_hour_close = request_security(
    syminfo.tickerid, "60", close[1], gaps=barmerge.gaps_on
)
prev_hour_open = request_security(
    syminfo.tickerid, "60", open[1], gaps=barmerge.gaps_on
)

# Candle setup
open_bar_previous = prev_hour_open
close_bar_previous = prev_hour_close
open_bar_current = hour_open
close_bar_current = hour_close

bullish_engulfing = (
    (open_bar_current <= close_bar_previous)
    and (open_bar_current < open_bar_previous)
    and (close_bar_current > open_bar_previous)
)
bearish_engulfing = (
    (open_bar_current >= close_bar_previous)
    and (open_bar_current > open_bar_previous)
    and (close_bar_current < open_bar_previous)
)

# Signals
bull_eng = bullish_engulfing and hour_close > ta.ema(close, ema_confirm * bars_in_hour)
bear_eng = bearish_engulfing and hour_close < ta.ema(close, ema_confirm * bars_in_hour)

down_fibo = bear_eng
up_fibo = bull_eng

# Get high and low of signal candle
last_signal_candle = 1000
signal_candle_high = 0.00
signal_candle_low = 0.00

for i in range(1000):
    if bull_eng[i] or bear_eng[i]:
        last_signal_candle = i

        j = i
        while minute[j] != 0:
            if signal_candle_high < high[j] or signal_candle_high == 0.00:
                signal_candle_high = high[j]
            if signal_candle_low > low[j] or signal_candle_low == 0.00:
                signal_candle_low = low[j]
            j += 1

        if signal_candle_high < high[j] or signal_candle_high == 0.00:
            signal_candle_high = high[j]
        if signal_candle_low > low[j] or signal_candle_low == 0.00:
            signal_candle_low = low[j]

        break

# Set fib data
F0 = signal_candle_low if down_fibo else signal_candle_high if up_fibo else 0
F500 = (
    (signal_candle_high - signal_candle_low) * 0.500 + signal_candle_low
    if down_fibo
    else signal_candle_high - (signal_candle_high - signal_candle_low) * 0.500
    if up_fibo
    else 0
)
FM272 = (
    (signal_candle_high - signal_candle_low) * -0.272 + signal_candle_low
    if down_fibo
    else signal_candle_high - (signal_candle_high - signal_candle_low) * -0.272
    if up_fibo
    else 0
)
FM618 = (
    (signal_candle_high - signal_candle_low) * -0.618 + signal_candle_low
    if down_fibo
    else signal_candle_high - (signal_candle_high - signal_candle_low) * -0.618
    if up_fibo
    else 0
)
F618 = (
    (signal_candle_high - signal_candle_low) * 0.618 + signal_candle_low
    if down_fibo
    else signal_candle_high - (signal_candle_high - signal_candle_low) * 0.618
)
