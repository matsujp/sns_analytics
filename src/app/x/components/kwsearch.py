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
        response = get_api_data(client, q, max_results)
        main_data = extract_data(response)
        return [main_data, 0]

    except Exception as e:
        return [e, 1]


def get_api_data(
    client,
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
        "tweet_fields": ["public_metrics"],
    }
    response = client.search_recent_tweets(**params)

    return response


def extract_data(response):

    print(response)
    if response.data is None:
        return []

    main_data = []
    for data in response.data:
        item_data = {}
        for key in ["id", "author_id", "text"]:
            item_data[key] = data[key]
        for key in data["public_metrics"]:
            item_data[key] = data["public_metrics"][key]
        user = [
            user
            for user in response.includes["users"]
            if user["id"] == item_data["author_id"]
        ][0]
        for key in ["name", "username", "url"]:
            item_data[key] = user[key]
        for key in user["public_metrics"]:
            item_data[key] = user["public_metrics"][key]
        main_data.append(item_data)

    return main_data
