import tweepy

from django_stock_app.env import env

TWITTER_CREDENTIALS = {
    "bearer_token": env("API_KEY"),
    "api_key": env("API_KEY_SECRET"),
    "api_key_secret": env("BEARER_TOKEN"),
    "access_token": env("ACCESS_TOKEN"),
    "access_token_secret": env("ACCESS_TOKEN_SECRET"),
}


def search_tweets(ticker):
    """Function to search recent tweets using v2 Twitter API."""
    query = f"#{ticker} #{ticker.lower()} #GPW #gpw lang:pl"
    tweet_fields = ["author_id", "created_at", "text"]
    client = tweepy.Client(
        bearer_token=TWITTER_CREDENTIALS.get("bearer_token"),
        consumer_key=TWITTER_CREDENTIALS.get("api_key"),
        consumer_secret=TWITTER_CREDENTIALS.get("api_key_secret"),
        access_token=TWITTER_CREDENTIALS.get("access_token"),
        access_token_secret=TWITTER_CREDENTIALS.get("access_token_secret"),
    )
    try:
        tweets = client.search_recent_tweets(
            query, max_results=10, tweet_fields=tweet_fields
        )
        return tweets
    except tweepy.errors.Unauthorized:
        pass
