import os
from urllib import parse

import acsearch
import actweet
import commingsoon
import kwsearch
import streamlit as st
import tweepy
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="X Analytics", page_icon="📈", layout="wide")

query_parameter = st.query_params
HOME_URL = os.getenv("HOME_URL")
REDIRECT_URI = os.getenv("X_REDIRECT_URL")
CLIENT_ID = os.getenv("X_CLIENT_ID")
CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")
# SCOPE = [
#     "tweet.read",
#     "tweet.write",
#     "users.read",
#     "offline.access",
#     "like.read",
#     "bookmark.read",
#     "bookmark.write",
# ]
SCOPE = ["tweet.read", "like.read", "bookmark.read", "users.read", "bookmark.write"]

if query_parameter == {}:
    st.columns(5)[2].link_button(
        "ホームへ戻る",
        HOME_URL,
        use_container_width=True,
    )
    st.stop()


oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    client_secret=CLIENT_SECRET,
)

query_parameter = parse.urlencode(st.query_params)
request_url = f"{REDIRECT_URI}?{query_parameter}"
oauth_token = oauth2_user_handler.fetch_token(request_url)
st.session_state["x_bearer_token"] = oauth_token

st.text(oauth_token)


if "x_api_key" not in st.session_state:
    st.session_state["x_api_key"] = ""
if "x_api_secret_key" not in st.session_state:
    st.session_state["x_api_secret_key"] = ""
if "x_access_token" not in st.session_state:
    st.session_state["x_access_token"] = ""
if "x_access_token_secret" not in st.session_state:
    st.session_state["x_access_token_secret"] = ""
# if "x_bearer_token" not in st.session_state:
#     st.session_state["x_bearer_token"] = ""
if "x_feature" not in st.session_state:
    st.session_state["x_feature"] = "キーワード検索"

with st.sidebar:
    st.title(":blue[X Analytics](仮)")
    st.divider()
    st.text_input(
        label="API Key",
        key="x_api_key",
        placeholder="API Keyを入力してください",
        value=st.session_state["x_api_key"],
    )
    st.text_input(
        label="API Secret Key",
        key="x_api_secret_key",
        placeholder="API Secret Keyを入力してください",
        value=st.session_state["x_api_secret_key"],
    )
    st.text_input(
        label="Bearer Token",
        key="x_bearer_token",
        placeholder="Bearer Tokenを入力してください",
        value=st.session_state["x_bearer_token"],
    )
    st.text_input(
        label="Access Token",
        key="x_access_token",
        placeholder="Access Tokenを入力してください",
        value=st.session_state["x_access_token"],
    )
    st.text_input(
        label="Access Token Secret",
        key="x_access_token_secret",
        placeholder="Access Token Secretを入力してください",
        value=st.session_state["x_access_token_secret"],
    )
    st.divider()

    st.radio(
        "Select feature",
        [
            "キーワード検索",
            "アカウント検索",
            "アカウント投稿取得",
            "Comming soon...",
        ],
        key="x_feature",
        captions=["", "", ""],
    )

if st.session_state["x_feature"] == "キーワード検索":
    kwsearch.page()
if st.session_state["x_feature"] == "アカウント検索":
    acsearch.page()
if st.session_state["x_feature"] == "アカウント投稿取得":
    actweet.page()
if st.session_state["x_feature"] == "Comming soon...":
    commingsoon.page()
