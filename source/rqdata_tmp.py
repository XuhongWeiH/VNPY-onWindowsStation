import rqdatac as rq
from rqdatac import *
rq.init('13381781395', 'w19940306')

futures.get_dominant('IF', '20160801')
"""
underlying_symbol	str	期货合约品种，例如沪深 300 股指期货为'IF'
start_date	str, datetime.date, datetime.datetime, pandasTimestamp	开始日期，默认为期货品种最早上市日期后一交易日
end_date	str, datetime.date, datetime.datetime, pandasTimestamp	结束日期，默认为当前日期
rule	int	默认是 rule=0,采用最大昨仓为当日主力合约，每个合约只能做一次主力合约，不会重复出现。针对股指期货，只在当月和次月选择主力合约。
当 rule=1 时，主力合约的选取只考虑最大昨仓这个条件。
rank	int	默认 rank=1。1-主力合约，2-次主力合约，3-次次主力合约。'2','3' 仅对 IC、IH、IF 合约，且 rule=1 时生效
"""
all_instruments_future = all_instruments(type='Future')
"""
all_instruments_future
     order_book_id underlying_symbol  market_tplus     symbol  margin_rate maturity_date    type trading_code exchange    product  contract_multiplier  round_lot                                    trading_hours listed_date industry_name de_listed_date underlying_order_book_id
0            A0303                 A           0.0     豆一0303         0.05    2003-03-14  Future        a0303      DCE  Commodity                 10.0        1.0  21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00  2002-03-15            油脂     2003-03-14                     null
1            A0309                 A           0.0     豆一0309         0.05    2003-09-12  Future        a0309      DCE  Commodity                 10.0        1.0  21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00  2002-05-22            油脂     2003-09-12                     null
2            A0311                 A           0.0     豆一0311         0.05    2003-11-14  Future        a0311      DCE  Commodity                 10.0        1.0  21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00  2002-05-22            油脂     2003-11-14                     null
3            A0305                 A           0.0     豆一0305         0.05    2003-05-23  Future        a0305      DCE  Commodity                 10.0        1.0  21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00  2002-03-15            油脂     2003-05-23                     null
4            A0307                 A           0.0     豆一0307         0.05    2003-07-14  Future        a0307      DCE  Commodity                 10.0        1.0  21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00  2002-03-15            油脂     2003-07-14                     null
...            ...               ...           ...        ...          ...           ...     ...          ...      ...        ...                  ...        ...                                              ...         ...           ...            ...                      ...
6491        PG2111                PG           0.0  液化石油气2111         0.11    2021-11-25  Future       pg2111      DCE  Commodity                 20.0        1.0  21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00  2020-11-26            未知     2021-11-25                     null


all_instruments_future.iloc[0]
order_book_id                                                         A0303
underlying_symbol                                                         A
market_tplus                                                              0
symbol                                                               豆一0303
margin_rate                                                            0.05
maturity_date                                                    2003-03-14
type                                                                 Future
trading_code                                                          a0303
exchange                                                                DCE
product                                                           Commodity
contract_multiplier                                                      10
round_lot                                                                 1
trading_hours               21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00
listed_date                                                      2002-03-15
industry_name                                                            油脂
de_listed_date                                                   2003-03-14
underlying_order_book_id                                               null

"""
instruments('A0303', market='cn')
"""
order_book_id	str	期货代码，期货的独特的标识符（郑商所期货合约数字部分进行了补齐。例如原有代码'ZC609'补齐之后变为'ZC1609'）。主力连续合约 UnderlyingSymbol+88，例如'IF88' ；指数连续合约命名规则为 UnderlyingSymbol+99
symbol	str	期货的简称，例如'沪深 1005'
margin_rate	float	期货合约的最低保证金率
round_lot	float	期货全部为 1.0
listed_date	str	期货的上市日期。主力连续合约与指数连续合约都为'0000-00-00'
type	str	合约类型，'Future'
contract_multiplier	float	合约乘数，例如沪深 300 股指期货的乘数为 300.0
underlying_order_book_id	str	合约标的代码，目前除股指期货(IH, IF, IC)之外的期货合约，这一字段全部为'null'
underlying_symbol	str	合约标的名称，例如 IF1005 的合约标的名称为'IF'
maturity_date	str	期货到期日。主力连续合约与指数连续合约都为'0000-00-00'
exchange	str	交易所，'DCE' - 大连商品交易所, 'SHFE' - 上海期货交易所，'CFFEX' - 中国金融期货交易所, 'CZCE'- 郑州商品交易所
trading_hours	str	合约交易时间
product	str	合约种类，'Commodity'-商品期货，'Index'-股指期货，'Government'-国债期货



Instrument(order_book_id='A0303', underlying_symbol='A', market_tplus=0, symbol='豆一0303', margin_rate=0.05, maturity_date='2003-03-14', type='Future', trading_code='a0303', exchange='DCE', product='Commodity', contract_multiplier=10.0, round_lot=1.0, trading_hours='21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00', listed_date='2002-03-15', industry_name='油脂', de_listed_date='2003-03-14', underlying_order_book_id='null')
special variables
function variables
citics_industry_code:None
citics_industry_name:None
concept_names:''
contract_multiplier:10.0
de_listed_date:'2003-03-14'
exchange:'DCE'
industry_name:'油脂'
listed_date:'2002-03-15'
margin_rate:0.05
market_tplus:0
maturity_date:'2003-03-14'
order_book_id:'A0303'
product:'Commodity'
round_lot:1.0
symbol:'豆一0303'
trading_code:'a0303'
trading_hours:'21:01-23:00,09:01-10:15,10:31-11:30,13:31-15:00'
type:'Future'
underlying_order_book_id:'null'
underlying_symbol:'A'
"""

