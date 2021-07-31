from fetch import fetch # fetches raw symbol data
from analysis import analysis # calculates desired indicators
from backtest import backtest # performs a backtest using a strategy
from graphing import * # functions that allow graphing of analysis and backtest data
from strategies import * # strategy functions used for backtesting
import time # used to monitor code
import os # gives access to file system

#check if core directories are absent, and if so create them
analyzed_data_path = "./analyzed_data"
backtest_results_path = "./backtest_results"
raw_symbol_data_path = "./raw_symbol_data"
if ((os.path.isdir(analyzed_data_path)) is False): os.mkdir(analyzed_data_path)
if ((os.path.isdir(backtest_results_path)) is False): os.mkdir(backtest_results_path)
if ((os.path.isdir(raw_symbol_data_path)) is False): os.mkdir(raw_symbol_data_path)

# fetch raw symbol data
fetch_time_start = time.perf_counter()
fetchModule = fetch()
raw_data_file_names = fetchModule.run()
fetch_time_end = time.perf_counter()
diff = fetch_time_end - fetch_time_start
print(f"Fetched symbol data in {diff:0.1f} seconds.")

# analyze gathered data
analysis_time_start = time.perf_counter()
analysisModule = analysis(raw_data_file_names)
analyzed_data_file_names = analysisModule.run()
analysis_time_end = time.perf_counter()
diff = analysis_time_end - analysis_time_start
print(f"Analyzed symbol data in {diff:0.1f} seconds.")

# backtest strategy on analyzed data
backtest_time_start = time.perf_counter()
data = backtest(analyzed_data_file_names)
data.init()
while True:
    simpleMovingAverageCrossover(data) # run backtest strategy
    if(data.update() == False): break # exit loop once backtesting is complete
backtest_results_file_names = data.OUTPUT_FILE_NAMES
backtest_time_end = time.perf_counter()
diff = backtest_time_end - backtest_time_start
print(f"Backtested strategy in {diff:0.1f} seconds.")

# backtest results
# successful trade percentage
# total percent gain
# largest percent loss
# largest percent gain

# ask to graph analyzed data and results
displayGraphs = input("Graph analyzed data and results? [y/n]: ")
if (displayGraphs == "y"):
    graph(analyzed_data_file_names, backtest_results_file_names)