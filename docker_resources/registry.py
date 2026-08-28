"""Custom registry extension — 在官方 VENDOR_CLASSES_BY_TYPE 基础上注入 eltdx vendor。

容器内 PYTHONPATH 需包含 /tmp/eltdx_install（由 start_eltdx.sh 设置）
"""

from __future__ import annotations

from marketdata.vendors.capital_flow import EastmoneyCapitalFlowVendor, SinaCapitalFlowVendor
from marketdata.vendors.tencent_fundflow import TencentFundflowVendor
from marketdata.vendors.ths_flow import ThsBoardFlowVendor, ThsMarketFlowVendor
from marketdata.vendors.ths_web import (
    ThsFlashNewsVendor,
    ThsFundamentalsVendor,
    ThsKlineVendor,
    ThsQuoteVendor,
)
from marketdata.vendors.eastmoney import EastmoneyQuoteVendor
from marketdata.vendors.events import EventsVendor
from marketdata.vendors.fundamentals import EastmoneyFundamentalsVendor, TencentFundamentalsVendor
from marketdata.vendors.flash_news import (
    ClsFlashNewsVendor,
    EastmoneyFlashNewsVendor,
    SinaFlashNewsVendor,
)
from marketdata.vendors.kline import (
    EastmoneyKlineVendor,
    StooqKlineVendor,
    TencentKlineVendor,
    YahooKlineVendor,
)
from marketdata.vendors.market_flow import (
    EastmoneyDividendVendor,
    EastmoneyDragonTigerVendor,
    EastmoneyMarginVendor,
    EastmoneyShareholdersVendor,
)
from marketdata.vendors.ftshare import FtshareDragonTigerVendor, FtshareMarginVendor
from marketdata.vendors.zhitu import ZhituDividendVendor
from marketdata.vendors.zhitu_full import (
    ZhituKlineVendor,
    ZhituShareholdersVendor,
    ZhituFundamentalsVendor,
)
from marketdata.vendors.news import (
    EastmoneyAnnNewsVendor,
    EastmoneyStockNewsVendor,
    XueqiuNewsVendor,
)
from marketdata.vendors.northbound import HexinNorthboundVendor
from marketdata.vendors.sina import SinaQuoteVendor
from marketdata.vendors.tencent import TencentQuoteVendor
from marketdata.vendors.tq import TqKlineVendor, TqMoreInfoVendor, TqQuoteVendor
from marketdata.vendors.yfinance import YFinanceQuoteVendor
from marketdata.vendors.alphavantage import AlphaVantageQuoteVendor
from marketdata.vendors.twelvedata import TwelveDataQuoteVendor

# ⭐ 注入 eltdx vendor（分步导入避免循环依赖）
try:
    from eltdx.sida_adapter import EltdxKlineVendor
    from eltdx.sida_adapter import EltdxMoreInfoVendor
    from eltdx.sida_adapter import EltdxQuoteVendor
    _ELTDX_OK = True
    print(f"[eltdx] ✅ eltdx vendor 加载成功, supports_markets={EltdxQuoteVendor.supports_markets}", flush=True)
except Exception as _e:
    _ELTDX_OK = False
    print(f"[eltdx] ⚠️ eltdx vendor 不可用: {_e}", flush=True)


# 各数据类型 → {vendor name: vendor 类}
VENDOR_CLASSES_BY_TYPE: dict[str, dict[str, type]] = {
    "quote": {
        "tq": TqQuoteVendor,
        "tencent": TencentQuoteVendor,
        "sina": SinaQuoteVendor,
        "eastmoney": EastmoneyQuoteVendor,
        "yfinance": YFinanceQuoteVendor,
        "alphavantage": AlphaVantageQuoteVendor,
        "twelvedata": TwelveDataQuoteVendor,
        "ths": ThsQuoteVendor,
    },
    "kline": {
        "tq": TqKlineVendor,
        "zhitu": ZhituKlineVendor,
        "tencent": TencentKlineVendor,
        "stooq": StooqKlineVendor,
        "eastmoney": EastmoneyKlineVendor,
        "yahoo": YahooKlineVendor,
        "ths": ThsKlineVendor,
    },
    "capital_flow": {
        "eastmoney": EastmoneyCapitalFlowVendor,
        "sina": SinaCapitalFlowVendor,
        "tencent": TencentFundflowVendor,
    },
    "board_capital_flow": {
        "ths_flow": ThsBoardFlowVendor,
    },
    "market_capital_flow": {
        "ths_market_flow": ThsMarketFlowVendor,
    },
    "events": {
        "eastmoney": EventsVendor,
    },
    "fundamentals": {
        "zhitu": ZhituFundamentalsVendor,
        "tencent": TencentFundamentalsVendor,
        "eastmoney": EastmoneyFundamentalsVendor,
        "ths_f10": ThsFundamentalsVendor,
    },
    "flash_news": {
        "cls": ClsFlashNewsVendor,
        "sina": SinaFlashNewsVendor,
        "eastmoney": EastmoneyFlashNewsVendor,
        "ths": ThsFlashNewsVendor,
    },
    "news": {
        "xueqiu": XueqiuNewsVendor,
        "eastmoney_news": EastmoneyStockNewsVendor,
        "eastmoney": EastmoneyAnnNewsVendor,
    },
    "dragon_tiger": {
        "eastmoney": EastmoneyDragonTigerVendor,
        "ftshare": FtshareDragonTigerVendor,
    },
    "margin": {
        "eastmoney": EastmoneyMarginVendor,
        "ftshare": FtshareMarginVendor,
    },
    "shareholders": {
        "zhitu": ZhituShareholdersVendor,
        "eastmoney": EastmoneyShareholdersVendor,
    },
    "dividend": {
        "eastmoney": EastmoneyDividendVendor,
        "zhitu": ZhituDividendVendor,
    },
    "northbound": {
        "ths": HexinNorthboundVendor,
    },
    "more_info": {
        "tq": TqMoreInfoVendor,
    },
}

# 各数据类型的合法 vendor 名集合(冻结,防止调用方误改)
PACKAGE_VENDORS_BY_TYPE: dict[str, frozenset[str]] = {
    datatype: frozenset(classes.keys()) for datatype, classes in VENDOR_CLASSES_BY_TYPE.items()
}


def build_vendors(datatype: str) -> dict[str, object]:
    """实例化某数据类型的全部 vendor,供 Engine 注入。未知 datatype 返回空字典。"""
    return {name: cls() for name, cls in VENDOR_CLASSES_BY_TYPE.get(datatype, {}).items()}
