from fetch import fetch # fetches raw symbol data
from analysis import analysis # calculates desired indicators
from backtest import backtest # performs a backtest using a strategy
from graphing import * # functions that allow graphing of analysis and backtest data
import time # used to monitor code

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
# backtestModule = backtest(analyzed_data_file_names)
backtest_results_file_names = []
backtest_time_end = time.perf_counter()
diff = backtest_time_end - backtest_time_start
print(f"Backtested strategy in {diff:0.1f} seconds.")

# backtest results
# successful trade percentage
# total percent gain
# largest percent loss
# largest percent gain

# ask to graph analysis data
displayAnalysisGraph = input("Graph analysis data? [y/n]: ")
if (displayAnalysisGraph == "y"):
    for filename in analyzed_data_file_names: 
        graph_a(filename)

# ask to graph backtest results
displayBacktestGraph = input("Graph backtest data? [y/n]: ")
if (displayBacktestGraph == "y"):graph_b(filename)