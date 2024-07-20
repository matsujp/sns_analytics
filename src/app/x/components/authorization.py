import tweepy
from tweepy.client import Client


def set_api_client(
    x_api_key,
    x_api_secret_key,
    x_access_token,
    x_access_token_secret,
    x_bearer_token,
) -> Client:
    client = tweepy.Client(
        bearer_token=x_bearer_token,
        consumer_key=x_api_key,
        consumer_secret=x_api_secret_key,
        access_token=x_access_token,
        access_token_secret=x_access_token_secret,
    )
    return client
