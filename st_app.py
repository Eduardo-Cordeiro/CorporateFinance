import sqlite3
import pandas as pd
import streamlit as st
st.markdown(
    """
    <style>
    /* Target the input box placeholder text */
    div[data-baseweb="input"] input {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def queryintoDF(query):
    with sqlite3.connect('balance_sheet.db') as conn:
        df = pd.read_sql_query(query, conn)
        return df

conn = sqlite3.connect('balance_sheet.db')

bp_df = pd.read_sql("SELECT * FROM bp", conn)

contas = bp_df["NOME_CONTA"].unique()

st.markdown("# Balanço Patrimonial")

col1,col2 = st.columns(2)
with col1:
    data = st.multiselect("Selecione o período", bp_df["DATA_BASE"].unique(),default=bp_df["DATA_BASE"].unique()[0])
with col2:  
    name = st.selectbox("Selecione o nome da cooperativa", bp_df["NOME_INSTITUICAO"].unique())

df_filtered = bp_df[(bp_df["NOME_INSTITUICAO"] == name) & (bp_df["DATA_BASE"].isin(data))]

st.dataframe(df_filtered[["CONTA", "NOME_CONTA", "SALDO"]])

st.markdown("<h2 style='text-align: center;'>Faça a sua consulta</h2>", unsafe_allow_html=True)

query = st.text_input("", "SELECT * FROM bp")

col1, col2, col3 = st.columns([6,4,6])
with col2:
    a = st.button("Executar Consulta")
if a:
    try:
        result_df = queryintoDF(query)
        st.dataframe(result_df)
    except Exception as e:
        st.error(f"Erro ao executar a consulta: {e}")