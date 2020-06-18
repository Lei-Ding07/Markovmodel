import pandas as pd
from itertools import product

def Starting_matrices(dataset,k=1):
    '''
    dataset should be a pandas dataframe
    k = 1 means order one Markov model
    return k matrices
    '''
    states = pd.unique(dataset["State"])
    states.sort()
    dataset = dataset.pivot(index="ID",columns="Time",values="State")
    counter = [ Counter() for i in range(k)]
    matrices = []

    for _,data in dataset.iterrows():
        for order in range(k):
            counter[order][tuple(data[0:order+1])] += 1
            
    for i in range(k):
        if i == 0:
            total = sum(counter[i].values())
            matrix = []
            for j in product(states, repeat=1):   
                matrix.append(counter[i][j]/total)
            matrices.append(pd.DataFrame(data=matrix,index=list(product(range(1,len(counter[i])+1), repeat=1)),columns=["Pobability"]))
        else:
            matrix = []
            row = []
            for index in product(states, repeat=i):  # index
                for j in product(states, repeat=1):  # columns
                    try:
                        import pdb
                        #pdb.set_trace()
                        row.append(counter[i][index + j] / counter[i-1][index])
                    except ZeroDivisionError:
                        row.append(0)
                row.append(1 - sum(row))  # 1 minus the total
                matrix.append(row)
                row = []
            matrices.append(pd.DataFrame(data=matrix, index=list(product(states, repeat=i)), columns=list(product(states, repeat=1)) + ["NaN"]))
    
    
    return matrices
