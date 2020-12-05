def load_graph(FG_NAME, GP_NAME):
    import network_map2 as nm2
    import networkx as nx
    import json
    import pickle

    
    with open(FG_NAME, 'rb') as f: 
        FG = pickle.load(f)
    with open(GP_NAME, 'rb') as f: 
        Gp1 = pickle.load(f)  
    return (FG, Gp1)
    

def projection_method(word_in, emoji_in, FG, Gp1):
    # See the emoji of direct this word
    try:
        res_weight = 0
        total_weight = 0
        weight_emoji = 0
        for e in FG[word_in]:
            total_weight += FG[word_in][e]['weight']
            if e == emoji_in:
                weight_emoji = FG[word_in][e]['weight']

        res_weight += weight_emoji/total_weight

        # See the emoji of neighbours
        sum_weight_neibour = 0
        for neighbours in Gp1[word_in]:
            sum_weight_neibour += Gp1[word_in][neighbours]['weight']
        for neighbours in Gp1[word_in]:    
            current_neighbour_weight = Gp1[word_in][neighbours]['weight']/sum_weight_neibour
            total_weight = 0
            weight_emoji = 0
            for e in FG[neighbours]:
                total_weight += FG[neighbours][e]['weight']
                if e == emoji_in:
                    weight_emoji = FG[neighbours][e]['weight']
            res_weight += current_neighbour_weight * (weight_emoji/total_weight)
    
        return res_weight
    except:
        return 0