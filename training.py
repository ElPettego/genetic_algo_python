import pandas as pd
import constants.config as defs
import random as rnd
import trader

# SETTINGS
pd.set_option('display.max_colwidth', None)

first_gen = pd.read_csv(defs.FIRST_GEN_FILE)

def selection(df = pd.DataFrame, profit = float, win_ratio = float, min_trade = int):
    df.sort_values(by=['PROFIT'], inplace=True, ascending=False)
    print(df)
    fittest = []
    while len(fittest) < 100:
        for i in range(0, len(df)):
            # print(df.iloc[i]['GENOME'])
            if df.iloc[i]['PROFIT'] > profit and df.iloc[i]['WIN RATIO'] > win_ratio and df.iloc[i]['NUMERO DI TRADE'] > min_trade:
                fittest.append(df.iloc[i]['GENOME'])
    print(fittest)

    return fittest

def mutation(parent_genome = str):
    for i in range(len(parent_genome)-1):
        if parent_genome[i] != '-':
            if rnd.randint(1, 100) < defs.MUTATION_RATE:
                if parent_genome[i] == '0':
                    parent_genome = f"{parent_genome[0:i]}1{parent_genome[i:138]}"
                if parent_genome[i] == '1':
                    parent_genome = f"{parent_genome[0:i]}0{parent_genome[i:138]}"
    return parent_genome

def reproduction(parents = list):
    sons = []
    while len(sons) < defs.REPRODUCTION_POPULATION:
        son = trader.trader(mutation(parents[rnd.randint(0, 99)]))
        sons.append(son)
    print(sons)
    return sons

def backtest(traders = list, df = pd.DataFrame):
    all_wojaks = []
    data = []
    for i in range (0, len(traders)):
        wojak = traders[i]
        wojak.strategyDEC()
        wojak.patternDEC()
        
        for i in range(2, len(df)):
            current_price = df.at[i, 'Close']
            pattern = [df.at[i, 'Percent Norm'], df.at[i-1, 'Percent Norm'], df.at[i-2, 'Percent Norm']]
            if wojak.trade_open:
                if wojak.position == 'LONG':
                    if -1 * (wojak.open_price - current_price) / wojak.open_price * 100 >= wojak.reward or -1 * (wojak.open_price - current_price) / wojak.open_price * 100 <= wojak.risk:
                        wojak.closeTrade(current_price)
                if wojak.position == 'SHORT':
                    if (wojak.open_price - current_price) / wojak.open_price * 100 >= wojak.reward or (wojak.open_price - current_price) / wojak.open_price * 100 <= wojak.risk:
                        wojak.closeTrade(current_price)
                # print(i, pattern)
            else:
                # print(i, pattern)
                if wojak.pattern_1 == pattern or wojak.pattern_2 == pattern or wojak.pattern_3 == pattern or wojak.pattern_4 == pattern or wojak.pattern_5 == pattern or wojak.pattern_6 == pattern or wojak.pattern_7 == pattern or wojak.pattern_8 == pattern or wojak.pattern_9 == pattern or wojak.pattern_10 == pattern:
                    wojak.openTrade(current_price)
                    # print(f"TRADE APERTO NUMERO: {trade_counter}. PREZZO: {current_price}")

        wojak.results()
        # print(f"TRADE APERTI: {trade_counter}. TOTAL RESULT: {round(wojak.final_result, 2)}%. STRATEGY: RISK: {wojak.risk}. REWARD: {wojak.reward}. POSITION: {wojak.position}")
        all_wojaks.append(wojak)

    for trader in all_wojaks:
        data.append([trader.genome, round(trader.final_result, 2), trader.n_trades, trader.win_ratio])

    results = pd.DataFrame(data=data, columns=['GENOME', 'PROFIT', 'NUMERO DI TRADE', 'WIN RATIO'])
    results.sort_values(by=['PROFIT'], inplace=True, ascending=False)
    print(results)

def data_normalization():
    norm_percent_list = []
    percent_list = []
    df = pd.read_csv(f'data/{defs.PAIR}_{defs.GRANULARITY}.csv')
    try:
        df.drop(labels=['High', 'Volume', 'Adj Close', 'Low', 'Open'], axis=1, inplace=True)
    except:
        print('FILE GIA MANIPOLATO')
    for i in range(0, len(df)):
        if i == 0:
            value_to_app = 0
        else:
            value_to_app = (float(df.at[i, 'Close']) - float(df.at[i-1, 'Close'])) / float(df.at[i-1, 'Close']) * 100
        percent_list.append(round(value_to_app, 2))

    df['Percent'] = percent_list

    for i in range (0, len(df)):
        if df.at[i, 'Percent'] >= 3.25:
            norm_value_to_app = 3.5
        if 2.75 <= df.at[i, 'Percent'] < 3.25: 
            norm_value_to_app = 3
        if 2.25 <= df.at[i, 'Percent'] < 2.75: 
            norm_value_to_app = 2.5
        if 1.75 <= df.at[i, 'Percent'] < 2.25: 
            norm_value_to_app = 2
        if 1.25 <= df.at[i, 'Percent'] < 1.75: 
            norm_value_to_app = 1.5
        if 0.75 <= df.at[i, 'Percent'] < 1.25: 
            norm_value_to_app = 1
        if 0.25 <= df.at[i, 'Percent'] < 0.75:
            norm_value_to_app = 0.5
        if -0.25 <= df.at[i, 'Percent'] < 0.25: 
            norm_value_to_app = 0
        if -0.75 <= df.at[i, 'Percent'] < -0.25: 
            norm_value_to_app = -0.5
        if -1.25 <= df.at[i, 'Percent'] < -0.75: 
            norm_value_to_app = -1
        if -1.75 <= df.at[i, 'Percent'] < -1.25: 
            norm_value_to_app = -1.5
        if -2.25 <= df.at[i, 'Percent'] < -1.75: 
            norm_value_to_app = -2
        if -2.75 <= df.at[i, 'Percent'] < -2.25: 
            norm_value_to_app = -2.5
        if -3.25 <= df.at[i, 'Percent'] < -2.75: 
            norm_value_to_app = -3
        if df.at[i, 'Percent'] < -3.25: 
            norm_value_to_app = -3.5     
        norm_percent_list.append(norm_value_to_app)

    df['Percent Norm'] = norm_percent_list
    return df

best_genome = selection(df=first_gen, profit=defs.MIN_PROFIT, win_ratio=defs.MIN_WIN_RATIO, min_trade=defs.MIN_TRADE)
new_gen = reproduction(best_genome)
backtest(new_gen, data_normalization())