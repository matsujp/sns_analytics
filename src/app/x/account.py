import pandas as pd
import streamlit as st

from .components import account


def make_table(data):
    df = pd.DataFrame(data)
    df = df.drop(columns=["id"])
    df.index = df.index + 1
    return df


def click_handler(
    x_api_key: str,
    x_api_secret_key: str,
    x_access_token: str,
    x_access_token_secret: str,
    x_bearer_token: str,
    username_list: list[str],
):
    if len(username_list) == 0:
        st.error("検索ユーザーネームを入力してください", icon="🚨")
        return

    st.session_state["x_account_data"], st.session_state["x_account_status"] = (
        account.get_data(
            x_api_key,
            x_api_secret_key,
            x_access_token,
            x_access_token_secret,
            x_bearer_token,
            username_list,
        )
    )


def page():
    if "x_account_input" not in st.session_state:
        st.session_state["x_account_input"] = pd.DataFrame([{"username": ""}])

    st.text("検索ユーザーネームリスト")
    df = st.data_editor(
        st.session_state["x_account_input"],
        num_rows="dynamic",
        use_container_width=True,
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
            df["username"].dropna().tolist(),
        ],
    )

    if "x_account_data" in st.session_state:
        df = make_table(st.session_state["x_account_data"])
        st.dataframe(df)
