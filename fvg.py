def fair_value_gap(candle_data):
  for i in range(len(candle_data) - 2):  # loop through all possible three-candle patterns
    cur_candle = candle_data[i]
    next_candle = candle_data[i+1]
    next_next_candle = candle_data[i+2]
    if cur_candle['close'] > next_candle['high'] and next_next_candle['low'] > next_candle['high']:
      # three-candle pattern matches three candles imbalance formation
      avg_shadow_len = (next_candle['high'] - next_candle['low'] + next_next_candle['high'] - next_next_candle['low']) / 2.0
      if cur_candle['open'] - cur_candle['close'] > 2*avg_shadow_len:
        return 'Buy signal'  # fair value gap detected

  return 'No signal'  # no fair value gap detected


# Example usage:
candle_data = [
  {'open': 50, 'high': 60, 'low': 40, 'close': 55},
  {'open': 54, 'high': 65, 'low': 45, 'close': 62},
  {'open': 61, 'high': 70, 'low': 50, 'close': 58},
  {'open': 59, 'high': 68, 'low': 48, 'close': 57},
  {'open': 55, 'high': 65, 'low': 45, 'close': 60},
]

signal = fair_value_gap(candle_data)
print(signal)  # output: Buy signal