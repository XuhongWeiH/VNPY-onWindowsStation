import os 
from dataclasses import dataclass
import csv, math
from datetime import datetime, time, timedelta
from tqdm import tqdm

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import database_manager
from vnpy.trader.object import TickData, BarData

@dataclass
class RQdataBarData(BarData):
    """
    1、期货的收盘价指的是期货交易时间结束时最后一笔合约的成交价格；
    期货的结算价是指某一期货合约当天的全部成交价按照总交易量的加权平均价，
    同时，收盘价是一个时间单位（天、小时、分钟）的最后成交价格，
    而结算价是指以一个交易日为时间单位的，最后15分钟或其它时间单位（有的品种结算时间不一样）的加权平均价。
    2、收盘价不是计算盈亏的依据，但对于评估当日市场环境和参与技术分析仍具有重要意义；
    结算价是交易所计算各账户盈亏，并划转资金的依据。
    在我国期货交易市场上，一般采用期货结算价制度，而不是使用收盘价作为实际交易价格。
    """
    exchange: str
    def __post_init__(self):
        """"""
        self.vt_symbol = f"{self.symbol}.{self.exchange}"

def run_load_csv():
    """
    遍历同一文件夹内所有csv文件，并且载入到数据库中
    """
    #!定义数量
    def csvNum(path):
        file_num = 0
        for root, dirs, files in os.walk(path, topdown=False):
            file_num += len(files)
        return file_num

    #!导入日线到数据库
    print("导入日线数据")
    # csv_root_path = "J:\Daily_csv"
    # pbar = tqdm(total=csvNum(csv_root_path))
    # for root, dirs, files in os.walk(csv_root_path, topdown=False):
    #     for name in files:
    #         file_path = os.path.join(root, name)
    #         pbar.update(1)
    #         if not file_path.endswith(".csv"): 
    #             continue
    #         pbar.set_description(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  ' ' + name)
    #         csv_load(file_path, name, 'd')
    # pbar.close()
    print("日线数据导入完成")

    print("导入分钟线数据")
    csv_root_path = "J:\Minute_csv"
    # pbar = tqdm(total=csvNum(csv_root_path))
    pbar = tqdm(total=1110703)
    qidong = False
    for root, dirs, files in os.walk(csv_root_path, topdown=False):
        try:
            symbol_filter = files[0].split('_')[0]
        except IndexError:
            continue
        if symbol_filter == "L2009": qidong = True #db.getCollection('db_bar_data').distinct( "symbol", {"interval":"1m"})
        if not qidong : 
            pbar.update(len(files))
            pbar.set_description(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  ' ' + symbol_filter)
            continue
        for name in files:
            file_path = os.path.join(root, name)
            pbar.update(1)
            if not file_path.endswith(".csv"): 
                continue
            pbar.set_description(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  ' ' + name)
            csv_load(file_path, name, '1m')
    pbar.close()
    print("分钟线数据导入完成")
       
    exit()

def csv_load(file, name, mode):
    """
    读取csv文件内容，并写入到数据库中    
    """
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        bars = []

        #* 提取文件名信息
        if mode == 'd':
            file_message = name.split('_')
            symbol = file_message[0]
            exchange = file_message[1]
            interval = Interval.DAILY
        
            for item in reader:
                try:
                    rqbar = RQdataBarData(
                    symbol=symbol,
                    datetime=datetime.strptime(item["date"], "%Y-%m-%d"),
                    exchange=exchange,
                    interval = interval,
                    volume=float(item["volume"]),
                    open_interest=float(item["open_interest"]),
                    open_price=float(item["open"]),
                    low_price=float(item["low"]),
                    high_price=float(item["high"]),
                    close_price=float(item["close"]),
                    total_turnover=float(item["total_turnover"]),
                    gateway_name="DB",       
                    )
                except ValueError:
                    rqbar = RQdataBarData(
                    symbol=symbol,
                    datetime=datetime.strptime(item["date"], "%Y-%m-%d"),
                    exchange=exchange,
                    interval = interval,
                    volume=float(item["volume"]),
                    open_interest=float(item["open_interest"]),
                    open_price=float(item["open"]),
                    low_price=float(item["low"]),
                    high_price=float(item["high"]),
                    close_price=float(item["close"]),
                    total_turnover=-1,
                    gateway_name="DB",       
                    )
                bars.append(rqbar)

            database_manager.save_bar_data(bars) 
        #****************************************************************#   
        elif mode == '1m' :
            file_message = name.split('_')
            symbol = file_message[0]
            exchange = file_message[1]
            interval = Interval.MINUTE
            for item in reader:
                try:
                    rqbar = RQdataBarData(
                    symbol=symbol,
                    datetime=datetime.strptime(item["datetime"], "%Y-%m-%d %H:%M:%S"),
                    exchange=exchange,
                    interval = interval,
                    volume=float(item["volume"]),
                    open_interest=float(item["open_interest"]),
                    open_price=float(item["open"]),
                    low_price=float(item["low"]),
                    high_price=float(item["high"]),
                    close_price=float(item["close"]),
                    total_turnover=float(item["total_turnover"]),
                    gateway_name="DB",       
                    )
                except ValueError:
                    rqbar = RQdataBarData(
                    symbol=symbol,
                    datetime=datetime.strptime(item["datetime"], "%Y-%m-%d %H:%M:%S"),
                    exchange=exchange,
                    interval = interval,
                    volume=float(item["volume"]),
                    open_interest=float(item["open_interest"]),
                    open_price=float(item["open"]),
                    low_price=float(item["low"]),
                    high_price=float(item["high"]),
                    close_price=float(item["close"]),
                    total_turnover=-1,
                    gateway_name="DB",       
                    )
                bars.append(rqbar)

            database_manager.save_bar_data(bars)

if __name__ == "__main__":
    run_load_csv()