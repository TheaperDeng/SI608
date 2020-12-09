# GP_MODE:
## 1. simp:simple
## 2. hyper:hyperbolic
## 3. ycn:ycn
## 4. probs:probS
## 5. heats:HeatS
## 6. hybrid:Hybrid
def load_graph(GP_MODE, FG_NAME = './Graphs/bipartite.gpickle'):
    import networkx as nx
    FG = nx.read_gpickle(FG_NAME)
    GP_path = './Graphs/Gp_' + GP_MODE + '_15k.gpickle'
    Gp = nx.read_gpickle(GP_path)
    return (FG, Gp)

def projection_score(word, emoji, FG, Gp):
    try:
        emoji_list = []
        # Bipartite weight score:
        ## If emoji has co-occurrence with word in the bipartite graph:
        # get the weight ratio for all this word's neighbors:
        bi_weight = 0
        bi_neighbors = FG.neighbors(word)

        total_bi_weight = 0
        for bi_nei in bi_neighbors:
            if emoji == bi_nei:
                bi_weight = FG[word][bi_nei]['weight']
            total_bi_weight += FG[word][bi_nei]['weight']
        bi_weight /= total_bi_weight
        # print('bi_weight is: ', bi_weight)

        if word in Gp.nodes():
            # Unbipartite weight score:
            unbi_weight = 0

            neighbor_weights = {}
            neighbor_emoji_weights = {}

            for unbi_w in Gp.neighbors(word):
                neighbor_weights[unbi_w] = Gp[word][unbi_w]['weight']
                # Iterate through each word neighbor:
                unbi_w_weight = 0
                temp_total = 0
                if not emoji in FG.neighbors(unbi_w):
                    pass
                else:
                    for bi_nei in FG.neighbors(unbi_w):
                        if not bi_nei in emoji_list:
                            emoji_list.append(bi_nei)
                        if emoji == bi_nei:
                            unbi_w_weight = FG[unbi_w][bi_nei]['weight']
                        temp_total += FG[unbi_w][bi_nei]['weight']
                    unbi_w_weight /= temp_total
                neighbor_emoji_weights[unbi_w] = unbi_w_weight
                # If the neighbor has the emoji weight of 0, then reset the neighbor weight to 0
                if neighbor_emoji_weights[unbi_w] == 0:
                    neighbor_weights[unbi_w] = 0

            total_weight = 0
            
            for nei in neighbor_weights.keys():
                if neighbor_emoji_weights[nei] != 0:
                    unbi_weight += neighbor_weights[nei] * neighbor_emoji_weights[nei]
                total_weight += neighbor_weights[nei]
                
            unbi_weight /= total_weight
            # print('unbi_weight is: ', unbi_weight)
            flag = 0
            if not emoji in bi_neighbors and emoji in emoji_list:
                flag = 1

            return (bi_weight + unbi_weight), flag
        else:
            return bi_weight, 0   
    except:
        return 0, 0


def projection_method_v2(word_in, emoji_in, FG, Gp1):
    
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
        if not emoji_in in FG[neighbours]:
            Gp1[word_in][neighbours]['weight'] = 0
        sum_weight_neibour += Gp1[word_in][neighbours]['weight']
    
    for neighbours in Gp1[word_in]:   
        if  sum_weight_neibour > 0:
            current_neighbour_weight = Gp1[word_in][neighbours]['weight']/sum_weight_neibour
        else:
            current_neighbour_weight = 0
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
                dict_emoji[e] += 0.1 * (dict_e_tmp[e]/total_weight)
            else:
#                 dict_emoji[e] = current_neighbour_weight * (dict_e_tmp[e]/total_weight)
                dict_emoji[e] = 0.1 * (dict_e_tmp[e]/total_weight)
                
    if emoji_in not in dict_emoji:
        return 0
    total = 0
    for e in dict_emoji:
        total += dict_emoji[e]
    return dict_emoji[emoji_in]/total

# FG, Gp = load_graph('simp', FG_NAME = './Graphs/bipartite.gpickle')
# test_word = 'launch'
# test_emoji = ':rocket:'
# # print(list(FG.neighbors(test_word)))
# # print(list(Gp.neighbors(test_word)))
# print(projection_method_v2(test_word, test_emoji, FG, Gp))




