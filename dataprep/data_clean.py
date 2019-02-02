import re


def extract_tags(tweet):
    tweet = tweet.replace('\r\n', '')
    tags = re.findall('(#\w+)', tweet)
    tags = [w.replace('https', '') for w in tags]
    tags = [w.replace('pic', '') for w in tags]

    return tags


def tweet_cleaner(tweet):
    pat1 = r'@[A-Za-z0-9]+'
    pat2 = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
    pat3 = r'pic.+'
    combined_pat = r'|'.join((pat1, pat2))

    tweet = tweet.replace('http', ' http')
    tweet = tweet.replace('pic.', ' pic.')
    tweet = tweet.replace('#', '')

    tweet = re.sub(combined_pat, '', tweet)
    tweet = re.sub(pat3, '', tweet)
    letters_only = re.sub("[^a-zA-Z]", " ", tweet)
    lower_case = letters_only.lower()
    return lower_case


def prep_tweet(tweet):
    return list(nlp(tweet).sents)
#     return [sentiment_analyzer_scores(x) for x in nlp(tweet).sents]


def prep(tw):
    import re

    tw = tw.replace('http', ' http')
    tw = tw.replace('pic.tw', ' pic.tw')

    tw = re.sub(r'#\w+', '', tw)
    tw = re.sub(r'http.+', '', tw)
    tw = re.sub(r'pic.tw.+', '', tw)

    tw.replace('\n', '')

    return tw
