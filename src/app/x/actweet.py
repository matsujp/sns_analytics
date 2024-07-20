from datetime import date

import pandas as pd
import streamlit as st

from .components import actweet


def click_handler(
    x_api_key: str,
    x_api_secret_key: str,
    x_access_token: str,
    x_access_token_secret: str,
    x_bearer_token: str,
    username: str,
    start_date: date,
    end_date: date,
    ex_retweet_flag: bool,
    ex_reply_flag: bool,
    max_results: int,
):
    if username.replace(" ", "") == "":
        st.error("ユーザーネームを入力してください", icon="🚨")
        return

    st.session_state["x_kwsearch_data"], st.session_state["x_kwsearch_status"] = (
        actweet.get_data(
            x_api_key,
            x_api_secret_key,
            x_access_token,
            x_access_token_secret,
            x_bearer_token,
            username,
            start_date,
            end_date,
            ex_retweet_flag,
            ex_reply_flag,
            max_results,
        )
    )


def make_table():
    df = pd.DataFrame(st.session_state["x_kwsearch_data"])
    df.index = df.index + 1
    return df


def page():
    if "x_kwsearch_status" not in st.session_state:
        st.session_state["x_kwsearch_status"] = 0

    username = st.text_input(
        label="ユーザーネーム",
        placeholder="ユーザーネームを入力してください",
    )
    columns = st.columns(spec=3)
    start_date = columns[0].date_input(
        "取得開始日",
        value=date(
            year=date.today().year, month=date.today().month, day=date.today().day - 7
        ),
    )
    end_date = columns[1].date_input("取得終了日")
    max_results = columns[2].number_input(
        label="最大取得件数",
        min_value=10,
        max_value=100,
        step=1,
        value=10,
    )
    sub_columns = columns[0].columns(spec=2)
    ex_retweet_flag = sub_columns[0].checkbox("リツイート除外")
    ex_reply_flag = sub_columns[1].checkbox("リプライ除外")

    st.button(
        "データ取得",
        on_click=click_handler,
        args=[
            st.session_state["x_api_key"],
            st.session_state["x_api_secret_key"],
            st.session_state["x_access_token"],
            st.session_state["x_access_token_secret"],
            st.session_state["x_bearer_token"],
            username,
            start_date,
            end_date,
            ex_retweet_flag,
            ex_reply_flag,
            max_results,
        ],
    )

    if "x_kwsearch_data" in st.session_state:
        if st.session_state["x_kwsearch_status"] == 0:
            df = make_table()
            # MIN_HEIGHT = 27
            # MAX_HEIGHT = 800
            # ROW_HEIGHT = 35
            # AgGrid(df, height=min(MIN_HEIGHT + len(df) * ROW_HEIGHT, MAX_HEIGHT))
            st.dataframe(df, height=800)
        else:
            st.error(st.session_state["x_kwsearch_data"], icon="🚨")
