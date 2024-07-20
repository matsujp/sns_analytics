from datetime import date, datetime

from tweepy.client import Client, Response

from . import authorization


def get_data(
    x_api_key,
    x_api_secret_key,
    x_access_token,
    x_access_token_secret,
    x_bearer_token,
    username,
    start_date,
    end_date,
    ex_retweet_flag,
    ex_reply_flag,
    max_results,
):
    try:
        client = authorization.set_api_client(
            x_api_key,
            x_api_secret_key,
            x_access_token,
            x_access_token_secret,
            x_bearer_token,
        )
        response = _call_api(
            client,
            username,
            start_date,
            end_date,
            ex_retweet_flag,
            ex_reply_flag,
            max_results,
        )
        data = _extract_data(response)
        return [data, 0]

    except Exception as e:
        return [e, 1]


def _call_api(
    client: Client,
    username: str,
    start_date: date,
    end_date: date,
    ex_retweet_flag: bool,
    ex_reply_flag: bool,
    max_results: int,
):
    response = client.get_users(usernames=username)
    if len(response.errors) > 0:
        raise Exception(response.errors[0]["detail"])

    id = response.data[0]["id"]

    start_time = datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        hour=0,
        minute=0,
        second=0,
    )
    end_time = datetime(
        year=end_date.year,
        month=end_date.month,
        day=end_date.day,
        hour=23,
        minute=59,
        second=59,
    )

    params = {
        "id": id,
        "start_time": start_time,
        "end_time": end_time,
        "max_results": max_results,
        "expansions": "referenced_tweets.id",
        "tweet_fields": ["created_at", "public_metrics", "text"],
    }

    exclude = []
    if ex_retweet_flag:
        exclude.append("retweets")
    if ex_reply_flag:
        exclude.append("replies")

    if len(exclude) > 0:
        params["exclude"] = exclude

    response = client.get_users_tweets(**params)

    return response


def _extract_data(response: Response):
    if response.data is None:
        return []

    data = []
    for tweet in response.data:
        data_item = {}
        for key in ["created_at", "text"]:
            data_item[key] = tweet[key]
        for key in tweet["public_metrics"]:
            data_item[key] = tweet["public_metrics"][key]

        data.append(data_item)

    return data
