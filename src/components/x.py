import numpy as np
import pandas as pd
import streamlit as st


def page():

    feature = st.sidebar.radio(
        "select feature",
        ["機能A", "機能B", "機能C"],
        key="feature",
        captions=["", "", ""],
    )

    if feature == "機能A":
        st.text_input("")
        st.button("change")
        df = pd.DataFrame(
            np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
        )

        st.table(df)
    if feature == "機能B":
        st.text_input("")
        st.button("change")
        df = pd.DataFrame(
            np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
        )

        st.table(df)
    if feature == "機能C":
        st.text_input("")
        st.button("change")
        df = pd.DataFrame(
            np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
        )

        st.table(df)
