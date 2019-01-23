import os
from bs4 import BeautifulSoup
import urllib3
import pandas as pd


def get_information(tweet):
    """Extracts the needed data from a single file.
    :param tweet: Single tweet in html format.
    """
    result = {}
    result['user_name'] = tweet.find('span', attrs={'class': 'username'}).get('text')
    result['time_created'] = tweet.find('small', attrs={'class': 'time'}).text.strip()
    result['hour_created'] = tweet.find('a', attrs={'class': 'tweet-timestamp'}).get('title')
    result['tweet_text'] = tweet.find('p', attrs={'class': 'js-tweet-text'}).text
    result['lang'] = tweet.find('p', attrs={'class': 'js-tweet-text'}).get('lang')
    result['stats'] = [x.text.strip() for x in tweet.findAll('span', attrs={'class': 'ProfileTweet-actionCount'})[:3]]

    return result


def scrape_twitter_page():
    """
    Scrapes the data from Tweeter Page and export the data into csv file.
    """
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://twitter.com/search?l=&q=%23ecoc%20plovdiv&src=typd')

    soup = BeautifulSoup(response.data, 'html.parser')
    page = soup.findAll('li', attrs={'class': 'js-stream-item'})

    data = pd.DataFrame([get_information(tweet) for tweet in page])

    data.reindex(columns=['user_name', 'time_created', 'hour_created', 'lang', 'stats', 'tweet_text'])

    dirname = os.path.dirname(__file__)
    output_file = os.path.join(os.path.dirname(dirname), os.path.join('data', 'data.csv'))

    if os.path.exists(output_file):
        data.to_csv(output_file, mode='a', index=False, header=False)
    else:
        data.to_csv(output_file, index = False)


if __name__ == "__main__":
    scrape_twitter_page()
