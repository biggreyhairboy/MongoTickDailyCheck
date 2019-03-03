import json
from pymongo import MongoClient
from datetime import datetime, date, time


config = open('config.json')
setting = json.load(config)

MONGO_HOST = setting['MONGO_HOST']
MONGO_PORT = setting['MONGO_PORT']
tradingyear = setting['tradingyear']
tradingmonth = setting['tradingmonth']
tradingday = setting['tradingday']
symbol = setting['symbol']
trading_date = date(tradingyear, tradingmonth, tradingday)
# time section
night_start = time(21, 0)
night_end = time(23, 0)
morning_start = time(8, 57)
morning_end = time(11, 30)
afternoon_start = time(13, 30)
afternoon_end = time(15, 0)
# count section
night_count = 14400
morning_count = 16200
afternoon_count = 10800


def runcheck():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    tick_db = client['VnTrader_Tick_Db']
    tick_collection = tick_db[symbol]
    timedict = {"night": [night_start, night_end, night_count], \
                "morning": [morning_start, morning_end, morning_count],\
                "afternoon": [afternoon_start, afternoon_end, afternoon_count]}
    for timekey in timedict.keys():
        tstart = datetime.combine(trading_date, timedict[timekey][0])
        tend = datetime.combine(trading_date, timedict[timekey][1])
        # print(tstart)
        query_condition = {'datetime': {'$gte': tstart, '$lte': tend}}
        sessioncount = tick_collection.find(query_condition).count()
        print(sessioncount)
        if timedict[timekey][2] == sessioncount:
            print(timekey + " complete!")
        elif timedict[timekey][2] - 20 < sessioncount:
            print(timekey + " lose less than 20 ticks!")
        else:
            print(timekey + " not complete!")


if __name__ == '__main__':
    runcheck()
