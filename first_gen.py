from datetime import date
import trader as tr
import pandas as pd
import constants.config as defs
import random as rnd
import sys
import datetime

# SETTINGS
pd.set_option('display.max_colwidth', None)

# VARIABILI
percent_list = []
norm_percent_list = []
all_wojaks = []
elite_wojaks = []

# GENERARE LA PRIMA GENERAZIONE
def first_generation():
    wojak_iterations = 0
    while wojak_iterations < defs.FIRST_GENERATION_POPULATION:
        wojak = tr.trader()
        RISK, REWARD, POSITION = wojak.strategyDEC()
        PATTERN_1, PATTERN_2, PATTERN_3, PATTERN_4, PATTERN_5, PATTERN_6, PATTERN_7, PATTERN_8, PATTERN_9, PATTERN_10 = wojak.patternDEC()

        trade_counter = 0
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
                if PATTERN_1 == pattern or PATTERN_2 == pattern or PATTERN_3 == pattern or PATTERN_4 == pattern or PATTERN_5 == pattern or PATTERN_6 == pattern or PATTERN_7 == pattern or PATTERN_8 == pattern or PATTERN_9 == pattern or PATTERN_10 == pattern:
                    wojak.openTrade(current_price)
                    trade_counter += 1 
                    # print(f"TRADE APERTO NUMERO: {trade_counter}. PREZZO: {current_price}")

        wojak.results()
        # print(f"TRADE APERTI: {trade_counter}. TOTAL RESULT: {round(wojak.final_result, 2)}%. STRATEGY: RISK: {wojak.risk}. REWARD: {wojak.reward}. POSITION: {wojak.position}")
        all_wojaks.append(wojak)
        wojak_iterations += 1

# seleziono i piu profittevoli
def selection():
    def sort_f(e):
        return e.win_ratio

    global data
    data = [] 
    for wojak in all_wojaks:
        
        data.append([wojak.genome, round(wojak.final_result, 2), wojak.n_trades, wojak.win_ratio])

        if round(wojak.final_result, 2) > defs.PROFIT_LEVEL_REPRODUCTION and wojak.n_trades > defs.TRADE_NUMBER_REPRODUCTION:
            elite_wojaks.append(wojak)
    
    elite_wojaks.sort(key=sort_f)

# mutazione di alcuni geni dei piu profittevoli 
def mutation(parent_genome):
    for i in range(len(parent_genome)-1):
        if parent_genome[i] != '-':
            if rnd.randint(1, 100) < defs.MUTATION_RATE:
                if parent_genome[i] == '0':
                    parent_genome = f"{parent_genome[0:i]}1{parent_genome[i:138]}"
                if parent_genome[i] == '1':
                    parent_genome = f"{parent_genome[0:i]}0{parent_genome[i:138]}"
    return parent_genome

# riproduzione dei piu profittevoli
def reproduction():
    for wojak in elite_wojaks:
        print(wojak.genome, ' - PROFIT: ', round(wojak.final_result, 2),' - N TRADES: ', wojak.n_trades, ' - WIN RATIO: ', wojak.win_ratio)
    
    print('GENERATION 2')
    for i in range(defs.N_GENERATION_POPULATION):
        wojak_gen_2 = tr.trader(mutation(elite_wojaks[rnd.randint(0, len(elite_wojaks)-1)].genome))
        print(wojak_gen_2.genome, ' - PROFIT: ', round(wojak_gen_2.final_result, 2),' - N TRADES: ', wojak_gen_2.n_trades, ' - WIN RATIO: ', wojak_gen_2.win_ratio)
    # print(wojak_gen_2.genome)

# INIZIO DELLO SCRIPT
# DATA NORMALIZATION
print("DATA NORMALIZATION")
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
#print(df)

print("CREAZIONE DELLA PRIMA GENERAZIONE")

first_generation()

selection()

results = pd.DataFrame(data=data, columns=['GENOME','PROFIT','NUMERO DI TRADE', 'WIN RATIO'])

print("RISULTATI PRIMA GENERAZIONE")
print(results)

time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
results.to_csv(f"results/first_gen/first_gen_{time}.csv", index=False)

# print("MIGLIORI DELLA PRIMA GENERAZIONE")
# reproduction()
