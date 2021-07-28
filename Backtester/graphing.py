import sys # allows us to see arguments
sys.path.append('../config') # make modules in util folder available
import plotly.graph_objects as go # useful graphing library
from plotly.subplots import make_subplots # allows us to make graph subplots
import pandas as pd # helps with reading .csv files
from backtest_config import * # import all backtest specific variables

def graph_a(data_file_name):
    df = pd.read_csv('./analyzed_data/' + data_file_name) # read csv file
    symbol = data_file_name.split('%')[0]

    #this chart will display candlestick, RSI, and MACD
    fig = make_subplots(
    rows=3, 
    cols=1, 
    subplot_titles=(f"{symbol} Candlestick", "RSI", "MACD"))
    #create candlestick chart
    if (CANDLE_OR_SIMPLE):
        fig.append_trace(   
            go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=('Candle')
                        ),row=1, col=1)
        fig.update_xaxes(row=1, col=1, rangeslider_visible=False)
    #or create a simpleifed price chart
    else: 
        fig.append_trace(go.Scatter(x=df['Date'], y=df[(
                'Close')], text="Price", name="Price", line=dict(color='rgb(0, 0, 0)')), row=1, col=1)
    #adds RSI indicator and overbought and underbought signals
    if (RSI):
        fig.append_trace(go.Scatter(x=df['Date'], y=df["RSI"], text="RSI", name="RSI", line=dict(color='rgb(0, 0, 0)')), row=2, col=1)
    #adds MACD indicator
    if (MACD):
        fig.append_trace(go.Scatter(x=df['Date'], y=df["MACD"], text="MACD", name="MACD", line=dict(color='rgb(0, 128, 0)')), row=3, col=1)
        fig.append_trace(go.Scatter(x=df['Date'], y=df["MACDSig"], text="MACD Signal", name="MACD Signal", line=dict(color='rgb(255, 0, 0)')), row=3, col=1)
        fig.append_trace(go.Bar(x=df['Date'], y=df["MACDHist"], text="MACD Histogram", name="MACD Histogram"), row=3, col=1)
    #add split and dividend signals to chart
    splits = df[('Split')]
    dividends = df[('Dividend')]
    print(splits)
    print(dividends)
    fig.append_trace(go.Scatter(x=df['Date'], y=df[(
                'Split')], text="Split", name="Split", mode="markers", line=dict(color='rgb(0, 128, 0)')), row=1, col=1)
    fig.append_trace(go.Scatter(x=df['Date'], y=df[(
                'Dividend')], text="Dividend", name="Dividend", mode="markers", line=dict(color='rgb(255, 0, 0)')), row=1, col=1)

    #show plot, opens in browser
    fig.show()

def graph_b(filename):
    pass