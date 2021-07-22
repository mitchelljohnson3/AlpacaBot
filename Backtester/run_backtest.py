from fetch import fetch
from analysis import analysis
from backtest import backtest

fetchModule = fetch()
raw_data_file_names = fetchModule.run()

analysisModule = analysis(raw_data_file_names)
analyzed_data_file_names = analysisModule.run()