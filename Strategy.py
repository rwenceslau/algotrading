from tables.tests.test_tables import updateRow

__author__ = 'rodrigowenceslau'

from decimal import Decimal, getcontext
import numpy
from collections import OrderedDict
from itertools import izip
fileNamesCSVM1 = ['Var_BRKM5M1.csv', 'Var_CSNA3M1.csv', 'Var_EMBR3M1.csv', 'Var_GOLL4M1.csv', 'Var_JBSS3M1.csv',
                  'Var_PETR4M1.csv', 'Var_VALE5M1.csv']

fileNamesClose = ['CLOSE_BRKM5M1.csv', 'CLOSE_CSNA3M1.csv', 'CLOSE_EMBR3M1.csv', 'CLOSE_GOLL4M1.csv', 'CLOSE_JBSS3M1.csv',
                  'CLOSE_PETR4M1.csv', 'CLOSE_VALE5M1.csv']

USDVariations = []

# READING USD VARIATIONS FILE
with open('Var_DOL-1min.csv') as fileUSD:
    for line in fileUSD:
        USDVariations.append(Decimal(line[:-1]))
fileUSD.close()

#----------------------------------------------------------------------------------------------------------------------#
# READING STOCK VARIATION FILES

stockVariations = []
stockClosingPrices = []
earningsList = []

indexFile = 0
for name in fileNamesCSVM1:
    print 'Writing EARNINGS file ...'
    fileEARNINGS = open('EARNINGS{}'.format(name.rstrip('.csv')), 'w')
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
    initalCash = Decimal(100000.00)
    tradeOpCost = Decimal(10.00)
    stockNumber = Decimal(0)
    previousMovement = Decimal(0.0)
    upCounter = 0
    downCounter = 0
    operationCounter = 0

    def operationThreshold(correlation):

        threshold = 0.0

        # Weaker positive correlation, which means the USD Variation needs to be higher in order to perform an operation.
        if 0.0 > correlation and correlation < 0.7:
            threshold = 0.045

        # Stronger positive correlation, which means even with small USD variations, the strategy can perform an operation.
        if correlation >= 0.7:
            threshold = 0.010

        # Weaker negative correlation, which means the USD Variation needs to be higher in order to perform an operation.
        if 0.0 < correlation and correlation > -0.7:
            threshold = 0.045

        # Stronger negative correlation, which means even with small USD variations, the strategy can perform an operation.
        if correlation <= -0.7:
            threshold = 0.010

        return threshold


    signalTolerance = 2
    threshold = operationThreshold(correlation)

    for indexX, indexJ, indexZ in zip(range(len(USDVariations)), range(len(stockVariations)), range(len(stockClosingPrices))):
        USDVariation = USDVariations[indexX]
        stockVariation = stockVariations[indexJ]
        stockClosingPrice = stockClosingPrices[indexZ]
        #print USDVariation, stockVariation, stockClosingPrice
        Op = 100 * stockClosingPrice + tradeOpCost

        if USDVariation > 0.0:
            if previousMovement > 0.0:
                upCounter += 1
            else:
                upCounter = 0

            if correlation > 0 and stockVariation > 0.0:
                if USDVariation >= threshold and stockNumber >= 100 and upCounter > signalTolerance: #SELL SIGNAL (POSITIVE CORREL - USD UP)
                    stockNumber -= 100
                    initalCash += Op
                    operationCounter += 1
                    hits += 1
            if correlation > 0 and stockVariation <= 0.0:
                if USDVariation >= threshold and stockNumber >= 100 and upCounter > signalTolerance: #SELL SIGNAL (POSITIVE CORREL - USD UP)
                    stockNumber -= 100
                    initalCash += Op
                    operationCounter += 1
                    misses += 1
            if correlation < 0 and stockVariation >= 0.0:
                if USDVariation >= threshold and initalCash >= Op and upCounter > signalTolerance: #BUY SIGNAL (NEGATIVE CORREL - USD UP)
                    stockNumber += 100
                    initalCash -= Op
                    operationCounter += 1
                    misses += 1
            if correlation < 0 and stockVariation < 0.0:
                if USDVariation >= threshold and initalCash >= Op and upCounter > signalTolerance: #BUY SIGNAL (NEGATIVE CORREL - USD UP)
                    stockNumber += 100
                    initalCash -= Op
                    operationCounter += 1
                    hits += 1

        if USDVariation < 0.0:
            if previousMovement < 0.0:
                downCounter += 1
            else:
                downCounter = 0

            if correlation > 0 and stockVariation < 0.0:
                if USDVariation <= threshold * -1 and initalCash >= Op and downCounter > signalTolerance: #BUY SIGNAL (NEGATIVE CORREL - USD DOWN)
                    stockNumber += 100
                    initalCash -= Op
                    operationCounter += 1
                    hits += 1
            if correlation > 0 and stockVariation >= 0.0:
                if USDVariation <= threshold * -1 and initalCash >= Op and downCounter > signalTolerance: #BUY SIGNAL (NEGATIVE CORREL - USD DOWN)
                    stockNumber += 100
                    initalCash -= Op
                    operationCounter += 1
                    misses += 1
            if correlation < 0 and stockVariation <= 0.0:
                if USDVariation <= threshold * -1 and stockNumber >= 100 and downCounter > signalTolerance: #SELL SIGNAL (POSITIVE CORREL - USD DOWN)
                    stockNumber -= 100
                    initalCash += Op
                    operationCounter += 1
                    misses += 1
            if correlation < 0 and stockVariation > 0.0:
                if USDVariation <= threshold * -1 and stockNumber >= 100 and downCounter > signalTolerance: #SELL SIGNAL (POSITIVE CORREL - USD DOWN)
                    stockNumber -= 100
                    initalCash += Op
                    operationCounter += 1
                    hits += 1

        if USDVariation == 0.0:
            if stockVariation == 0.0:
                hits += 1
            else:
                misses += 1
        #print stockNumber, initalCash
        previousMovement = USDVariation
        earnings = stockNumber * Op
        earningsList.append(earnings)

    if stockNumber > 0:
        initalCash += stockNumber * Op

    floatData = [float(x) for x in earningsList]
    npEarnings = numpy.array(floatData)

    total = hits + misses
    hitPercentage = float(hits)/float(total)
    missPercentage = float(misses)/float(total)
    noOpPercentage = float(noOp)/float(total)
    bruteEarnings = initalCash - Decimal(100000)

    name = name.replace("Var_", "")
    name = name.replace("M1.csv", "")

    print '\n', name
    print 'NAIVE CORRELATION-BASED STRATEGY'
    print 'Threshold Used:', threshold
    print 'Correlation: ', correlation
    print 'Hits: {} ({}%) '.format(hits, hitPercentage * 100)
    print 'Misses {} ({}%): '.format(misses, missPercentage * 100)
    print 'Final Balance: ', initalCash
    print 'Number of Operations Triggered: ', operationCounter
    print 'Profit per Operation: ', initalCash / operationCounter
    print 'Earnings: {} ({}%)'.format(bruteEarnings, bruteEarnings / Decimal(100000))
    print npEarnings
    print 'Earning MAX:', numpy.max(npEarnings)
    print 'Earning MIN:', numpy.min(npEarnings[numpy.nonzero(npEarnings)])


    indexFile += 1
    stockVariations = []
    stockClosingPrices = []
    fileVar.close()
    fileClose.close()
    fileEARNINGS.close()
    earningsList = []