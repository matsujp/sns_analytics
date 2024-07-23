import streamlit as st

import firebase
from instagram import instagram
from top import top
from x import x

st.set_page_config(page_title="SNS Analytics", page_icon="📈", layout="wide")


def login():
    with st.columns(3)[1]:
        email = st.empty()
        email = email.text_input(
            "Emailアドレス", placeholder="Emailアドレスを入力してください"
        )
        password = st.text_input(
            "パスワード", placeholder="パスワードを入力してください", type="password"
        )
        submit = st.button("ログイン")
        if submit and firebase.authenticate(email, password):
            st.rerun()


if "user" not in st.session_state:
    st.markdown(
        "<h1 style='text-align: center; color: grey;'>Welcome to SNS Anlytics(仮)</h1>",
        unsafe_allow_html=True,
    )
    st.divider()
    login()
    st.stop()

with st.sidebar:
    st.title(":blue[SNS Analytics](仮)")
    st.divider()
    st.selectbox("Select SNS", ("-", "X (Twitter)"), key="selected_sns")

if st.session_state["selected_sns"] == "-":
    top.page()
if st.session_state["selected_sns"] == "X (Twitter)":
    x.page()
if st.session_state["selected_sns"] == "Instagram":
    instagram.page()
