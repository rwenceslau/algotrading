__author__ = 'rodrigowenceslau'
import numpy
import talib
from scipy.stats.stats import pearsonr
from decimal import Decimal, getcontext

# codigo,fechamento_atual,abertura,maximo,minimo,fechamento_anterior,negocios,quantidade_papeis,volume_financeiro,datahora'

fileNames = ['EMBR3_PDM.txt', 'GOLL4_PDM.txt', 'JBSS3.txt', 'VALE3_PDM.txt', 'PETR4_PDM.txt', 'BRKM5.txt', 'CSNA3.txt']
fileNamesCSVM1 = ['EMBR3M1.csv', 'GOLL4M1.csv', 'JBSS3M1.csv', 'VALE5M1.csv', 'PETR4M1.csv', 'BRKM5M1.csv', 'CSNA3M1.csv']
fileNamesCSVDaily = ['EMBR3Daily.csv', 'GOLL4Daily.csv', 'JBSS3Daily.csv', 'VALE3Daily.csv', 'PETR4Daily.csv', 'BRKM5Daily.csv', 'CSNA3Daily.csv', 'IBOVDaily.csv']
nonWorkingDays = ['20151102', '20151012', '20150907', '20150709', '20150604', '20150501', '20150421', '20150403', '20150217', '20150216', '20150101', '20141231',
                  '20141225', '20141224', '20141120', '20140709', '20140619', '20140612', '20140501', '20140421', '20140418', '20140304', '20140303', '20140101',
                  '20131231', '20131225', '20131224', '20131120', '20131115', '20130709', '20130530', '20130501', '20130329', '20130212', '20130211', '20130125',
                  '20130101', '20121231', '20121225', '20121224', '20121120', '20121115', '20121102', '20121012', '20120907', '20120709', '20120607', '20120501',
                  '20120406', '20120221', '20120220', '20120125', '20111230', '20111115', '20111102', '20111012', '20110907', '20110623', '20110422', '20110421',
                  '20110308', '20110307', '20110125', '20101231', '20101224', '20101115', '20101102', '20101012', '20100907', '20100709', '20100603', '20100421',
                  '20100402', '20100216', '20100215', '20100125']

stockMax = {}
stockMin = {}
stockTick = {}
stockVol = {}
stockTimestampCheck = []
usPrice = {}
usTick = {}
closingPricesUSD = []
closingPrices = []
closingPricesUSDTemp = []
bovPrice = {}
bovTick = {}
closingPricesBOV = []
closingPricesBOVTemp = []

