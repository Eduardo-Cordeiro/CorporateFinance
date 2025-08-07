import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect('C:/Users/eduar/case.db')

bp_df = pd.read_sql("SELECT * FROM bp;", conn)

contas = bp_df["NOME_CONTA"].unique()
st.dataframe(bp_df)

st.markdown("# Balanço Patrimonial")

col1,col2 = st.columns(2)
with col1:
    st.selectbox("Selecione o período", bp_df["DATA_BASE"].unique())
with col2:  
    st.selectbox("Selecione a conta", contas)