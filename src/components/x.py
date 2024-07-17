import numpy as np
import pandas as pd
import streamlit as st


def page():

    feature = st.sidebar.radio(
        "Select feature",
        ["🔍検索リサーチ(例)", "🙍アカウント分析(例)", "📚ツイート取得(例)"],
        key="feature",
        captions=["", "", ""],
    )

    if feature == "機能A":
        st.button("change")
        df = pd.DataFrame(
            np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
        )

        st.table(df)
    if feature == "🙍アカウント分析(例)":
        st.subheader("graph B")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

        st.line_chart(chart_data)
        st.table(chart_data)

    if feature == "機能C":
        st.subheader("graph C")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

        st.bar_chart(chart_data)
