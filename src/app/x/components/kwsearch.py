from tweepy.client import Client, Response

from . import authorization


def get_data(
    x_api_key,
    x_api_secret_key,
    x_access_token,
    x_access_token_secret,
    x_bearer_token,
    q,
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
        response = _call_api(client, q, max_results)
        data = _extract_data(response)
        return [data, 0]

    except Exception as e:
        return [e, 1]


def _call_api(
    client: Client,
    q,
    max_results,
):

    params = {
        "query": q,
        "max_results": max_results,
        "expansions": [
            "author_id",
            "referenced_tweets.id",
            "entities.mentions.username",
            "in_reply_to_user_id",
            "referenced_tweets.id.author_id",
        ],
        "user_fields": ["description", "url", "public_metrics"],
        "tweet_fields": ["created_at", "public_metrics"],
    }
    response = client.search_recent_tweets(**params)

    return response


def _extract_data(response: Response):
    if response.data is None:
        return []

    data = []
    for tweet in response.data:
        data_item = {}
        for key in ["created_at", "author_id", "text"]:
            data_item[key] = tweet[key]
        for key in tweet["public_metrics"]:
            data_item[key] = tweet["public_metrics"][key]
        user = [
            user
            for user in response.includes["users"]
            if user["id"] == data_item["author_id"]
        ][0]
        for key in ["name", "username", "url"]:
            data_item[key] = user[key]
        for key in user["public_metrics"]:
            data_item[key] = user["public_metrics"][key]
        data.append(data_item)

    return data