# READING AND CALCULATING INDICATORS FROM USD-BRL
#----------------------------------------------------------------------------------------------------------------------
# numberOfLines = 0
#
# name = 'CURRFX-USDBRL.csv'
# with open(name) as file:
#         next(file)
#         for line in file:
#             numberOfLines += 1
#             if numberOfLines < 1530:
#                 line = line.split(',')
#                 timestamp = line[0].translate(None, '-')
#                 if not (timestamp in nonWorkingDays):
#                     stockTimestampCheck.append(timestamp)
#                     if line[1] != '\r\n' and line[1] != '0.0':
#                         keyPrice = float(line[1])
#                         usPrice[timestamp] = keyPrice
#                         closingPricesUSD.append(keyPrice)
#
# closingPricesUSD = closingPricesUSD[::-1]
#
# ant = closingPricesUSD[0]
# keyVariation = 0
# for x in closingPricesUSD:
#     keyVariation = x - ant
#     if keyVariation < 0:
#         keyVariation = abs(keyVariation)/ant
#         keyVariation *= -1
#         keyVariation *= 100
#     else:
#         keyVariation /= ant
#         keyVariation *= 100
#     usTick[keyVariation] = ant, x
#     ant = x
#
# floatData = [float(x) for x in closingPricesUSD]
# npFloatDataTickUSD = numpy.array(floatData)
# npSMA = talib.SMA(npFloatDataTickUSD, timeperiod=120)  # Using the 12-day span since it's one of the most common.
# npAVG = talib.EMA(npFloatDataTickUSD, timeperiod=120)  #
# npBBANDS = talib.BBANDS(npFloatDataTickUSD, timeperiod=120)
#
# # print 'SMA: ', npSMA
# # print 'EMA: ', npAVG
# # print 'BBANDS_UPPER: ', npBBANDS[0]
# # print 'BBANDS_MID: ', npBBANDS[1]
# # print 'BBANDS_LOWER: ', npBBANDS[2]
#
# maxVariation = max(usTick.keys())
# minVariation = min(usTick.keys())
# maxPrice = max(usPrice.values())
# minPrice = min(usPrice.values())
# avgVariation = sum(usTick.keys())/float(len(usTick.keys()))
#
# upTrend = 0
# downTrend = 0
#
# for variation in usTick.keys():
#     if variation > 0.1:
#         upTrend += 1
#     else:
#         downTrend += 1
#
# print '\n'
# print name.rstrip('.txt')
# print 'Max:', maxPrice, 'on',  usPrice.keys()[usPrice.values().index(maxPrice)]
# print 'Min:', minPrice, 'on', usPrice.keys()[usPrice.values().index(minPrice)]
# print 'Max Variation (Up):', maxVariation, '% on', usTick[maxVariation]
# print 'Max Variation (Down):', minVariation, '% on', usTick[minVariation]
# print 'Avg Variation:', avgVariation
# print 'Number of Up Trends: ', upTrend
# print 'Number of Down Trends: ', downTrend
# print 'Number of Stable Positions: ', abs(downTrend-upTrend)
# print '# of candles: ', len(closingPricesUSD)
#
# print 'Writing SMA file ...'
# fileSMA = open('SMA_{}'.format(name.rstrip('.csv')), 'w')
# for x in npSMA:
#     fileSMA.write('{}\n'.format(x))
# fileSMA.close()
#
# print 'Writing EMA file ...'
# fileEMA = open('EMA_{}'.format(name.rstrip('.csv')), 'w')
# for x in npAVG:
#     fileEMA.write('{}\n'.format(x))
# fileEMA.close()
#
# print 'Writing BBANDS file ...'
# fileBBANDS = open('BBANDS_{}'.format(name.rstrip('.csv')), 'w')
# for x, y, z in zip(npBBANDS[0], npBBANDS[1], npBBANDS[2]):
#     fileBBANDS.write('{} {} {}\n'.format(x, y, z))
# fileBBANDS.close()
#
# print 'Writing CLOSE file ...'
# fileCLOSE = open('CLOSE_{}'.format(name.rstrip('.csv')), 'w')
# for x in closingPricesUSD:                  # Had to print the list in reverse order since the original table if from
#      fileCLOSE.write('{}\n'.format(x))      # the newest to older value.
# fileCLOSE.close()
#
# correlation = pearsonr(closingPricesUSD, closingPricesUSD)
# print 'Pearson Correlation Value: ', correlation

# READING USD FILE 1 MIN

usMax = {}
usMin = {}
name = 'DOL-1min.csv'
with open(name) as file:
        for line in file:
            line = line.split(',')
            #print line
            timestamp = line[1].replace("-", ".")
            timestamp = timestamp[:-3]
            keyMax = float(line[3])
            keyMin = float(line[4])
            openPrice = float(Decimal(line[2]))
            closingPrice = float(Decimal(line[5]))
            keyVariation = closingPrice - openPrice
            #print keyVariation
            closingPricesUSD.append(closingPrice)
            if keyVariation < 0:
                keyVariation = abs(keyVariation)/openPrice
                keyVariation *= -1
                keyVariation *= 100
            else:
                keyVariation /= openPrice
                keyVariation *= 100
            #print keyVariation
            usMax[timestamp] = keyMax
            usMin[timestamp] = keyMin
            usTick[timestamp] = keyVariation, openPrice, closingPrice
file.close()

USDvariationList = [value[0] for value in usTick.values()]
maxPrice = max(usMax.values())
minPrice = min(usMin.values())
maxVariation = max(USDvariationList)
minVariation = min(USDvariationList)
avgVariation = sum(USDvariationList)/float(len(USDvariationList))
upTrend = 0
nonUpTrend = 0

floatData = [float(x) for x in closingPricesUSD]
npFloatDataTickUSD = numpy.array(floatData)
npSMA = talib.SMA(npFloatDataTickUSD, timeperiod=120)  # Using the 12-day span since it's one of the most common.
npAVG = talib.EMA(npFloatDataTickUSD, timeperiod=120)  #
npBBANDS = talib.BBANDS(npFloatDataTickUSD, timeperiod=120)

