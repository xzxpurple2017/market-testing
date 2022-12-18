import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest, CryptoLatestQuoteRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

# Load environment variables from .env file
load_dotenv()
API_KEY = os.environ["APCA-API-KEY-ID"]
SECRET_KEY = os.environ["APCA-API-SECRET-KEY"]

# no keys required.
crypto_client = CryptoHistoricalDataClient()

# keys required
stock_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# Ticker
ticker = "SPY"

# Get candlestick bars
start_datetime_str = "2022-12-16 07:00:00"
end_datetime_str = "2022-12-17 07:00:00"

date_format = "%Y-%m-%d %H:%M:%S"
date_timezone = timezone('US/Eastern')

def plot_graph(ticker, start_datetime_str, end_datetime_str):
    start_datetime_object = datetime.strptime(start_datetime_str, date_format)
    start_local_date = date_timezone.localize(start_datetime_object)

    end_datetime_object = datetime.strptime(end_datetime_str, date_format)
    end_local_date = date_timezone.localize(end_datetime_object)

    request_params = StockBarsRequest(
                            symbol_or_symbols=[ticker],
                            timeframe=TimeFrame.Minute,
                            start=start_local_date,
                            end=end_local_date
                    )

    bars = stock_client.get_stock_bars(request_params)
    df = bars.df

    # Bar data candlestick plot
    candlestick_fig = go.Figure(data=[go.Candlestick(x=df.index.get_level_values('timestamp').tz_convert('US/Eastern'),
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])

    fig = go.Figure(data=candlestick_fig.data)

    # Adding a title and axes labels
    fig.update_layout(
        title="Price of {} from {} to {}".format(ticker, start_datetime_str, end_datetime_str),
        xaxis_title="Minute",
        yaxis_title="Price ($USD)",
    )

    # Displaying our chart
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show()

plot_graph(ticker, start_datetime_str, end_datetime_str)