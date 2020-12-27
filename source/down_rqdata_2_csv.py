import os
import rqdatac as rq
from rqdatac import *
import pandas as pd
from tqdm import tqdm
from datetime import datetime,timedelta
import time
rq.init('13381781395', 'w19940306')

def getUserByteLimit(time_last = datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
    user_limit = rq.user.get_quota()
    while user_limit['bytes_used'] / user_limit['bytes_limit'] > 0.99:
        time.sleep(1)
        time_now = datetime.now()
        user_limit = rq.user.get_quota()
        print('\r' + '停止时间：' + time_last + ' ~ 当前时间： ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
              ' 已使用流量百分比：%.5f %% ' % (100 * user_limit['bytes_used'] / user_limit['bytes_limit']), end='', flush=True)
    return '已用流量： ' + '%.5f %%   ' % (100 * user_limit['bytes_used'] / user_limit['bytes_limit'])

print(getUserByteLimit())

all_instruments_future = all_instruments(type='Future')
all_instruments_future.to_csv("j:/all_instruments_future.csv")

# all_instruments_future = pd.DataFrame(pd.read_csv('j:/all_instruments_future.csv'))



trad = get_trading_dates(start_date='20030101', end_date='20201220')
t = lambda td:td.strftime("%Y-%m-%d")
for i in range(len(trad)):trad[i] = t(trad[i])
pd_trade_day=pd.DataFrame(columns=['trade_day'],data=trad)
pd_trade_day_list = pd_trade_day['trade_day'].to_list()
pd_trade_day.to_csv('j:/trade_day.csv')
# pd_trade_day = pd.DataFrame(pd.read_csv('j:/trade_day.csv'))

all_instruments_future_sub=all_instruments_future.drop_duplicates(subset=['underlying_symbol'], keep='first')
symbol_list = all_instruments_future_sub['underlying_symbol'].to_list()
trade_day_list = pd_trade_day['trade_day'].to_list()
symbol_domain_table = []

with tqdm(total=len(symbol_list)*len(trade_day_list)) as pbar:
    for symbol in symbol_list:
        for trade_day in trade_day_list:
            try:
                pbar.update(1)
                symbol_domain_table.append((trade_day, symbol, futures.get_dominant(symbol, trade_day).values[0]))
            except AttributeError:
                pass
pbar.close()
symbol_domain_df = pd.DataFrame(data = symbol_domain_table, columns=['trade_day', 'symbol', 'domain_contract'])
symbol_domain_df.to_csv("j:/domain_contract.csv")
# symbol_domain_df = pd.DataFrame(pd.read_csv("j:/domain_contract.csv"))



print("日线下载开始")
# # !日线下载

# pbar = tqdm(total=all_instruments_future.shape[0])
# for index, row in all_instruments_future.iterrows():
#     pbar.update(1)
#     underlying_symbol = row["underlying_symbol"]
#     order_book_id = row['order_book_id']
#     listed_date = row['listed_date']
#     de_listed_date = row['de_listed_date']
#     exchange  = row['exchange']

#     pbar.set_description(order_book_id + '_' + datetime.now().strftime("%Y-%m-%d") +  getUserByteLimit())

#     file_save_name = "J:/Daily_csv/" + underlying_symbol + '/' + '_'.join([order_book_id, exchange , listed_date, de_listed_date, "daily.csv"])
#     if os.path.exists(file_save_name):
#         continue
#     if row['listed_date'] == '0000-00-00':
#         data_daily = get_price(order_book_id, start_date='2003-01-01', end_date=datetime.now().strftime("%Y-%m-%d"))
#     else:
#         data_daily = get_price(order_book_id, start_date='2003-01-01', end_date=datetime.now().strftime("%Y-%m-%d"))
#     if not type(data_daily) == type(all_instruments_future) : continue
#     if not os.path.exists('J:/Daily_csv/' + underlying_symbol):
#         os.mkdir('J:/Daily_csv/' + underlying_symbol)
#     data_daily.to_csv(file_save_name)
# pbar.close()
print("日线下载完成")


print("分钟线下载")
# #!分钟线下载
# pbar = tqdm(total=all_instruments_future.shape[0])
# for index, row in all_instruments_future.iterrows():
#     pbar.update(1)
#     order_book_id = row['order_book_id']
#     exchange  = row['exchange']
#     underlying_symbol = row["underlying_symbol"]

#     if row['listed_date'] == '0000-00-00':  # row['listed_date'] == '0000-00-00'则为记录连续线
#         #?不下载连续分钟线
#         #continue

#         pbar.set_description(
#             order_book_id + '_' + datetime.now().strftime("%Y-%m-%d") + getUserByteLimit())
#         file_save_name = "J:/Minute_csv/" + '/'.join([underlying_symbol, order_book_id]) + '/' \
#                         + '_'.join([order_book_id, exchange, '0000-00-00', "minute.csv"])
        
#         if os.path.exists(file_save_name):
#             continue
#         data_minute = get_price(
#             order_book_id,
#             start_date='2010-01-01',
#             end_date=datetime.now().strftime("%Y-%m-%d"),
#             frequency='1m')
#         if not type(data_minute) == type(all_instruments_future):
#             continue
#         if not os.path.exists('J:/Minute_csv/' + '/'.join([underlying_symbol, order_book_id])):
#             os.makedirs('J:/Minute_csv/' +
#                         '/'.join([underlying_symbol, order_book_id]))
#         data_minute.to_csv(file_save_name)

#     else:
#         continue
#         listed_date = datetime.strptime(row['listed_date'], "%Y-%m-%d")
#         de_listed_date = datetime.strptime(row['de_listed_date'], "%Y-%m-%d")
#         tmp_date = listed_date
        
#         if de_listed_date < datetime.strptime('2010-01-05', "%Y-%m-%d") : continue

#         while tmp_date <= de_listed_date:
#             tmp_date = tmp_date + timedelta(days=1)
#             pbar.set_description(
#                 order_book_id + '_' + tmp_date.strftime("%Y-%m-%d") + getUserByteLimit())
#             file_save_name = "J:/Minute_csv/" + '/'.join([underlying_symbol, order_book_id]) + '/' +\
#                             '_'.join([order_book_id, exchange, tmp_date.strftime("%Y-%m-%d"), "minute.csv"])

#             if os.path.exists(file_save_name) or tmp_date < datetime.strptime('2010-01-05', "%Y-%m-%d"):
#                 continue
#             data_minute = get_price(
#                 order_book_id,
#                 start_date=tmp_date.strftime("%Y-%m-%d"),
#                 end_date=tmp_date.strftime("%Y-%m-%d"),
#                 frequency='1m')

#             if not type(data_minute) == type(all_instruments_future):
#                 continue
#             if not os.path.exists('J:/Minute_csv/' + '/'.join([underlying_symbol, order_book_id])):
#                 os.makedirs('J:/Minute_csv/' +
#                             '/'.join([underlying_symbol, order_book_id]))
#             data_minute.to_csv(file_save_name)

# pbar.close()
