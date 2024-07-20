import os

import streamlit as st
import tweepy
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SNS Analytics", page_icon="📈")


def x_oauth():
    TWITTER_CLIENT_ID = os.getenv("X_CLIENT_ID")
    REDIRECT_URI = "https://sns-analytics-dev.onrender.com/"
    SCOPE = [
        "tweet.read",
        "tweet.write",
        "users.read",
        "offline.access",
        "like.read",
        "bookmark.read",
        "bookmark.write",
    ]

    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=TWITTER_CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        client_secret=os.getenv("X_CLIENT_SECRET"),
    )

    x_request_url = oauth2_user_handler.get_authorization_url()

    return x_request_url


x_request_url = x_oauth()

st.markdown(
    "<h1 style='text-align: center; color: grey;'>Welcome to SNS Anlytics</h1>",
    unsafe_allow_html=True,
)
st.divider()

cols = st.columns(4)
cols[1].link_button("X (Twitter)", x_request_url, use_container_width=True)
cols[2].link_button("Instagram", x_request_url, disabled=True, use_container_width=True)