get_price('A0303', start_date='2002-10-15', end_date='2002-10-20', frequency='1d', fields=None, adjust_type='pre', skip_suspended =False, market='cn', expect_df=False)
"""
order_book_ids	str OR str list	合约代码，可传入 order_book_id, order_book_id list
start_date	str, datetime.date, datetime.datetime, pandasTimestamp	开始日期
end_date	str, datetime.date, datetime.datetime, pandasTimestamp	结束日期
frequency	str	历史数据的频率。 现在支持周/日/分钟/tick 级别的历史数据，默认为'1d'。
1m - 分钟线
1d - 日线
1w - 周线，只支持'1w'
日线和分钟可选取不同频率，例如'5m'代表 5 分钟线。
fields	str OR str list	字段名称
adjust_type	str	权息修复方案，默认为pre。
不复权 - none，
前复权 - pre，后复权 - post，
前复权 - pre_volume, 后复权 - post_volume
两组前后复权方式仅 volume 字段处理不同，其他字段相同。其中'pre'、'post'中的 volume 采用拆分因子调整；'pre_volume'、'post_volume'中的 volume 采用复权因子调整。
skip_suspended	bool	是否跳过停牌数据。默认为 False，不跳过，用停牌前数据进行补齐。True 则为跳过停牌期。注意，当设置为 True 时，函数 order_book_id 只支持单个合约传入
expect_df	bool	默认返回原有的数据结构。如果调为真，则返回 pandas dataframe ,周线数据需设置 expect_df=True
market	str	默认是中国内地市场('cn') 。可选'cn' - 中国内地市场；
"""
"""
#               high  total_turnover     low    open  open_interest  limit_down  limit_up  volume  settlement   close  prev_settlement
# date                                                                                                                                
# 2002-10-15  2182.0      63282500.0  2176.0  2177.0        24828.0      2086.0    2259.0  2904.0      2179.0  2178.0           2172.0
# 2002-10-16  2201.0      88926200.0  2185.0  2185.0        24720.0      2092.0    2267.0  4052.0      2194.0  2198.0           2179.0
# 2002-10-17  2195.0     202898500.0  2181.0  2195.0        31088.0      2107.0    2282.0  9284.0      2185.0  2183.0           2194.0
# 2002-10-18  2194.0      46100900.0  2187.0  2187.0        31216.0      2098.0    2273.0  2104.0      2191.0  2191.0           2185.0
open	float	开盘价
close	float	收盘价
high	float	最高价
low	float	最低价
limit_up	float	涨停价
limit_down	float	跌停价
total_turnover	float	成交额
volume	float	成交量
num_trades	int	成交笔数 （仅限股票日线数据）
settlement	float	结算价 （仅限期货日线数据）
prev_settlement	float	昨日结算价（仅限期货日线数据）
open_interest	float	累计持仓量（期货专用）
trading_date	pandasTimeStamp	交易日期（仅限期货分钟线数据），对应期货夜盘的情况
dominant_id	str	实际合约的 order_book_id，对应期货 888 系主力连续合约的情况
strike_price	float	行权价，仅限 ETF 期权日线数据
contract_multiplier	float	合约乘数，仅限 ETF 期权日线数据
iopv	float	场内基金实时估算净值
"""