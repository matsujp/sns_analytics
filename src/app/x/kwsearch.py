import pandas as pd
import streamlit as st

from .components import actweet

# from st_aggrid import AgGrid


def click_handler(
    x_api_key: str,
    x_api_secret_key: str,
    x_access_token: str,
    x_access_token_secret: str,
    x_bearer_token: str,
    q: str,
    max_results: int,
):
    if q.replace(" ", "") == "":
        st.error("検索キーワードを入力してください", icon="🚨")
        return

    st.session_state["x_actweet_data"], st.session_state["x_actweet_status"] = (
        actweet.get_data(
            x_api_key,
            x_api_secret_key,
            x_access_token,
            x_access_token_secret,
            x_bearer_token,
            q,
            max_results,
        )
    )


def make_table():
    df = pd.DataFrame(st.session_state["x_actweet_data"])
    df = df.drop(columns=["author_id"])
    df.index = df.index + 1
    return df


def page():
    if "x_actweet_kw" not in st.session_state:
        st.session_state["x_actweet_kw"] = ""
    if "x_actweet_status" not in st.session_state:
        st.session_state["x_actweet_status"] = 0

    st.text_input(
        label="検索キーワード",
        value=st.session_state["x_actweet_kw"],
        placeholder="キーワードを入力してください",
        key="x_actweet_kw",
    )
    st.number_input(
        label="最大取得件数",
        min_value=10,
        max_value=100,
        step=1,
        value=10,
        key="x_actweet_getnum",
    )
    st.button(
        "データ取得",
        on_click=click_handler,
        args=[
            st.session_state["x_api_key"],
            st.session_state["x_api_secret_key"],
            st.session_state["x_access_token"],
            st.session_state["x_access_token_secret"],
            st.session_state["x_bearer_token"],
            st.session_state["x_actweet_kw"],
            st.session_state["x_actweet_getnum"],
        ],
    )

    if "x_actweet_data" in st.session_state:
        if st.session_state["x_actweet_status"] == 0:
            df = make_table()
            # MIN_HEIGHT = 27
            # MAX_HEIGHT = 800
            # ROW_HEIGHT = 35
            # AgGrid(df, height=min(MIN_HEIGHT + len(df) * ROW_HEIGHT, MAX_HEIGHT))
            st.dataframe(df, height=800)
        else:
            st.error(st.session_state["x_actweet_data"], icon="🚨")
