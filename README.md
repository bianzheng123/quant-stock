# stock-market

用于验证交易策略以及相关指标在A股市场中的有效性，后期可能会扩展到美股或者数字交易市场，采用python实现



### 技术指标

1. MA均线

   - 遛狗算法

   - 20日均线为底部的有效性

2. MACD均线

### 交易策略

1. 对两个股票进行对比，买入情况根据上一天进行对比，买入上一天收益最高的那个，如果都是负收益，就不买入

### 备注

如无特别说明，交易数据采用的是上证50指数以及中证300，取近五年的数据以及

数据采集工具采用tushare，画图采用matplot