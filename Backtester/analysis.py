import sys
sys.path.append('../util') # make modules in util folder available
from global_config import * # import all global config variables
from backtest_config import * # import all backtest specific variables
import file_io as io # file_io lets us write and read to files

class analysis():
    def __init__(self, file_names):
        self.RAW_DATA_FILE_NAMES = file_names

    def run(self):
        print(self.RAW_DATA_FILE_NAMES)