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
print 'BUY-AND-HOLD OPERATION STRATEGY'

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

    # STRATEGY BASED ON BUYING ON THE FIRST DAY AND SELLING ON THE LAST DAY OF THE PERIOD.
    initialOp = 100 * stockClosingPrices[0] + tradeOpCost
    stockNumber = initalCash / initialOp
    initalCash -= initialOp * stockNumber

    finalOp = 100 * stockClosingPrices[-1] + tradeOpCost

    if stockNumber > 0:
        initalCash += stockNumber * finalOp
        operationCash += stockNumber * finalOp

    name = name.replace("Var_", "")
    name = name.replace("M1.csv", "")

    bruteEarnings = initalCash - Decimal(100000)

    print '\n', name
    print 'Final Balance: ', initalCash
    print 'Earnings: {} ({}%)'.format(bruteEarnings, bruteEarnings / Decimal(100000))

    indexFile += 1
    stockVariations = []
    stockClosingPrices = []
    fileVar.close()
    fileClose.close()