import mplfinance as mpf
import constants.config as defs
import pandas as pd
from datetime import datetime

df = pd.read_csv(f'data/{defs.PAIR}_{defs.GRANULARITY}.csv', index_col=0, parse_dates=True)

mpf.plot(df, type='candle', style='nightclouds', volume=True, mav=200)
