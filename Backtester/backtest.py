import sys
sys.path.append('../util') # make modules in util folder available
from global_config import * # import all global config variables
from backtest_config import * # import all backtest specific variables
import file_io as io # file_io lets us write and read to files

class backtest():
    def __init__(self, file_names):
        self.RAW_DATA_FILE_NAMES = file_names # holds all file names to gather raw data from
        self.SYMBOLS = self.fill_symbols() # holds all symbol names
        self.RAW_DATA = self.fill_raw_data() # holds all data of all symbols being analyzed
        self.INDICATORS = self.fill_indicators() # holds all requested indicators to be calculated
        self.INDEX = 0 # represents current index in both symbols and raw_data array

    def fill_symbols(self): # uses file names and creates symbols list
        symbols = [] # empty list to hold symbols
        for filename in self.RAW_DATA_FILE_NAMES:
            symbol = filename.split('%')[0] # split filename by %
            symbols.append(symbol) # append symbol to list
        return symbols # return completed list

    def fill_indicators(self):
        for value in SMA: self.INDICATORS.append(str(value)) # append all requested SMA periods
        for value in EMA: self.INDICATORS.append(str(value)) # append all requested EMA periods
        if (RSI): self.INDICATORS.append("RSI") # append RSI
        if (MACD): self.INDICATORS.append("MACD") # append MACD

    def fill_raw_data(self):
        raw_data = []
        for filename in self.RAW_DATA_FILE_NAMES: # reads data in from csv file, converts to a list of objects
            lines = io.readFile('./raw_symbol_data/' + filename).readlines() # read all lines from a file into a list
            bars = self.construct_bars_data(lines) # convert list into list of objects
            raw_data.append(bars) # append finished bars data for one symbol
        return raw_data # return completed list of data

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
            bars.append(bar_object) # append bar object to list
        return bars # return completed bars array

    def update(self): # increases index by 1
        pass
        