import numpy as np
import random

class trader():

    def __init__(self, parent_genome=None):
        def order_genome(genome):
            genome = genome.replace('-', '')
            list_to_order = []
            tail_to_keep = genome[120:128]
            # 12 E la lunghezza di un pattern
            for i in range(0, 10):
                str_to_app = genome[i*12:(i+1)*12]
                list_to_order.append(str_to_app)
            list_to_order.sort()
            # print(list_to_order)
            return f"{list_to_order[0]}-{list_to_order[1]}-{list_to_order[2]}-{list_to_order[3]}-{list_to_order[4]}-{list_to_order[5]}-{list_to_order[6]}-{list_to_order[7]}-{list_to_order[8]}-{list_to_order[9]}-{tail_to_keep}"
        
        if parent_genome is None:
            self.final_result = 0
            self.total_p_e_l = []
            self.trade_open = False
            genoma = ''
            for i in range(0, 128):
                int_to_app = random.randint(0, 1)
                genoma += str(int_to_app)
            self.genome = order_genome(genoma)
            # print(f"Genoma: {self.genome}")
            self.pattern = self.genome[0:130].replace('-', '')
            self.strategy = self.genome[130:138]
            self.risk = -1 * (int(self.strategy[0:1]) * 2 + int(self.strategy[1:2]) + (int(self.strategy[2:3])/2))
            self.reward = (int(self.strategy[3:4]) * 2 + int(self.strategy[4:5]) + (int(self.strategy[5:6])/2))        
            self.n_trades = 0
            self.n_win = 0
            self.n_loss = 0
            self.win_ratio = 0
            self.pattern_1 = []
            self.pattern_2 = []
            self.pattern_3 = []
            self.pattern_4 = []
            self.pattern_5 = []
            self.pattern_6 = []
            self.pattern_7 = []
            self.pattern_8 = []
            self.pattern_9 = []
            self.pattern_10 = []

        else:
            self.final_result = 0
            self.total_p_e_l = []
            self.trade_open = False
            self.genome = order_genome(parent_genome)
            # print(f"Genoma: {self.genome}")
            self.pattern = self.genome[0:120]
            self.strategy = self.genome[120:128]
            self.risk = -1 * (int(self.strategy[0:1]) * 2 + int(self.strategy[1:2]) + (int(self.strategy[2:3])/2))
            self.reward = (int(self.strategy[3:4]) * 2 + int(self.strategy[4:5]) + (int(self.strategy[5:6])/2))        
            self.n_trades = 0
            self.n_win = 0
            self.n_loss = 0
            self.win_ratio = 0
            self.pattern_1 = []
            self.pattern_2 = []
            self.pattern_3 = []
            self.pattern_4 = []
            self.pattern_5 = []
            self.pattern_6 = []
            self.pattern_7 = []
            self.pattern_8 = []
            self.pattern_9 = []
            self.pattern_10 = []



    def strategyDEC(self):
        if self.strategy[6:8] == '00' or self.strategy[6:8] == '11':
            self.short = True
            self.long = False
            self.position = 'SHORT'
        else:
            self.short = False
            self.long = True
            self.position = 'LONG'
        # print(f"STRATEGY: RISK: {self.risk}. REWARD: {self.reward}. POSITION TYPE: {self.position}")
        return self.risk, self.reward, self.position  
    
    def patternDEC(self):
        s = self.pattern.replace('-', '0')
        week = []
        for i in range(0, len(s), 4):
            day = s[i:i+4]
            if day[0:1] == '0':
                day_dec = -1 * (int(day[1:2]) * 2 + int(day[2:3]) + int(day[3:4])/2)
            else:
                day_dec = int(day[1:2]) * 2 + int(day[2:3]) + int(day[3:4])/2
            week.append(day_dec)

        self.pattern_1  = [week[0], week[1], week[2]]
        self.pattern_2  = [week[3], week[4], week[5]]
        self.pattern_3  = [week[6], week[7], week[8]]
        self.pattern_4  = [week[9], week[10], week[11]]
        self.pattern_5  = [week[12], week[13], week[14]]
        self.pattern_6  = [week[15], week[16], week[17]]
        self.pattern_7  = [week[18], week[19], week[20]]
        self.pattern_8  = [week[21], week[22], week[23]]  
        self.pattern_9  = [week[24], week[25], week[26]]
        self.pattern_10 = [week[27], week[28], week[29]]

        return [week[0], week[1], week[2]], [week[3], week[4], week[5]], [week[6], week[7], week[8]], [week[9], week[10], week[11]], [week[12], week[13], week[14]], [week[15], week[16], week[17]], [week[18], week[19], week[20]], [week[21], week[22], week[23]], [week[24], week[25], week[26]], [week[27], week[28], week[29]] 


    def openTrade(self, price):
        self.n_trades += 1
        self.trade_open = True
        self.open_price = price
        #if self.long:
        #    print(f"OPEN LONG POSITION AT {price}")
        #if self.short:
        #    print(f"OPEN SHORT POSITION AT {price}")

    def closeTrade(self, price):
        if self.long:
            p_e_l = -1 * (self.open_price - price) / self.open_price * 100
            # print(f"CLOSE LONG POSITION AT {price}. RESULT: {round(p_e_l, 2)}")
        if self.short:
            p_e_l = (self.open_price - price) / self.open_price * 100
            # print(f"CLOSE SHORT POSITION AT {price}. RESULT: {round(p_e_l, 2)}")
        if round(p_e_l, 2) >= 0:
            self.n_win  += 1
        if round(p_e_l, 2) <  0:
            self.n_loss += 1

        self.total_p_e_l.append(round(p_e_l, 2))
        self.win_ratio = round(self.n_win / (self.n_win + self.n_loss) * 100, 2)
        self.trade_open = False
    
    def results(self):
        self.final_result = 0
        # print(self.total_p_e_l)
        for el in self.total_p_e_l:
            self.final_result += float(el)


