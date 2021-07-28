import sys  # allows us to see arguments
sys.path.append('../config')  # make modules in util folder available
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd  # helps with reading .csv files
from backtest_config import *  # import config settings


def graph_a(data_file_name):
    # read in data from csv file
    data = pd.read_csv('./analyzed_data/' + data_file_name) # read csv file
    symbol = data_file_name.split('%')[0]

    plt.style.use('ggplot')

    # Extracting Data for plotting
    ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    ohlc['Date'] = pd.to_datetime(ohlc['Date'])
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)

    # Creating Subplots
    num_plots = 1
    if (RSI): num_plots += 1
    if (MACD): num_plots += 1
    fig, ax = plt.subplots(num_plots)

    # Formatting Date
    date_format = mpl_dates.DateFormatter('%m-%d-%Y')
    fig.tight_layout()

    # creating candlestick chart
    candlestick_ohlc(ax[0], ohlc.values, width=0.6,
                     colorup='green', colordown='red', alpha=0.8)
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Price')
    ax[0].xaxis.set_major_formatter(date_format)

    # setup main title
    fig.suptitle('{} {}'.format(symbol, TIME_FRAME))

    if (RSI):
        _data = data.loc[:, ['RSI']]
        ax[1].set_xlabel('Date')
        ax[1].set_ylabel('RSI')
        ax[1].plot(_data['RSI'], color = 'black')
        ax[1].axhline(y = 70, color = 'red')
        ax[1].axhline(y = 30, color = 'green')
        ax[1].xaxis.set_visible(False)
        labels = ["RSI", "Overbought Signal", "Underbought Signal"]
        ax[1].legend(labels)

    if (MACD):
        _data = (data.loc[:, ['MACD', 'MACDSig', 'MACDHist']])
        ax[2].set_xlabel('Date')
        ax[2].set_ylabel('MACD')
        ax[2].plot(_data['MACD'], color = 'green')
        ax[2].plot(_data['MACDSig'], color = 'red')
        #ax[2].hist(_data['MACDHist'], color = 'yellow')
        ax[2].xaxis.set_visible(False)
        labels = ["MACD", "MACD Signal", "MACD Histogram"]
        ax[2].legend(labels)
        
    plt.show()




def graph_b(filename):
    pass
