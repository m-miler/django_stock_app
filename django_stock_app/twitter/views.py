from django.conf import settings
import tweepy

TWITTER_CREDENTIALS = {
    'bearer_token': settings.BEARER_TOKEN,
    'api_key': settings.API_KEY,
    'api_key_secret': settings.API_KEY_SECRET,
    'access_token': settings.ACCESS_TOKEN,
    'access_token_secret': settings.ACCESS_TOKEN_SECRET
}


def search_tweets(ticker):
    """ Function to search recent tweets using v2 Twitter API."""
    query = f'#{ticker} #{ticker.lower()} #GPW #gpw lang:pl'
    tweet_fields = ['author_id', 'created_at', 'text']
    client = tweepy.Client(
        bearer_token=TWITTER_CREDENTIALS.get('bearer_token'),
        consumer_key=TWITTER_CREDENTIALS.get('api_key'),
        consumer_secret=TWITTER_CREDENTIALS.get('api_key_secret'),
        access_token=TWITTER_CREDENTIALS.get('access_token'),
        access_token_secret=TWITTER_CREDENTIALS.get('access_token_secret')
    )

    tweets = client.search_recent_tweets(query, max_results=10,
                                         tweet_fields=tweet_fields,
                                         )

    return tweets
