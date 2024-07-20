import hmac
import urllib.parse as parse

import streamlit as st
import top
from instagram import instagram
from x import x

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


def oauth():
    AUTH_URL = "https://twitter.com/i/oauth2/authorize"
    RESPOSE_TYPE = "code"
    TWITTER_CLIENT_ID = "NVhxVW5ZbUtkeEczMFlKejAySmQ6MTpjaQ"
    # REDIRECT_URI = "https://sns-analytics-dev.onrender.com/"
    REDIRECT_URI = "https://sns-analytics-dev.onrender.com/"
    STATE = "state"
    SCOPE = ["tweet.read", "tweet.write", "users.read", "offline.access"]
    CODE_CHALLENGE = "challenge"
    CODE_CHALLENGE_METHOD = "code_challenge_method=plain"

    query_parameter = parse.urlencode(
        {
            "response_type": RESPOSE_TYPE,
            "client_id": TWITTER_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "state": STATE,
            "scope": " ".join(SCOPE),
            "code_challenge": CODE_CHALLENGE,
            "code_challenge_method": CODE_CHALLENGE_METHOD,
        }
    )

    request_url = f"{AUTH_URL}?{query_parameter}"

    st.markdown(
        "<h1 style='text-align: center; color: grey;'>Welcome to SNS Anlyzer</h1>",
        unsafe_allow_html=True,
    )
    st.columns(5)[2].link_button("Log In", request_url, use_container_width=True)


if not oauth():
    st.stop()  # Do not continue if check_password is not True.

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
