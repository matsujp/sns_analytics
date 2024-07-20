import hmac
import os
from urllib import parse

import streamlit as st
import top
import tweepy
from dotenv import load_dotenv
from instagram import instagram
from x import x

load_dotenv()

st.set_page_config(page_title="SNS Analytics", page_icon="📈", layout="wide")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        for id, pw in st.secrets["accounts"]:
            if hmac.compare_digest(st.session_state["id"], id) and hmac.compare_digest(
                st.session_state["pw"], pw
            ):
                st.session_state["login_correct"] = True
                del st.session_state["pw"]  # Don't store the password.
                break
            else:
                st.session_state["login_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("login_correct", False):
        return True

    # Show input for password.
    st.text_input("E-mail", type="default", key="id")
    st.text_input("Password", type="password", key="pw")
    st.button("login", on_click=password_entered)
    if "login_correct" in st.session_state:
        st.error("😕 E-mail または Password が正しくありません")
    return False


def oauth2():
    REDIRECTED_URL = "https://sns-analytics-dev.onrender.com/"
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    print(CLIENT_ID)
    print(CLIENT_SECRET)
    if st.session_state.get("login_correct", False):
        return True

    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECTED_URL,
        scope=[
            "tweet.read",
            "like.read",
            "bookmark.read",
            "users.read",
            "bookmark.write",
        ],
        client_secret=CLIENT_SECRET,
    )

    st.markdown(
        "<h1 style='text-align: center; color: grey;'>Welcome to SNS Anlyzer</h1>",
        unsafe_allow_html=True,
    )
    st.columns(5)[2].link_button(
        "Login", oauth2_user_handler.get_authorization_url(), use_container_width=True
    )

    query_params = parse.urlencode(st.query_params)
    oauth2_user_handler.fetch_token(f"{REDIRECTED_URL}?{query_params}")

    return False


if not oauth2():
    st.stop()

# Main Streamlit app starts here

if "sns_type" not in st.session_state:
    st.session_state["sns_type"] = "-"

with st.sidebar:
    st.title(":blue[SNS Analytics](仮)")
    st.divider()
    st.selectbox("Choose SNS", ("-", "X (Twitter)"), key="sns_type")

if st.session_state["sns_type"] == "-":
    top.page()
if st.session_state["sns_type"] == "X (Twitter)":
    x.page()
if st.session_state["sns_type"] == "Instagram":
    instagram.page()
