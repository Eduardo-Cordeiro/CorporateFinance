import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect('C:/Users/eduar/case.db')

bp_df = pd.read_sql("SELECT * FROM bp", conn)

contas = bp_df["NOME_CONTA"].unique()
st.dataframe(bp_df)

st.markdown("# Balanço Patrimonial")

col1,col2 = st.columns(2)
with col1:
    data = st.multiselect("Selecione o período", bp_df["DATA_BASE"].unique(),default="202502")
with col2:  
    name = st.selectbox("Selecione o nome da cooperativa", bp_df["NOME_INSTITUICAO"].unique())

df_filtered = bp_df[(bp_df["NOME_INSTITUICAO"] == name) & (bp_df["DATA_BASE"].isin(data))]

st.dataframe(df_filtered[["CONTA", "NOME_CONTA", "SALDO"]])