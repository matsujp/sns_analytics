import json
import os

import pyrebase
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

cfg = {
    "apiKey": os.getenv("FB_APIKEY"),
    "authDomain": os.getenv("FB_AUTHDOMAIN"),
    "databaseURL": os.getenv("FB_DATABASE_URL"),
    "storageBucket": os.getenv("FB_STRAGE_BUCKET"),
}
TRIAL_USER_ID = os.getenv("TRIAL_USER_ID")

firebase = pyrebase.initialize_app(cfg)
auth = firebase.auth()


def authenticate(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state["user"] = user

        if user["localId"] == TRIAL_USER_ID:
            st.session_state["trial"] = True
        else:
            st.session_state["trial"] = False

        return True

    except requests.exceptions.HTTPError as e:
        msg = json.loads(e.args[1])["error"]["message"]
        if msg == "EMAIL_NOT_FOUND" or msg == "INVALID_PASSWORD":
            st.error("メールアドレスかパスワードに誤りがあります。")
        elif msg == "USER_DISABLED":
            st.error("このユーザーは無効化されています。管理者にお問い合わせください。")
        elif msg == "TOO_MANY_ATTEMPTS_TRY_LATER":
            st.error("試行回数が多すぎます。しばらく経ってからお試しください。")
        else:
            st.error("ログインに失敗しました。")

        if "user" in st.session_state:
            del st.session_state["user"]
    return False


def refresh():
    if "user" not in st.session_state:
        return False
    try:
        user = auth.refresh(st.session_state.user["refreshToken"])
        st.session_state.user = user
        return True
    except Exception:
        del st.session_state.user
    return False
