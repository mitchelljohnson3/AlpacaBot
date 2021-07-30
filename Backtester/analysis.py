import sys
sys.path.append('../util') # make modules in util folder available
sys.path.append('../config') # make modules in util folder available
from global_config import * # import all global config variables
from backtest_config import * # import all backtest specific variables
import file_io as io # file_io lets us write and read to files
import util as util # utility functions

class analysis():
    def __init__(self, file_names):
        self.RAW_DATA_FILE_NAMES = file_names # holds all file names to gather raw data from
        self.INDICATORS = [] # holds all requested indicators to be calculated
        self.SYMBOLS = [] # holds all symbol names
        self.RAW_DATA = [] # holds all data of all symbols being analyzed
        self.index = 0 # represents current position in RAW_DATA[symbol_index]
        self.symbol_index = 0 # represents current position in RAW_DATA

    def fill_symbols(self, raw_data_file_names): # uses file names and creates symbols list
        for filename in raw_data_file_names:
            symbol = filename.split('%')[0] # split filename by %
            self.SYMBOLS.append(symbol) # append symbol to list
        
    def fill_indicators(self):
        for value in SMA: self.INDICATORS.append("SMA" + str(value)) # append all requested SMA periods
        for value in EMA: self.INDICATORS.append("EMA" + str(value)) # append all requested EMA periods
        if (RSI): self.INDICATORS.append("RSI") # append RSI
        if (MACD): 
            self.INDICATORS.append("EMA12") # append MACD
            self.INDICATORS.append("EMA26") # append MACD
            self.INDICATORS.append("MACD") # append MACD
            self.INDICATORS.append("MACDSig") # append MACD signal line
            self.INDICATORS.append("MACDHist") # append MACD histogram

    def fill_raw_data(self, raw_data_file_names):
        for filename in raw_data_file_names: # reads data in from csv file, converts to a list of objects
            lines = io.readFile('./raw_symbol_data/' + filename).readlines() # read all lines from a file into a list
            bars = self.construct_bars_data(lines) # convert list into list of objects
            self.RAW_DATA.append(bars) # append finished bars data for one symbol

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
            for ind in self.INDICATORS: # append values for each requested indicator
                bar_object[ind] = 0.0
            bars.append(bar_object) # append bar object to list
        return bars # return completed bars array

    def get_file_names(self, raw_data_file_names): # returns file names for analyzed data
        file_names = [] # empty list to hold all file names of analyzed data
        indicators = "" # empty string to hold all indicators
        for ind in self.INDICATORS:
            if (ind in DO_NOT_INCLUDE_IN_FILENAME): continue # don't include certain symbol in filename
            indicators += "%" + ind # append all indicators separated by a '%'
        for i in range(len(raw_data_file_names)):
            new_filename = raw_data_file_names[i].split('.')[0] # isolate just the file name without the .csv
            new_filename += indicators + ".csv" # append indicators to end of file name
            file_names.append(new_filename) # append new file name to list
        return file_names # return file_names

    def calculateIndicators(self):
        for period in SMA: # place SMA value on current bar object
            sma = self.calculateSMA(period)
            if (sma != 0.0): self.setCurrent('SMA' + str(period), sma)
        for period in EMA: # place EMA value on current bar object
            ema = self.calculateEMA(period)
            if (ema != 0.0): self.setCurrent('EMA' + str(period), ema)
        if (RSI): # place RSI value on current bar object
            rsi = self.calculateRSI()
            if (rsi != 0.0): self.setCurrent('RSI', rsi)
        if (MACD): # calculate and place all macd values on current bar object
            ema12 = self.calculateEMA(12)
            if (ema12 != 0.0): self.setCurrent('EMA12', ema12)
            ema26 = self.calculateEMA(26)
            if (ema26 != 0.0): self.setCurrent('EMA26', ema26)
            macd = self.calculateMACD()
            if (macd != 0.0): self.setCurrent('MACD', macd)
            macdsig = self.calculateMACDSig()
            if (macdsig != 0.0): self.setCurrent('MACDSig', macdsig)
            macdhist = self.calculateMACDHist()
            if (macdhist != 0.0): self.setCurrent('MACDHist', macdhist)

    def calculateSMA(self, period):
        if (self.index < (period - 1)): return 0.0 # if not enough data to calculate with this period, return 0.0
        sum = 0.0 # empty incrementer sum
        for i in range(period):
            sum += self.getIndex(self.index - i, 'c') # add the last 5 bar closes to sum
        newSMA = sum / period # calculate new SMA
        return round(newSMA, 2) # return SMA

    def calculateEMA(self, period):
        if (self.index < (period - 1)): return 0.0 # if not enough data to calculate with this period, return 0.0
        previousEMA = self.getIndex(self.index - 1, 'EMA' + str(period)) # get previous bars EMA
        if (previousEMA == 0.0): previousEMA = self.calculateSMA(period) # at the start, start with SMA of same period
        k = (2 / (period + 1)) # calculate k, used in calculation of EMA
        newEMA = (k * self.getCurrent('c')) + (previousEMA * (1 - k)) # calculate new EMA
        return round(newEMA, 2) # return new EMA

    def calculateRSI(self):
        if (self.index < (RSI_PERIOD)): return 0.0 # first RSI shows on bar 15
        gainSum, lossSum = 0.0, 0.0 # declare variables
        for i in range(RSI_PERIOD): # get sum of all gains and lossed over RSI_PERIOD
            change = self.getIndex(self.index - i, 'c') - self.getIndex((self.index - (i + 1)), 'c')
            if (change > 0): gainSum += change
            else: lossSum += abs(change)
        gainAvg = gainSum / RSI_PERIOD # get avg gain and avg loss
        lossAvg = lossSum / RSI_PERIOD
        _rs = 0
        if (lossAvg != 0): _rs = gainAvg / lossAvg # prevent dividing by 0
        newRSI = 100 - (100/(1 + _rs)) # calculate new RSI
        return round(newRSI, 2) # return new RSI

    def calculateMACD(self):
        if (self.index < 25): return 0.0 # EMA26 is required in calculation of MACD
        newMACD = self.calculateEMA(12) - self.calculateEMA(26) # calculate newMACD
        return round(newMACD, 2) # return newMACD

    def calculateMACDSig(self):
        if (self.index < 34): return 0.0 # MACDSig is a 9 period EMA of the MACD
        previousMACDSig = self.getIndex(self.index - 1, 'MACDSig') # get previous bars MACDSig
        k = (2 / (10)) # calculate k, used in calculation of EMA
        newMACDSig = (k * self.getCurrent('MACD')) + (previousMACDSig * (1 - k)) # calculate new EMA
        return round(newMACDSig, 2) # return new EMA

    def calculateMACDHist(self):
        if (self.index < 34): return 0.0 # MACDHist is the difference between MACD and MACDSig, both are required to calculate
        newMACDHist = self.getCurrent('MACD') - self.getCurrent('MACDSig') # calculate new MACDHist
        return round(newMACDHist, 2) # return new MACDHist

    def getCurrent(self, indicator): # gets current value of 'indicator'
        return self.RAW_DATA[self.symbol_index][self.index][indicator]

    def setCurrent(self, indicator, val): # sets current bar object 'indicator' to 'val'
        self.RAW_DATA[self.symbol_index][self.index][indicator] = val

    def getIndex(self, index, indicator): # gest current 'indicator' of bar object at 'index'
        return self.RAW_DATA[self.symbol_index][index][indicator]

    def output_analyzed_data(self, output_file_names): # outputs all analyzed data in raw_data to output files
        for i in range(len(output_file_names)):
            path = self.setup_fileheader(output_file_names[i]) # set up file header and receive path to created file
            for j in range(len(self.RAW_DATA[i])):
                for ind in DO_NOT_INCLUDE_IN_DATA: self.RAW_DATA[i][j].pop(ind) # remove indicators from object
                data_list = list(self.RAW_DATA[i][j].values())
                for k in range(len(data_list)): data_list[k] = str(data_list[k]) # cast values to strings
                s = ","
                data = s.join(data_list)
                io.appendToFile(path, data) # append data to file

    def setup_fileheader(self, file_name): # writes a header to the top of the file
        path = './analyzed_data/' + file_name
        header = 'Date,Open,High,Low,Close,Volume'
        for ind in self.INDICATORS: 
            if (ind in DO_NOT_INCLUDE_IN_DATA): continue # don't write items in doNotInclude to output file
            header += ',' + ind # append all indicators to header
        io.writeToFile(path, header) # write header to file
        return path

    def run(self):
        self.fill_indicators() # add all requested indicators to indicators object
        output_file_names = self.get_file_names(self.RAW_DATA_FILE_NAMES) # get analysis output file names
        valid_input_file_names = []
        valid_output_file_names = [] # this array will hold all valid file names associated with each valid symbol
        for i in range(len(output_file_names)):
            if (io.fileExistsIn('./analyzed_data', output_file_names[i]) is False): # if file does not already exist..
                valid_output_file_names.append(output_file_names[i]) # append file_name to valid list
                valid_input_file_names.append(self.RAW_DATA_FILE_NAMES[i]) # append original file name to valid list
        self.fill_symbols(valid_input_file_names) # fill symbols list using filenames
        self.fill_raw_data(valid_input_file_names) # construct bars list from each file csv and append to raw data
        for i in range(len(self.SYMBOLS)): # analyze each symbol
            for j in range(len(self.RAW_DATA[i])): # calculate indicators for each bar in raw_data
                self.calculateIndicators() # calculate and append indicators
                self.index += 1 # increment index in self.RAW_DATA[self.symbol_index]
            self.index = 0 # reset index to 0
            self.symbol_index += 1 # increment symbol index
        self.output_analyzed_data(valid_output_file_names) # output analyzed data to data files
        return output_file_names # return file names with analyzed data