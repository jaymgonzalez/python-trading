import download_yfinance as yf
import argparse
from datetime import date, timedelta, datetime
# from bokeh.models import DatetimeTickFormatter

# formatter = DatetimeTickFormatter(hourmin='%H:%M')
# Define and parse command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--ticker", type=str, required=True, help="Ticker symbol")
parser.add_argument("-ti", "--time_interval", type=str, required=True, help="Time interval (e.g. 6m, 1y, 1d)")
parser.add_argument("-i", "--interval", type=str, default="5m", help="Data interval (default: 5m)")
parser.add_argument("-o", "--output_file", type=str, help="Output file name if different from default (default: tiker_timeint_int.csv)")

args = parser.parse_args()

if args.time_interval.endswith("d"):
    days = int(args.time_interval[:-1])
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
elif args.time_interval.endswith("m"):
    months = int(args.time_interval[:-1])
    end_date = date.today()
    start_month = end_date.month - months
    start_year = end_date.year
    if start_month <= 0:
        start_month += 12
        start_year -= 1
    start_date = date(start_year, start_month, 1)
else:
    years = int(args.time_interval[:-1])
    end_date = date.today()
    start_date = date(end_date.year - years, end_date.month, 1)

# Add Date column
def add_date_column(data, interval):
    start_time = data.index[0]
    time_number, time_letter = int(interval[0]), interval[1]

    if time_letter == 'm':
        date_list = [start_time + timedelta(minutes=i*time_number) for i in range(len(data))]
    elif time_letter == 'd':
        date_list = [start_time + timedelta(days=i*time_number) for i in range(len(data))]
    elif time_letter == 'h':
        date_list = [start_time + timedelta(hours=i*time_number) for i in range(len(data))]
    else:
        raise Exception(f"Invalid time {time_letter}. Use d, h or m")
    
    data.insert(0, "Date", date_list)

# Download the data
data = yf.download(args.ticker, start=start_date, end=None, interval=args.interval)

# Save the data to a CSV file
file_output = f"./{args.ticker}_{args.interval}_{args.time_interval}.csv"
add_date_column(data, args.interval)
data.to_csv(file_output, index=False)

print(f"Data for {args.ticker} from {start_date} to {end_date} with interval {args.interval} saved to {file_output}")
