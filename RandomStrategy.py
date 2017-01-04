__author__ = 'rodrigowenceslau'

from decimal import Decimal, getcontext
import random
import numpy
from collections import OrderedDict
from itertools import izip

fileNamesCSVM1 = ['Var_BRKM5M1.csv', 'Var_CSNA3M1.csv', 'Var_EMBR3M1.csv', 'Var_GOLL4M1.csv', 'Var_JBSS3M1.csv',
                  'Var_PETR4M1.csv', 'Var_VALE5M1.csv']

fileNamesClose = ['CLOSE_BRKM5M1.csv', 'CLOSE_CSNA3M1.csv', 'CLOSE_EMBR3M1.csv', 'CLOSE_GOLL4M1.csv', 'CLOSE_JBSS3M1.csv',
                  'CLOSE_PETR4M1.csv', 'CLOSE_VALE5M1.csv']

USDVariations = []
with open('Var_DOL-1min.csv') as fileUSD:
    for line in fileUSD:
        USDVariations.append(Decimal(line[:-1]))
fileUSD.close()
#print USDVariations


stockVariations = []
stockClosingPrices = []
print 'RANDOM OPERATION STRATEGY'

indexFile = 0
for name in fileNamesCSVM1:
    with open(name) as fileVar, open(fileNamesClose[indexFile]) as fileClose:
        lineVar = fileVar.readline()
        lineVar = lineVar.split(",")
        correlation = Decimal(lineVar[0].replace("(", ""))

        for lineVar, lineClose in zip(fileVar, fileClose):
            stockVariations.append(Decimal(lineVar[:-1]))
            stockClosingPrices.append(Decimal(lineClose[:-1]))

    del stockVariations[0]
    del stockClosingPrices[0]

    hits = 0
    misses = 0
    noOp = 0
    initalCash = Decimal(100000)
    operationCash = Decimal(0.00)
    tradeOpCost = Decimal(0.00)
    stockNumber = Decimal(0)
    operationCounter = 0

    # STRATEGY BASED ON RANDOM BUY-SELL OPERATIONS TO SERVE AS A BASELINE
    for indexX, indexJ, indexZ in zip(range(len(USDVariations)), range(len(stockVariations)), range(len(stockClosingPrices))):
        USDVariation = USDVariations[indexX]
        stockVariation = stockVariations[indexJ]
        stockClosingPrice = stockClosingPrices[indexZ]
        #print USDVariation, stockVariation, stockClosingPrice
        Op = 100 * stockClosingPrice + tradeOpCost
        operation = random.randint(0, 1)                            # 1 = guessing up trend
                                                                    # 0 = guessing down trend
        if operation == 1 and USDVariation > 0:
            hits += 1
            if stockNumber >= 100:
                stockNumber -= 100
                initalCash += Op
                operationCash += Op
                operationCounter += 1

        if operation == 1 and USDVariation < 0:
            misses += 1
            if stockNumber >= 100:
                stockNumber -= 100
                initalCash += Op
                operationCash += Op
                operationCounter += 1

        if operation == 0 and USDVariation > 0:
            misses += 1
            if initalCash >= Op:
                stockNumber += 100
                initalCash -= Op
                operationCash -= Op
                operationCounter += 1

        if operation == 0 and USDVariation < 0:
            hits += 1
            if initalCash >= Op:
                stockNumber += 100
                initalCash -= Op
                operationCash -= Op
                operationCounter += 1

    if stockNumber > 0:
        initalCash += stockNumber * Op
        operationCash += stockNumber * Op
        operationCounter += 1

    total = hits + misses
    hitPercentage = float(hits)/float(total)
    missPercentage = float(misses)/float(total)
    noOpPercentage = float(noOp)/float(total)
    bruteEarnings = initalCash - Decimal(100000)
    #print hitPercentage
    name = name.replace("Var_", "")
    name = name.replace("M1.csv", "")

    print '\n', name
    print 'Hits: {} ({}%) '.format(hits, hitPercentage * 100)
    print 'Misses {} ({}%): '.format(misses, missPercentage * 100)
    print 'Final Balance: ', initalCash
    print 'Number of Operations Triggered: ', operationCounter
    print 'Profit per Operation: ', operationCash / operationCounter
    print 'Earnings: {} ({}%)'.format(bruteEarnings, bruteEarnings / Decimal(100000))

    indexFile += 1
    stockVariations = []
    stockClosingPrices = []
    fileVar.close()
    fileClose.close()