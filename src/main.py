import hmac

import streamlit as st

from components import instagram, top, x

st.set_page_config(page_title="SNS Analyzer", page_icon="📈", layout="wide")


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


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here

sns_type = st.sidebar.selectbox("Chose SNS", ("-", "X"))

if sns_type == "-":
    top.page()
if sns_type == "X":
    x.page()
if sns_type == "Instagram":
    instagram.page()