bovMax = {}
bovMin = {}
name = 'IBOVM1.csv'
with open(name) as file:
        for line in file:
            line = line.split(',')
            #print line
            timestamp = line[0]
            keyMax = float(line[2])
            keyMin = float(line[3])
            closingPrice = float(line[4])
            openPrice = float(line[1])
            keyVariation = closingPrice - openPrice
            #print keyVariation
            closingPricesBOV.append(closingPrice)
            if keyVariation < 0:
                keyVariation = abs(keyVariation)/openPrice
                keyVariation *= -1
                keyVariation *= 100
            else:
                keyVariation /= openPrice
                keyVariation *= 100
            #print keyVariation
            bovMax[timestamp] = keyMax
            bovMin[timestamp] = keyMin
            bovTick[timestamp] = keyVariation, openPrice, closingPrice
file.close()

BOVvariationList = [value[0] for value in bovTick.values()]
maxPrice = max(bovMax.values())
minPrice = min(bovMin.values())
maxVariation = max(BOVvariationList)
minVariation = min(BOVvariationList)
avgVariation = sum(BOVvariationList)/ float(len(BOVvariationList))
upTrend = 0
nonUpTrend = 0


for variation in BOVvariationList:
    if variation > 0.0:
        upTrend += 1
    else:
        nonUpTrend += 1

print '\n'
print name.rstrip('.csv')
print 'Max:', maxPrice, 'on', bovMax.keys()[bovMax.values().index(maxPrice)]
print 'Min:', minPrice, 'on', bovMin.keys()[bovMin.values().index(minPrice)]
print 'Avg Variation: {} %'.format(avgVariation)
print 'Number of Up Trends: ', upTrend
print 'Number of Non-Up Trends: ', nonUpTrend
print 'Number of Ticks: ', len(bovTick.keys())

floatData = [float(x) for x in closingPricesBOV]
npFloatDataTickBOV = numpy.array(floatData)
npSMA = talib.SMA(npFloatDataTickBOV, timeperiod=3000)  # Using the 12-period span since it's one of the most common.
npAVG = talib.EMA(npFloatDataTickBOV, timeperiod=3000)
npBBANDS = talib.BBANDS(npFloatDataTickBOV, timeperiod=3000)
print numpy.mean(npFloatDataTickBOV)

print npFloatDataTickUSD.size
npFloatDataTickBOV.resize(npFloatDataTickUSD.size)
print npFloatDataTickBOV.size
covariance = numpy.cov(npFloatDataTickBOV, npFloatDataTickUSD)
print covariance

print 'Writing CLOSE file ...'
fileCLOSE = open('CLOSE_{}'.format(name.rstrip('.csv')), 'w')
for x in closingPricesUSD:
    fileCLOSE.write('{}\n'.format(x))
fileCLOSE.close()
#
# print 'Writing SMA file ...'
# fileSMA = open('SMA_{}'.format(name.rstrip('.csv')), 'w')
# for x in npSMA:
#     fileSMA.write('{}\n'.format(x))
# fileSMA.close()
#
# print 'Writing EMA file ...'
# fileEMA = open('EMA_{}'.format(name.rstrip('.csv')), 'w')
# for x in npAVG:
#     fileEMA.write('{}\n'.format(x))
# fileEMA.close()
#
# print 'Writing BBANDS file ...'
# fileBBANDS = open('BBANDS_{}'.format(name.rstrip('.csv')), 'w')
# for x, y, z in zip(npBBANDS[0], npBBANDS[1], npBBANDS[2]):
#     fileBBANDS.write('{} {} {}\n'.format(x, y, z))
# fileBBANDS.close()

print 'Writing Variation file ...'
fileCLOSE = open('Var_{}'.format(name.rstrip('.csv')), 'w')
for x in USDvariationList:
    fileCLOSE.write('{}\n'.format(x))
fileCLOSE.close()

#----------------------------------------------------------------------------------------------------------------------

# READING AND CALCULATING INDICATORS FROM STOCKS
#----------------------------------------------------------------------------------------------------------------------

