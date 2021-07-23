import sys
sys.path.append('../util') # make modules in util folder available
import requests, json # requests lets us make web requests, json gives us tools that help dealing with json
from global_config import * # import all global config variables
from backtest_config import * # import all backtest specific variables
import file_io as io # file_io lets us write and read to files

class fetch():
    def __init__(self):
        self.ADJUSTED_DATE_START = DATE_START + "T09:30:00+00:00" # market opens at 9:30am EST
        self.ADJUSTED_DATE_END = DATE_END + "T17:30:00+00:00" # market closes at 4:30pm EST
        self.PARAMETERS = { 'start': self.ADJUSTED_DATE_START, 'end': self.ADJUSTED_DATE_END, 'limit': LIMIT, 'timeframe': TIME_FRAME }
        self.FULL_VALID_SYMBOLS = SYMBOLS_TO_TEST

    def get_symbol_data(self, symbol):
        BARS_URL = '{}/v2/stocks/{}/bars'.format(DATA_URL, symbol) # formatting url to fetch data from api
        r = requests.get(BARS_URL, params=self.PARAMETERS, headers=HEADERS) # make the api request
        return json.loads(r.content) # convert string to python dict and return it

    def get_remaining_data(self, symbol, raw):
        keep_going = True # bool used to continue while loop until all data is gathered
        _parameters = self.PARAMETERS # pulling base parameter object from config
        BARS_URL = '{}/v2/stocks/{}/bars'.format(DATA_URL, symbol) # formatting url to fetch data from api
        previous_data = raw # previous_data will hold the last gathered data set, starting from raw
        master_data = { 'bars': raw['bars'] } # this object will have its 'bars' list continually appended to
        while(keep_going):
            _parameters['page_token'] = previous_data['next_page_token'] # update 'page_token' which signifies which page to gather 
            r = requests.get(BARS_URL, params=_parameters, headers=HEADERS) # make the api request
            previous_data = json.loads(r.content) # convert string to python dict
            appended_bars = master_data['bars'] + previous_data['bars'] # append the master 'bars' with newly gathered 'bars'
            master_data['bars'] = appended_bars # update bars in master object
            if (previous_data['next_page_token'] is None): keep_going = False # if there is no more to gather, end loop
        return master_data # return the master object
    
    def output_raw_data(self, raw_symbol_data, file_names):
        for i in range(len(file_names)):
            path = './raw_symbol_data/{}'.format(file_names[i]) # get path to output file
            io.writeToFile(path, "Date,Open,High,Low,Close,Volume") # write header to file
            self.write_json_to_csv(path, raw_symbol_data[i]['bars']) # write to file in raw_symbol_data folder
    
    def write_json_to_csv(self, path, bar_data):
        for bar in bar_data:
            f_date = bar['t'].split('T')[0] # remove time stamp from date
            formatted_data = '{},{},{},{},{},{}'.format(f_date, bar['o'], bar['h'], bar['l'], bar['c'], bar['v']) # convert dict to csv string
            io.appendToFile(path, formatted_data) # append to file
    
    def get_file_names(self, symbol_list):
        file_names = [] # empty list to hold all file names
        for symbol in symbol_list:
            date_start = DATE_START.split('T')[0]
            date_end = DATE_END.split('T')[0]
            file_name = '{}%{}%{}%{}.csv'.format(symbol, TIME_FRAME, date_start, date_end) # construct new file name
            file_names.append(file_name) # append new file name to list
        return file_names # return list of file names
    
    def run(self):
        file_names = self.get_file_names(SYMBOLS_TO_TEST) # get all filenames of output files
        valid_symbols = [] # this array will be filled with symbols that dont currently have a matching output file
        valid_file_names = [] # this array will hold all valid file names associated with each valid symbol
        for i in range(len(file_names)):
            if (io.fileExistsIn('./raw_symbol_data', file_names[i]) is False): # if file does not already exist..
                valid_symbols.append(SYMBOLS_TO_TEST[i]) # append to valid_symbols
                valid_file_names.append(file_names[i]) # append file_name to valid list
        raw_symbol_data = [] # empty list that will hold all gathered data
        for i in range(len(valid_symbols)): # for each symbol listed in config
            raw = self.get_symbol_data(valid_symbols[i]) # make api call for that symbol
            if (len(raw['bars']) == 0): 
                self.FULL_VALID_SYMBOLS.remove(valid_symbols[i]) # remove invalid symbol from master symbol list
                valid_file_names.remove(valid_file_names[i]) # also remove the file name associated with it
                continue # if the bars length is 0, symbol does not exist, skip this cycle
            if (raw['next_page_token'] is not None): # if there is more data to gether
                raw = self.get_remaining_data(valid_symbols[i], raw) # fetch remaining data until all is gathered
            else: 
                raw.pop('next_page_token') # remove 'next_page_token'
                raw.pop('symbol') # remove 'symbol' from raw
            raw_symbol_data.append(raw) # append raw symbol data to list
        if (len(raw_symbol_data) != 0): # if at least 1 symbol needed data gathered...
            self.output_raw_data(raw_symbol_data, valid_file_names) # output all data to files in raw_symbol_data folder
        return self.get_file_names(self.FULL_VALID_SYMBOLS) # return file_names for use in analysis module