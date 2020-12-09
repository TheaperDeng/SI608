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
    
    if word_in not in FG:
        return 0
    # See the emoji of direct this word
    dict_emoji = {}
    res_weight = 0
    total_weight = 0
    weight_emoji = 0
    for e in FG[word_in]:
        total_weight += FG[word_in][e]['weight']
        dict_emoji[e] = FG[word_in][e]['weight']
        if e == emoji_in:
            weight_emoji = FG[word_in][e]['weight']

    for e in dict_emoji:
        dict_emoji[e] = dict_emoji[e]/total_weight
    res_weight += weight_emoji/total_weight

#     if word_in not in Gp1:
#         total = 0
#         for e in dict_emoji:
#             total += dict_emoji[e]
#         if emoji_in not in dict_emoji:
#             return 0
#         return dict_emoji[emoji_in]/total
    # See the emoji of neighbours
    
    if word_in not in Gp1:
        if emoji_in not in dict_emoji:
            return 0
        total = 0
        for e in dict_emoji:
            total += dict_emoji[e]
        return dict_emoji[emoji_in]/total
    
    
    sum_weight_neibour = 0
    for neighbours in Gp1[word_in]:
        sum_weight_neibour += Gp1[word_in][neighbours]['weight']
    
    for neighbours in Gp1[word_in]:    
        current_neighbour_weight = Gp1[word_in][neighbours]['weight']/sum_weight_neibour
        total_weight = 0
        weight_emoji = 0
        dict_e_tmp = {}
        for e in FG[neighbours]:
            total_weight += FG[neighbours][e]['weight']
            dict_e_tmp[e] = FG[neighbours][e]['weight']
            if e == emoji_in:
                weight_emoji = FG[neighbours][e]['weight']
        res_weight += current_neighbour_weight * (weight_emoji/total_weight)
        for e in dict_e_tmp:
            if e in dict_emoji:
#                 dict_emoji[e] += current_neighbour_weight * (dict_e_tmp[e]/total_weight)
                dict_emoji[e] += 0.01 * (dict_e_tmp[e]/total_weight)
            else:
#                 dict_emoji[e] = current_neighbour_weight * (dict_e_tmp[e]/total_weight)
                dict_emoji[e] = 0.01 * (dict_e_tmp[e]/total_weight)
                
    if emoji_in not in dict_emoji:
        return 0
    total = 0
    for e in dict_emoji:
        total += dict_emoji[e]
    return dict_emoji[emoji_in]/total
    

                