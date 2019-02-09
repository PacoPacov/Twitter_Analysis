import requests
import pandas as pd
import json
import warnings


def use_azure_pd_df(df, tweet_column, save_response=True):
    text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
    subscription_key = '39c90169bc1a41ab88379ed9e59316ca'

    another_df = pd.DataFrame()

    another_df['text'] = df[tweet_column]
    another_df['language'] = 'en'
    another_df['id'] = another_df.index

    data = another_df.to_dict('record')
    documents = {'documents': data}

    sentiment_api_url = text_analytics_base_url + "sentiment"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(
        sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()

    if sentiments['errors']:
        warnings.warn(f"error occur {sentiments['errors']}")

    if save_response:
        with open(f'azure_response_result.json', 'w') as f:
            json.dump(sentiments, f)

    return pd.DataFrame(sentiments['documents'])


def score_word_az(word, save_response=False):
    text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
    subscription_key = '39c90169bc1a41ab88379ed9e59316ca'

    documents = {'documents': [
        {
        'id': 1,
        'language': 'en',
        'text': word
        }
    ]}

    sentiment_api_url = text_analytics_base_url + "sentiment"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(
        sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()

    if sentiments['errors']:
        warnings.warn(f"error occur {sentiments['errors']}")

    if save_response:
        with open(f'azure_response_result.json', 'w') as f:
            json.dump(sentiments, f)

    return sentiments['documents'][0]['score']


if __name__ == "__main__":
    print(score_word_az('happy'))