# for name in fileNames:
#     with open(name) as file:
#         for line in file:
#             #print line
#             line = line.split(',')
#             keyMax = float(line[3])
#             keyMin = float(line[4])
#             closingPrice = float(line[1])
#             openPrice = float(line[2])
#             keyVariation = closingPrice - openPrice
#             closingPrices.append(closingPrice)
#
#             if keyVariation < 0:
#                 keyVariation = abs(keyVariation)/openPrice
#                 keyVariation *= -1
#                 keyVariation *= 100
#             else:
#                 keyVariation /= openPrice
#                 keyVariation *= 100
#
#             keyVol = float(line[8])
#             timestamp = line[9].rstrip('\n')
#             stockMax[timestamp] = keyMax
#             stockMin[timestamp] = keyMin
#             stockTick[keyVariation] = timestamp, openPrice, closingPrice
#             stockVol[timestamp] = keyVol
#     file.close()

numberOfCandles = 0
for name in fileNamesCSVM1:
    with open(name) as file:
        for line in file:
            #print line
            line = line.split(',')
            timestamp = line[0]
            #print 'Checking TS ', timestamp
            if "2015" in timestamp:
                if timestamp in usTick.keys():
                    priceUSD = usTick[timestamp][2]                # Getting the closing price from usTick dict
                    closingPricesUSDTemp.append(priceUSD)
                    #print 'TS hit'
                    keyMax = float(line[2])
                    keyMin = float(line[3])
                    closingPrice = float(line[4])
                    openPrice = float(line[1])
                    keyVariation = closingPrice - openPrice
                    closingPrices.append(closingPrice)
                    if keyVariation < 0:
                        keyVariation = abs(keyVariation)/openPrice
                        keyVariation *= -1
                        keyVariation *= 100
                    else:
                        keyVariation /= openPrice
                        keyVariation *= 100

                    keyVol = float(line[6])
                    stockMax[timestamp] = keyMax
                    stockMin[timestamp] = keyMin
                    stockTick[timestamp] = keyVariation, openPrice, closingPrice
                    stockVol[timestamp] = keyVol
    file.close()

    variationList = [value[0] for value in stockTick.values()]

    maxPrice = max(stockMax.values())
    minPrice = min(stockMin.values())
    maxVariation = max(variationList)
    minVariation = min(variationList)
    maxVol = max(stockVol.values())
    minVol = min(stockVol.values())
    avgVariation = sum(variationList)/float(len(variationList))

    upTrend = 0
    nonUpTrend = 0
    for variation in variationList:
        if variation > 0.0:
            upTrend += 1
        else:
            nonUpTrend += 1

    print '\n'
    print name.rstrip('.csv')
    print 'Max:', maxPrice, 'on',  stockMax.keys()[stockMax.values().index(maxPrice)]
    print 'Min:', minPrice, 'on', stockMin.keys()[stockMin.values().index(minPrice)]
    print 'Max Volume:', maxVol, 'M on',  stockVol.keys()[stockVol.values().index(maxVol)]
    print 'Min Volume:', minVol, 'M on', stockVol.keys()[stockVol.values().index(minVol)]
    print 'Max Variation (Up):', maxVariation
    print 'Max Variation (Down):', minVariation
    print 'Avg Variation: {} %'.format(avgVariation)
    print 'Number of Up Trends: ', upTrend
    print 'Number of Non-Up Trends: ', nonUpTrend

    floatData = [float(x) for x in closingPrices]
    npFloatDataTick = numpy.array(floatData)

    floatDataUSD = [float(x) for x in closingPricesUSDTemp]
    npFloatDataTickUSD = numpy.array(floatDataUSD)

    npSMA = talib.SMA(npFloatDataTick, timeperiod=3000)  # Using the 12-period span since it's one of the most common.
    npAVG = talib.EMA(npFloatDataTick, timeperiod=3000)  #
    npBBANDS = talib.BBANDS(npFloatDataTick, timeperiod=3000)

    #npSMA = talib.SMA(npFloatDataUSDollar, 12)  # Using the 12-day span since it's one of the most common.
    #npAVG = talib.EMA(npFloatDataUSDollar, 12)  #
    print '# of Ticks: ', len(variationList)
    #npCORREL = talib.CORREL(npFloatDataTick, npFloatDataTickUSD)

    meansUSD = numpy.mean(npFloatDataTickUSD, dtype=numpy.float64)
    meansStock = numpy.mean(npFloatDataTick, dtype=numpy.float64)
    covariance = numpy.cov(npFloatDataTickUSD, npFloatDataTick)

    print 'Writing Means file ...'
    fileMeans = open('MeansUSD_{}'.format(name.rstrip('.csv')), 'w')
    fileMeans.write('{}\n'.format(meansUSD))
    fileMeans.write('{}\n'.format(meansStock))
    fileMeans.close()

    print 'Writing Covariance file ...'
    fileMeans = open('CovarianceUSD_{}'.format(name.rstrip('.csv')), 'w')
    fileMeans.write('{}\n'.format(covariance))
    fileMeans.close()

    correlation = pearsonr(closingPrices, closingPricesUSDTemp)
    print 'Pearson Correlation Value: ', correlation

    # print 'SMA: ', npSMA
    # print 'EMA: ', npAVG
    # print 'BBANDS_UPPER: ', npBBANDS[0]
    # print 'BBANDS_MID: ', npBBANDS[1]
    # print 'BBANDS_LOWER: ', npBBANDS[2]
    # print 'MAX: ', talib.MAX(npFloatDataTick)
    # print 'MIN: ', talib.MIN(npFloatDataTick)
    floatData = [float(x) for x in stockMax.values()]
    npFloatDataMax = numpy.array(floatData)

    floatData = [float(x) for x in stockMin.values()]
    npFloatDataMin = numpy.array(floatData)


    # print 'Writing SMA file ...'
    # fileSMA = open('SMA_{}'.format(name.rstrip('.txt')), 'w')
    # for x in npSMA:
    #     fileSMA.write('{}\n'.format(x))
    # fileSMA.close()
    #
    # print 'Writing EMA file ...'
    # fileEMA = open('EMA_{}'.format(name.rstrip('.txt')), 'w')
    # for x in npAVG:
    #     fileEMA.write('{}\n'.format(x))
    # fileEMA.close()
    #
    # bbands = numpy.vstack((npBBANDS[0], npBBANDS[1], npBBANDS[2]))
    #
    # print 'Writing BBANDS file ...'
    # fileBBANDS = open('BBANDS_{}'.format(name.rstrip('.txt')), 'w')
    # for x, y, z in zip(npBBANDS[0], npBBANDS[1], npBBANDS[2]):
    #     fileBBANDS.write('{} {} {}\n'.format(x, y, z))
    # fileBBANDS.close()
    #
    print 'Writing CLOSE file ...'
    fileCLOSE = open('CLOSE_{}'.format(name.rstrip('.csv')), 'w')
    for x in closingPrices:
        fileCLOSE.write('{}\n'.format(x))
    fileCLOSE.close()

    # SCENARIO DEFINITION AND RESULTS GENERATION FOR PERIOD #

    print 'Writing Variation file ...'
    fileVar = open('Var_{}'.format(name.rstrip('.csv')), 'w')
    fileVar.write('{}\n'.format(correlation))
    for x in variationList:
        fileVar.write('{}\n'.format(x))
    fileVar.close()

    # hits = 0
    # misses = 0
    # noOp = 0
    #
    # for indexX, indexJ in zip(range(len(USDvariationList)), range(len(variationList))):
    #     if USDvariationList[indexX] > 0.0:           # USD up
    #         if correlation > 0.0:                   # Positive correlation
    #             if variationList[indexJ] > 0.0:      # Will guess an up trend in stock value
    #                 hits += 1
    #         else:                                   # Negative correlation
    #             if variationList[indexJ] < 0.0:      # Will guess an down trend in stock value
    #                 hits += 1
    #     else:                                       # USD down
    #         if correlation > 0.0:                   # Positive correlation
    #             if variationList[indexJ] < 0.0:      # Will guess an down trend in stock value
    #                 hits += 1
    #         else:                                   # Negative correlation
    #             if variationList[indexJ] > 0.0:      # Will guess an up trend in stock value
    #                 hits += 1
    #     if USDvariationList[indexX] == 0.0:
    #         noOp += 1
    #
    # print 'Hits: ', hits
    # print 'No Operation: ', noOp
    # print 'Misses: ', abs(len(USDvariationList) - (hits + noOp))


    stockMax.clear()
    stockMin.clear()
    stockTick.clear()
    stockVol.clear()
    closingPrices = []
    closingPricesUSDTemp = []
    variationList = []
    npAVG = []
    npSMA = []

#----------------------------------------------------------------------------------------------------------------------