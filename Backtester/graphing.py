import sys  # allows us to see arguments
sys.path.append('../config')  # make modules in util folder available
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd  # helps with reading .csv files
from backtest_config import *  # import config settings


def graph(analyzed_data_file_names, backtest_results_file_names):
    for i in range(len(analyzed_data_file_names)):
        # Creating Subplots
        plt.style.use('ggplot')
        num_plots = 1
        if (RSI): num_plots += 1
        if (MACD): num_plots += 1
        fig, ax = plt.subplots(num_plots)

        # read in data from csv file
        data = pd.read_csv('./analyzed_data/' + analyzed_data_file_names[i]) # read csv file
        symbol = analyzed_data_file_names[i].split('%')[0]

        # Extracting Data for plotting
        ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc['Date'] = pd.to_datetime(ohlc['Date'])
        ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
        ohlc = ohlc.astype(float)

        # setup main title
        fig.suptitle('{} {}'.format(symbol, TIME_FRAME))

        # Formatting Date
        date_format = mpl_dates.DateFormatter('%m-%d-%Y')
        fig.tight_layout()

        # creating candlestick chart
        candlestick_ohlc(ax[0], ohlc.values, width=0.6,
                        colorup='green', colordown='red', alpha=0.8)
        ax[0].set_xlabel('Date')
        ax[0].set_ylabel('Price')
        ax[0].xaxis.set_major_formatter(date_format)

        # creating RSI chart if enabled
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

        # creating MACD chart if enabled
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
    
    for i in range(len(backtest_results_file_names)):
        # Creating Subplots
        plt.style.use('ggplot')
        fig, ax = plt.subplots(2)

        # read in data from csv file
        data = pd.read_csv('./backtest_results/' + backtest_results_file_names[i]) # read csv file
        symbol = backtest_results_file_names[i].split('%')[0]

        # Extracting Data for plotting
        ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        ohlc['Date'] = pd.to_datetime(ohlc['Date'])
        ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
        ohlc = ohlc.astype(float)

        # setup main title
        fig.suptitle('{} {} Backtest Results'.format(symbol, TIME_FRAME))

        # Formatting Date
        date_format = mpl_dates.DateFormatter('%m-%d-%Y')
        fig.tight_layout()

        # creating candlestick chart
        candlestick_ohlc(ax[0], ohlc.values, width=0.6,
                        colorup='green', colordown='red', alpha=0.8)
        ax[0].set_xlabel('Date')
        ax[0].set_ylabel('Price')
        ax[0].xaxis.set_major_formatter(date_format)

        # plot buy and sell signals on graph
        _data = data.loc[:, ['Buy', 'Sell']]
        buys = _data['Buy']
        sells = _data['Sell']
        for i in range(len(buys)):
            if buys[i] > 0: ax[0].axvline(x = ohlc['Date'][i], color = 'green')
        for i in range(len(sells)):
            if sells[i] > 0: ax[0].axvline(x = ohlc['Date'][i], color = 'red')
        labels = ["Buy", "Sell"]
        ax[0].legend(labels)

        _data = data.loc[:, ['Assets']]
        ax[1].set_xlabel('Date')
        ax[1].set_ylabel('Assets')
        ax[1].plot(_data['Assets'], color = 'black')
        ax[1].xaxis.set_visible(False)
        
    plt.show()