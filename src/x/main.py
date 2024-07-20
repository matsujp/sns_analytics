import acsearch
import actweet
import commingsoon
import kwsearch
import streamlit as st

st.set_page_config(page_title="X Analytics", page_icon="📈", layout="wide")


if "x_api_key" not in st.session_state:
    st.session_state["x_api_key"] = ""
if "x_api_secret_key" not in st.session_state:
    st.session_state["x_api_secret_key"] = ""
if "x_access_token" not in st.session_state:
    st.session_state["x_access_token"] = ""
if "x_access_token_secret" not in st.session_state:
    st.session_state["x_access_token_secret"] = ""
if "x_bearer_token" not in st.session_state:
    st.session_state["x_bearer_token"] = ""
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
