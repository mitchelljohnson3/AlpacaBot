import sys
sys.path.append('../util') # make modules in util folder available
from global_config import * # import all global config variables
from backtest_config import * # import all backtest specific variables
import file_io as io # file_io lets us write and read to files

class backtest():
    def __init__(self, file_names):
        self.RAW_DATA_FILE_NAMES = file_names # holds all file names to gather raw data from
        self.OUTPUT_FILE_NAMES = [] # holds all output file names
        self.INDICATORS = [] # holds all available indicators for use by strategy
        self.SYMBOLS = [] # holds all symbol names to be tested
        self.RAW_DATA = [] # holds all data of all symbols being backtested
        self.symbol_index = 0 # represents current index of symbol being backtested
        self.index = 0 # represents current index in raw_data array
        self.funds = STARTING_FUNDS # represents total amount of money
        self.num_shares = 0 # represents the number of shares currently owned
        self.average_share_price = 0.0 # represents the average share price

    def init(self):
        self.OUTPUT_FILE_NAMES = self.get_output_file_names()
        self.fill_indicators()
        self.SYMBOLS = self.fill_symbols()
        self.RAW_DATA = self.fill_raw_data()

    def fill_symbols(self): # uses file names and creates symbols list
        symbols = [] # empty list to hold symbols
        for filename in self.RAW_DATA_FILE_NAMES:
            symbol = filename.split('%')[0] # split filename by %
            symbols.append(symbol) # append symbol to list
        return symbols # return completed list

    def fill_indicators(self):
        for value in SMA: self.INDICATORS.append("SMA" + str(value)) # append all requested SMA periods
        for value in EMA: self.INDICATORS.append("EMA" + str(value)) # append all requested EMA periods
        if (RSI): self.INDICATORS.append("RSI") # append RSI
        if (MACD):
            self.INDICATORS.append("MACD") # append MACD
            self.INDICATORS.append("MACDSig") # append MACD signal line
            self.INDICATORS.append("MACDHist") # append MACD histogram

    def fill_raw_data(self):
        raw_data = []
        for filename in self.RAW_DATA_FILE_NAMES: # reads data in from csv file, converts to a list of objects
            lines = io.readFile('./analyzed_data/' + filename).readlines() # read all lines from a file into a list
            bars = self.construct_bars_data(lines) # convert list into list of objects
            raw_data.append(bars) # append finished bars data for one symbol
        return raw_data # return completed list of data

    def get_total_assets(self):
        return round( (self.funds + (self.num_shares * self.getCurrent('c'))), 2)

    def construct_bars_data(self, lines):
        bars = [] # empty list will hold all bar data
        for i in range(len(lines)):
            if (i == 0): continue # skip the first line
            values = lines[i].split(',') # split line by comma to separate values
            bar_object = {} # empty object representing 1 bar
            bar_object['t'] = values[0] # add time
            bar_object['o'] = float(values[1]) # add open
            bar_object['h'] = float(values[2]) # add high
            bar_object['l'] = float(values[3]) # add low
            bar_object['c'] = float(values[4]) # add close
            bar_object['v'] = int(values[5]) # add volume
            bar_object['assets'] = STARTING_FUNDS # add total assets
            bar_object['buy'] = 0 # add buy signal
            bar_object['sell'] = 0 # add sell signal
            for i in range(len(self.INDICATORS)):
                bar_object[self.INDICATORS[i]] = float(values[6 + i])
            bars.append(bar_object) # append bar object to list
        return bars # return completed bars array

    def getCurrent(self, indicator): # gets current value of 'indicator'
        return self.RAW_DATA[self.symbol_index][self.index][indicator]

    def setCurrent(self, indicator, val): # sets current bar object 'indicator' to 'val'
        self.RAW_DATA[self.symbol_index][self.index][indicator] = val

    def getIndex(self, index, indicator): # gest current 'indicator' of bar object at 'index'
        return self.RAW_DATA[self.symbol_index][index][indicator]

    def crossesOver(self, indicator_1, indicator_2): # returns true if indicator_1 JUST crossed over indicator 2
        currentlyOver = (self.getCurrent(indicator_1) > self.getCurrent(indicator_2))
        previouslyNotOver = (self.getIndex(self.index - 1, indicator_1) < self.getIndex(self.index - 1, indicator_2))
        return (currentlyOver and previouslyNotOver)

    def overValue(self, indicator_1, value): # returns true if indicator_1 is currently over value
        return (self.getCurrent(indicator_1) > value)

    def buyAll(self): # buys the maximum number of shares possible with current funds
        max_shares = self.funds / self.getCurrent('c')
        self.buy(max_shares)

    def sellAll(self): # sells all shares
        self.sell(self.num_shares)

    def buy(self, num_shares): # buys a number of shares
        cost = num_shares * self.getCurrent('c')
        if (cost > self.funds): 
            print("insufficent funds")
            return
        self.funds -= cost
        self.num_shares += num_shares
        self.setCurrent('buy', self.getCurrent('c'))

    def sell(self, num_shares): # sells a number of shares
        if (self.num_shares < num_shares):
            print("insufficient shares")
            return
        self.num_shares -= num_shares
        self.funds += (num_shares * self.getCurrent('c'))
        self.setCurrent('sell', self.getCurrent('c'))

    def resetModule(self): # resets all necessary values in module to prepare for next symbol backtest
        self.index = 0 # reset index
        self.funds = STARTING_FUNDS
        self.num_shares = 0
        self.average_share_price = 0.0

    def get_output_file_names(self): # returns the filenames of the backtest results
        filename_list = []
        for i in range(len(self.RAW_DATA_FILE_NAMES)):
            split = self.RAW_DATA_FILE_NAMES[i].split('%')
            filename = '{}%{}%{}%{}%BACKTEST'.format(split[0],split[1],split[2],split[3])
            filename_list.append(filename + '.csv')
        return filename_list

    def setup_fileheader(self, file_name): # writes a header to the top of the file
        path = './backtest_results/' + file_name
        header = 'Date,Open,High,Low,Close,Assets,Buy,Sell'
        io.writeToFile(path, header) # write header to file
        return path

    def output_backtest_results(self, file_name): # outputs all analyzed data in raw_data to output files
        path = self.setup_fileheader(file_name) # set up file header and receive path to created file
        for j in range(len(self.RAW_DATA[self.symbol_index])):
            for ind in self.INDICATORS: self.RAW_DATA[self.symbol_index][j].pop(ind) # remove indicators from object
            self.RAW_DATA[self.symbol_index][j].pop('v')
            data_list = list(self.RAW_DATA[self.symbol_index][j].values())
            for k in range(len(data_list)): data_list[k] = str(data_list[k]) # cast values to strings
            s = ","
            data = s.join(data_list)
            io.appendToFile(path, data) # append data to file

    def update(self): # increases index by 1, upon reaching end of first symbol array, increases symbol_index by 1 and resets index to 0
        self.setCurrent('assets', self.get_total_assets()) # update current assets
        self.index += 1 # increment index by 1

        if (self.index == len(self.RAW_DATA[self.symbol_index])): # if true, we have finished backtesting a symbol, reset and prepare for next test
            self.output_backtest_results(self.OUTPUT_FILE_NAMES[self.symbol_index]) # write backtest data for current symbol to results folder
            self.resetModule() # reset values of module
            self.symbol_index += 1 # move onto next symbol
        
        if (self.symbol_index == len(self.RAW_DATA)): # if true, we have reached end of backtest
            return False # signifies end of backtest

        return True # signifies all good, keep going
        