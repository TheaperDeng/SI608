import networkx as nx
from networkx.algorithms import bipartite
import network_map2 as nm2
import json
import pandas as pd
import sklearn
import numpy as np
import projection as proj


def filter_test_data(all_word_set, all_emoji, test_df):
    test_df = test_df.drop(labels = list(test_df[test_df.apply(lambda row:(not row.word in all_word_set) or (not row.emoji in all_emoji),axis=1)].index), axis=0)
    return test_df

def evaluate(test_df, predict_func):
    test_df['res'] = test_df.apply(lambda row:predict_func(row.word, row.emoji) ,axis=1)
    count = 0
    for index, row in test_df.iterrows():
        if row[2] <= 0:
            count += 1
    print(1-count/len(test_df))
    return test_df.mean().res

def random_pred(word, emoji):
    return 1/len(sl)

def trivial_neighbor(word, emoji):
    global sl
    total_weight = 0
    good_weight = 0
    for key in sl.keys():
        if word in sl[key].keys():
            total_weight += sl[key][word]
            if key == emoji:
                good_weight += sl[key][word]
    if total_weight == 0:
        return 0
    else:
        return good_weight/total_weight

def normalize_score(test_word, test_emoji, FG, Gp):
    score = proj.projection_score(test_word, test_emoji, FG, Gp)
    # print(len(emoji_list))
    print("The normalized score for {}-{} is {}".format(test_word, test_emoji, score))
    # # result_dic[(test_word, test_emoji)] = score
    # if score > 0:
    #     sum_ = score
    #     for e in emoji_list:
    #         if e != test_emoji:
    #             s, _ = proj.projection_method_v2(word, e, FG, Gp)
    #             sum_ += s
    #     norm_score = score / sum_
    #     print("The normalized score for {}-{} is {}".format(test_word, test_emoji, norm_score))
    #     score = norm_score
    print("-------------------------------------------------")
    return score


def evaluate_proj(test_df, FG, Gp):
    # test_df['res'] = test_df.apply(lambda row:predict_func(row.word, row.emoji, FG, Gp) ,axis=1)
    # return test_df.mean().res

    # global result_dic
    # result_dic = {}
    res = []
    count = 0
    for index, row in test_df.iterrows():
        test_word = row[0]
        test_emoji = row[1]
        score, flag = proj.projection_score(test_word, test_emoji, FG, Gp)
        if score <= 0:
            count += 1
        # score = proj.projection_method_v2(test_word, test_emoji, FG, Gp)

        # print(len(emoji_list))

        print("The unnormalized score for {}-{} is {}".format(test_word, test_emoji, score))
        # result_dic[(test_word, test_emoji)] = score
        # if score > 0:
        #     norm_score = normalize_score(emoji_list, test_word, test_emoji, score, FG, Gp)
        #     print("The normalized score for {}-{} is {}".format(test_word, test_emoji, norm_score))
        #     score = norm_score
        print("-------------------------------------------------")
        res.append(score)
    print("The ratio with unbipartite emoji is: {}%".format((1-count/len(test_df))*100))
    return np.mean(res)



global sl # can be removed
f = open("./myfile.json", "r", encoding='utf-8')
sl = json.load(f)
f.close()

all_word_set = {}
for key in sl.keys():
    for word in sl[key].keys():
        if word not in all_word_set:
            all_word_set[word] = 1
        else:
            all_word_set[word] += 1

test_df = pd.read_csv('./test_rec.csv')
test_df = filter_test_data(all_word_set, sl.keys(), test_df)

print("The score for random prediction: ")
print(evaluate(test_df, random_pred))

print("The score for trivial neighbor: ")
print(evaluate(test_df, trivial_neighbor))
# 0.043115

FG, Gp = proj.load_graph('simp', FG_NAME = './Graphs/bipartite.gpickle')
print("The score for normalized projection: ")

# score, emoji_list = proj.projection_score(test_word, test_emoji, FG, Gp)
# result_dic[(test_word, test_emoji)] = score
print(evaluate_proj(test_df, FG, Gp))