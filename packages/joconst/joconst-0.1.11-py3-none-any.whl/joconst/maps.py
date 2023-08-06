from joconst.constant import TdxMarket, Exchange, Interval
from jotdx.params import TDXParams

# 和下面 key 保持一致
TDX_JONPY_MARKET_MAP = {
    TdxMarket.DCE: Exchange.DCE,
    TdxMarket.SGE: Exchange.SGE,
    TdxMarket.CFFEX: Exchange.CFFEX,
    TdxMarket.SHFE: Exchange.SHFE,
    TdxMarket.CZCE: Exchange.CZCE,
}

JONPY_TDX_MARKET_MAP = {v: k for k, v in TDX_JONPY_MARKET_MAP.items()}

# vnpy 中的 constant 和 joconst 中的 Enum class 在 dict key 中被视为两个不同的东西
# 所以在 vnpy 中引入 joconst 替换原有的常量
INTERVAL_TDX_MAP = {
    Interval.MINUTE: TDXParams.KLINE_TYPE_1MIN,
    Interval.MINUTE_5: TDXParams.KLINE_TYPE_5MIN,
    Interval.MINUTE_15: TDXParams.KLINE_TYPE_15MIN,
    Interval.MINUTE_30: TDXParams.KLINE_TYPE_30MIN,
    Interval.HOUR: TDXParams.KLINE_TYPE_1HOUR,
    Interval.DAILY: TDXParams.KLINE_TYPE_DAILY,
    Interval.MONTHLY: TDXParams.KLINE_TYPE_MONTHLY,
    Interval.SEASONAL: TDXParams.KLINE_TYPE_3MONTH,
    Interval.YEARLY: TDXParams.KLINE_TYPE_YEARLY
}

TDX_INTERVAL_MAP = {v: k for k, v in INTERVAL_TDX_MAP.items()}

EXCHANGE_NAME_MAP = {
    Exchange.SHFE: "上海期货",
    Exchange.DCE: "大连商品",
    Exchange.CZCE: "郑州商品",
    Exchange.CFFEX: "中金所期货",
    Exchange.SGE: "上海黄金"
}

NAME_EXCHANGE_MAP = {v: k for k, v in EXCHANGE_NAME_MAP.items()}
