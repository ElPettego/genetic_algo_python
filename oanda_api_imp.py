import oanda_api as oa
import pandas as pd
import constants.config as defs


data = oa.OandaApi()

df = data.get_candles_df(defs.PAIR)

df.drop(labels=['bid_o', 'bid_l', 'bid_h', 'bid_c', 'ask_o', 'ask_l', 'ask_h', 'ask_c'], axis=1, inplace=True)

df.rename(columns={'time':'Date', 'mid_c':'Close', 'mid_o': 'Open', 'mid_l': 'Low', 'mid_h': 'High', 'volume': 'Volume'}, inplace=True)

df.to_csv(f'data/{defs.PAIR}_{defs.GRANULARITY}.csv', index=False)

print(df)