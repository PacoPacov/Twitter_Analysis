import pandas as pd
import preprocessor as p
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from symspellpy.symspellpy import SymSpell, Verbosity
import os


POSITIVE = ["*O", "*-*", "*O*", "*o*", "* *",
        ":P", ":D", ":d", ":p",
        ";P", ";D", ";d", ";p",
        ":-)", ";-)", ":=)", ";=)",
        ":<)", ":>)", ";>)", ";=)",
        "=}", ":)", "(:;)",
        "(;", ":}", "{:", ";}",
        "{;:]",
        "[;", ":')", ";')", ":-3",
        "{;", ":]",
        ";-3", ":-x", ";-x", ":-X",
        ";-X", ":-}", ";-=}", ":-]",
        ";-]", ":-.)",
        "^_^", "^-^"]

NEGATIVE = [":(", ";(", ":'(",
            "=(", "={", "):", ");",
            ")':", ")';", ")=", "}=",
            ";-{{", ";-{", ":-{{", ":-{",
            ":-(", ";-(",
            ":,)", ":'{",
            "[:", ";]", ":O"
            ]

our_corpus = {'aint',
           'barely',
           'bit',
           'completely',
           'doesnt',
           'extremely',
           'hardly',
           'incredibly',
           'isnt',
           'little',
           'moderately',
           'neither',
           'never',
           'no',
           'none',
           'nor',
           'not',
           'quite',
           'rather',
           'really',
           'remarkably',
           'slightly',
           'so',
           'too',
           'totally',
           'unusually',
           'very',
           'wasnt',
           'wont'}


def settings_up():
    print('Setting packages')
    set_nltk()
    # pip install tweet-preprocessor
    # pip install -U symspellpy
    # need to have frequency_dictionary_en_82_765.txt

    # Optional: 
    #    pip install textblob

def set_nltk():
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')


def find_emoji(tweet):
    for word in tweet.split():
        if word in POSITIVE:
            return word
        if word in NEGATIVE:
            return word


def remove_emoji(tweet):
    if tweet['Emoji']:
      return tweet['SentimentText'].replace(tweet['Emoji'], '').strip()
    else:
      return tweet['SentimentText'].strip()


def remove_duplicate_consecutive_letters(string):
    new_str = ''
    count = 0

    for i in range(1, len(string)):
        if string[i] == string[i-1]:
            count += 1
        else:
            count = 0

        if(count < 2):
            new_str += string[i-1]

    new_str += string[-1]

    return new_str


def remove_repeated_letters(tokens):
    return [remove_duplicate_consecutive_letters(token) for token in tokens]


def symspell(text):
    # create object
    initial_capacity = 83000
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 0
    prefix_length = 7
    sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                         prefix_length)
    # load dictionary
    dictionary_path = "Twitter_Analysis\spellcheck_dictionary\frequency_dictionary_en_82_765.txt"
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file

    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return

    result = sym_spell.word_segmentation(text)

    return result.corrected_string


def lemmitize(tweet):
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_tweet = [wordnet_lemmatizer.lemmatize(w) for w in tweet]

    return ' '.join(lemmatized_tweet)

def dataprep(path):
    df = pd.read_csv(path, nrows=100, usecols=['Sentiment', 'SentimentText'])

    # Create column with extracted emojis
    df.loc[:, 'Emoji'] = df.apply(
        lambda x: find_emoji(x['SentimentText']), axis=1)

    # Remove emojis from text
    df.loc[:, "Filtered_Text"] = df.apply(lambda x: remove_emoji(x), axis=1)

    # Remove urls and Emojis with preprocessor
    p.set_options(p.OPT.URL, p.OPT.EMOJI)

    df['Filtered_Text'] = df.apply(
        lambda x: p.clean(x['Filtered_Text']), axis=1)

    df['Filtered_Text'].str.replace(r'[@|#]', '')

    # tokenize
    df.loc[:, 'Tokenized'] = df.apply(
        lambda x: word_tokenize(x['Filtered_Text']), axis=1)

    df.loc[:, 'Prepped_Tokens'] = df.apply(
        lambda x: remove_repeated_letters(x['Tokenized']), axis=1)

    df.loc[:, 'Prepped_Tokens_Flag'] = df.apply(lambda x:
                        len(' '.join(x['Tokenized'])) != len(' '.join(x['Prepped_Tokens'])),
                        axis=1)

    # general flag if any of the tokens is UPPER case
    df['IsUpper_Flag'] = df.apply(lambda x: any(token.isupper() for token in x['Prepped_Tokens']
                                                if len(token) > 1),
                                  axis=1)

    stop_words = set(stopwords.words('en'))
    # remove words that we use
    stop_words -= our_corpus

    df['Filtered_Prepped_Tokens'] = df.apply(lambda x: [token for token in x['Prepped_Tokens']
                                                        if token not in stop_words],
                                             axis=1)

    # need to flag words that are all UPPER
    df['Upper_Tokens'] = df.apply(lambda x: [int(token.isupper())
                                             for token in x['Filtered_Prepped_Tokens']],
                                  axis=1)

    # convert to lower
    df['Filtered_Prepped_Tokens'] = df.apply(lambda x: [token.lower() for token in x['Prepped_Tokens']
                                                        if type(token) == str],
                                             axis=1)

    # Spell correction
    #######################################


    # Lemmatize the text
    df.loc[:, 'Lemmatized_Filted_Tweet'] = df.apply(lambda x: lemmitize(x['Filtered_Prepped_Tokens']),
                                                    axis=1)

    return df