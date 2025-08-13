import sqlite3
import pandas as pd
import streamlit as st
#Centralizing input field
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

# Function to run a SQL query and return resulting df
def queryintoDF(query):
    with sqlite3.connect('balance_sheet.db') as conn:
        df = pd.read_sql_query(query, conn)
        return df

q1 = """SELECT DISTINCT NOME_INSTITUICAO as Cooperativa FROM bp ORDER BY NOME_INSTITUICAO"""
q2 = "SELECT DISTINCT CONTA as Conta, NOME_CONTA as Nome FROM bp ORDER BY CONTA"
q3 = """SELECT DATA_BASE as Mês, ROUND(sum(saldo)/1000,2) as Saldo_Consolidado FROM bp WHERE (CONTA = 10000000 OR CONTA = 20000000 OR CONTA = 30000000) GROUP BY DATA_BASE"""
q4 = "SELECT DATA_BASE as Mês, ROUND(sum(saldo)/1000,2) as Saldo_Consolidado FROM bp WHERE CONTA = 40000000 GROUP BY DATA_BASE"
q5 = "SELECT DATA_BASE as Mês, ROUND(sum(saldo)/1000,2) as Saldo_Consolidado FROM bp WHERE CONTA = 60000000 GROUP BY DATA_BASE"
q6 = "SELECT DATA_BASE as Mês, NOME_INSTITUICAO as Cooperativa, SUM(CASE WHEN CONTA IN (11000000, 12000000) THEN saldo ELSE 0 END)/NULLIF(SUM(CASE WHEN CONTA in (41100000,44000000) THEN saldo ELSE 0 END), 0) AS indice FROM bp GROUP BY DATA_BASE, CNPJ"
q7 = """SELECT DATA_BASE as Mês, ROUND(AVG(indice), 3) AS media_indice FROM (SELECT DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA IN (11000000, 12000000) THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (41100000,44000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10 ELSE SUM(CASE WHEN CONTA IN (11000000, 12000000) THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (41100000,44000000) THEN saldo ELSE 0 END), 0) END AS indice FROM bp GROUP BY DATA_BASE, CNPJ) GROUP BY DATA_BASE"""
q8 = "SELECT DATA_BASE as Mês, NOME_INSTITUICAO as Cooperativa, SUM(CASE WHEN CONTA = 10000000 THEN saldo ELSE 0 END)/NULLIF(SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END), 0) AS indice FROM bp GROUP BY DATA_BASE, CNPJ"
q9 = """SELECT DATA_BASE as Mês, ROUND(AVG(indice), 3) AS media_indice FROM (SELECT DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA = 10000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END), 0) > 5 THEN 5 ELSE SUM(CASE WHEN CONTA = 10000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END), 0) END AS indice FROM bp GROUP BY DATA_BASE, CNPJ) GROUP BY DATA_BASE"""
q10 = """SELECT DATA_BASE as Mês, NOME_INSTITUICAO as Cooperativa, CASE WHEN SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10 ELSE SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) END AS indice FROM bp GROUP BY DATA_BASE, CNPJ"""
q11 = """SELECT DATA_BASE as Mês, ROUND(AVG(indice), 4) AS media_indice FROM (SELECT DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10 ELSE SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) END AS indice FROM bp GROUP BY DATA_BASE, CNPJ) GROUP BY DATA_BASE"""
q12 = """SELECT DATA_BASE as Mês, ROUND(AVG(indice), 4) AS media_indice FROM (SELECT DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10 ELSE SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) END AS indice FROM bp GROUP BY DATA_BASE, CNPJ) GROUP BY DATA_BASE"""
queries_dict = {
    "Nomes das Cooperativas": q1,
    "Contas do Balanço Patrimonial": q2,
    "Soma dos Ativos por Mês": q3,
    "Soma dos Passivos por Mês": q4,
    "Patrimônio Líquido por Mês": q5,
    "Índice de Liquidez Imediata": q6,
    "Média do Índice de Liquidez Imediata": q7,
    "Índice de Liquidez Corrente": q8,
    "Média do Índice de Liquidez Corrente": q9,
    "Índice de Endividamento Geral": q10,
    "Média do Índice de Endividamento Geral": q11,
    "Média do Índice de Endividamento Geral": q12
}
# Load CSV data into the SQLite database
conn = sqlite3.connect('balance_sheet.db')
bp_df = pd.read_sql("SELECT * FROM bp", conn)

# Begin Streamlit app
st.markdown("# Explore o Balanço Patrimonial")
col1,col2 = st.columns(2)
with col1:
    data = st.multiselect("Selecione o período", bp_df["DATA_BASE"].unique(),default=bp_df["DATA_BASE"].unique()[0])
with col2:  
    name = st.selectbox("Selecione o nome da cooperativa", bp_df["NOME_INSTITUICAO"].unique())

# Filter the DataFrame based on user input
df_filtered = bp_df[(bp_df["NOME_INSTITUICAO"] == name) & (bp_df["DATA_BASE"].isin(data))]
st.dataframe(df_filtered[["CONTA", "NOME_CONTA", "SALDO"]])

# Display the queries in expandable sections
st.markdown("## Consultas Disponíveis")
st.markdown("Selecione uma consulta abaixo para visualizar os resultados.")

tab1, tab2, tab3 = st.tabs(["Informações Gerais", "Liquidez", "Endividamento"])

with tab1:
    for i in ["Nomes das Cooperativas", "Contas do Balanço Patrimonial", "Soma dos Ativos por Mês", "Soma dos Passivos por Mês", "Patrimônio Líquido por Mês"]:
        with st.expander(i):
            query = queries_dict[i]
            try:
                result_df = queryintoDF(query)
                st.dataframe(result_df,hide_index=True)
                st.code(query, language='sql')
            except Exception as e:
                st.error(f"Erro ao executar a consulta: {e}")
with tab2:
    for i in ["Índice de Liquidez Imediata", "Média do Índice de Liquidez Imediata", "Índice de Liquidez Corrente", "Média do Índice de Liquidez Corrente"]:
        with st.expander(i):
            query = queries_dict[i]
            try:
                result_df = queryintoDF(query)
                st.dataframe(result_df,hide_index=True)
                st.code(query, language='sql')
            except Exception as e:
                st.error(f"Erro ao executar a consulta: {e}")
with tab3:
    for i in ["Índice de Endividamento Geral", "Média do Índice de Endividamento Geral"]:
        with st.expander(i):
            query = queries_dict[i]
            try:
                result_df = queryintoDF(query)
                st.dataframe(result_df,hide_index=True)
                st.code(query, language='sql')
            except Exception as e:
                st.error(f"Erro ao executar a consulta: {e}")

st.divider()
# Add a text input for custom SQL queries
st.markdown("<h2 style='text-align: center;'>Faça a sua consulta</h2>", unsafe_allow_html=True)
input_query = st.text_input("", "SELECT * FROM bp")
col1, col2, col3 = st.columns([6,4,6])
with col2:
    a = st.button("Executar Consulta")
if a:
    try:
        result_df = queryintoDF(input_query)
        st.dataframe(result_df)
    except Exception as e:
        st.error(f"Erro ao executar a consulta: {e}")