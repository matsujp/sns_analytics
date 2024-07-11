import numpy as np
import pandas as pd
import streamlit as st


def page():
    st.button("change")
    df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))

    st.table(df)
