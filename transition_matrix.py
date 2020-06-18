import pandas as pd
from collections import Counter
from itertools import product

def cal_tran_prob(dataset, k=1):
    '''
    calculate transition probability given several time series data
    k = 1 means order 1 markov
    '''
    states = pd.unique(dataset["State"])
    states.sort()
    dataset = dataset.pivot(index="ID",columns="Time",values="State")
    
    cnt_join = Counter()  # counter for numerator
    cnt_de = Counter()  # counter for denominator
    
    for index, series in dataset.iterrows():
        length = series.last_valid_index()
        series = series.tolist()
        series = series[:length]
        
        for i in range(length-k):
            cnt_join[tuple(series[i:i+k+1])] += 1   # count P(x_i:x_i+k+1)
            cnt_de[tuple(series[i:i+k])] += 1     # count P(x_i:x_i+k)
        cnt_join[tuple(list(series[i+1:i+k+1])+["NaN"])] += 1
        cnt_de[tuple(series[i+1:i+k+1])] += 1

    matrix = []
    row = []
    for i in product(states, repeat=k):
        for j in product(states, repeat=1):
            try:
                row.append(cnt_join[i + j] / cnt_de[i])
            except ZeroDivisionError:
                row.append(0)
        row.append(1 - sum(row))  # 1 minus the total
        matrix.append(row)
        row = []

    return pd.DataFrame(data=matrix, index=list(product(states, repeat=k)), columns=list(product(states, repeat=1)) + ["NaN"])






#print(cal_tran_prob(syn,k=1))




