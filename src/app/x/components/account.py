from tweepy.client import Client, Response

from . import authorization


def get_data(
    x_api_key,
    x_api_secret_key,
    x_access_token,
    x_access_token_secret,
    x_bearer_token,
    username_list,
):
    try:
        client = authorization.set_api_client(
            x_api_key,
            x_api_secret_key,
            x_access_token,
            x_access_token_secret,
            x_bearer_token,
        )
        response = get_api_data(client, username_list)
        data = extract_data(response)
        return [data, 0]

    except Exception as e:
        return [e, 1]


def get_api_data(
    client: Client,
    username_list: list[str],
):

    params = {
        "usernames": username_list,
        "expansions": "pinned_tweet_id",
        "tweet_fields": ["author_id", "created_at", "public_metrics"],
        "user_fields": [
            "created_at",
            "description",
            "entities",
            "id",
            "location",
            "most_recent_tweet_id",
            "name",
            "pinned_tweet_id," "profile_image_url",
            "protected",
            "public_metrics",
            "url",
            "verified",
            "verified_type",
            "withheld",
        ],
    }
    response = client.get_users(**params)

    return response


def extract_data(response: Response):
    if response.data is None:
        return []

    data = []
    for user in response.data:
        data_item = {}
        for key in ["id", "username", "name", "created_at", "url"]:
            data_item[key] = user[key]
        for key in user["public_metrics"]:
            data_item[key] = user["public_metrics"][key]
        tweets = [
            tweet
            for tweet in response.includes["tweets"]
            if tweet["author_id"] == data_item["id"]
        ]
        if len(tweets) > 0:
            tweet = tweets[0]
            for key in ["text", "created_at"]:
                data_item[key] = tweet[key]
            for key in tweet["public_metrics"]:
                data_item[key] = tweet["public_metrics"][key]
        data.append(data_item)

    return data
