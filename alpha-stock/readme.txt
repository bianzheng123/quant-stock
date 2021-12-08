仿照论文AlphaStock: A Buying-Winners-and-Selling-Losers Investment Strategy using Interpretable Deep Reinforcement Attention Networks实现
特征提取说明:
论文<->实现
Price Rising Rate <-> price_rise_rate
Fine-grained Volatility <-> day_price_std
Trade Volume <-> volume
Market Capitalization <-> mkt_capital
Price-earning Ratio <-> price_earning_ratio
Book-to-market Ratio <-> price_book_ratio
Dividend <-> 数据找不到,就不用这个特征了

以月线为标准, 全部的数据都做了归一化处理(除了日线std和每月涨跌幅)