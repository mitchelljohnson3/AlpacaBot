def simpleMovingAverageCrossover(data):
    if (data.crossesOver("MACD", "MACDSig")):
        data.buyAll()
    if (data.crossesOver("MACDSig", "MACD")):
        data.sellAll()