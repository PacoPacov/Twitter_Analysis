import pandas as pd


def evaluate(text):
    df = pd.read_csv('../lexicon/emo_sentic_net_new.csv')
    lexicon = {}
    for i in df.to_dict(orient='records'):
        lexicon[i['Concepts']] = {'pos': i['Positive'], 'neg': i['Negative']}

    neg_list = ["no", "not", "nor", "neither", "aint", "none", "isnt", "wasnt",
               "doesent", "wont", "never"]
    intense_list = {"too": 10, "completely": 9, "remarkably": 8, "unusually": 7,
                   "incredibly": 6, "extremely": 5, "really": 4, "very": 3,
                   "totally": 9, "quite": 2, "rather": 2}
    deminisher_list = {"bit": 0.5, "little": 0.5, "hardly": 0.5,
                      "barely": 0.5}

    pos_instance, neg_instance = 0, 0
    max_pos, min_neg = 1, -1

    for index, w in enumerate(text):
        if w in lexicon:
            word_value = lexicon[w]['pos'] if lexicon[w]['pos'] else lexicon[w]['neg']
            left = (index - 5) if (index - 5) >= 0 else 0
            right = (index + 5) if (index + 5) < len(text) else len(text) -1

            for i in range(left, right+1):
                if text[i] in neg_lexicon:
                    if word_value <= 0:
                        word_value = - word_value - 1
                    else:
                        word_value = - word_value + 1
                if text[i] in intense_list:
                    if word_value <= 0:
                        word_value = word_value - intense_list[text[i]]
                    else:
                        word_value = - word_value + intense_list[text[i]]
                if len(text) >= 2 and text[i].isupper():
                    if word_value <= 0:
                        word_value = word_value - 1
                    else:
                        word_value = - word_value + 1
                if text[i] in deminisher_list:
                    if word_value <= 0:
                        word_value = word_value + deminisher_list[text[i]]
                    else:
                        word_value = - word_value - deminisher_list[text[i]]
#                 if text[i] in excl_list:
#                     if word_value <=0:
#                         word_value += -1
#                     else:
#                         word_value += 1 
        if word_value > 5:
            word_value = 5
        if word_value < -5:
            word_value = -5

        if word_value > 0:
            pos_instance = 1
        else:
            neg_instance = 1
        if word_value > 0 and word_value > max_pos:
            max_pos = word_value
        if word_value < 0 and word_value < min_neg:
            min_neg = word_value

        if max_pos == - min_neg == 1:
            return -1 # TODO
        elif max_pos > - min_neg:
            return 1
        elif max_pos < - min_neg:
            return 0
        elif max_pos == - min_neg:
            if pos_instance > neg_instance:
                return 1
            elif pos_instance < neg_instance:
                return 0
            elif pos_instance == neg_instance:
                return -1
        # finito 
