import sqlite3
import pandas as pd
import streamlit as st

def run_query(query):
    with sqlite3.connect('C:/Users/eduar/case.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        r = cursor.fetchall()
        for row in r:
            print(row)


conn = sqlite3.connect('C:/Users/eduar/case.db')
cursor = conn.cursor()

#Quais são os nomes das cooperativas de crédito presentes no banco de dados ordenadas alfabeticamente?
run_query("""SELECT DISTINCT NOME_INSTITUICAO FROM bp ORDER BY NOME_INSTITUICAO""")

#Quais são os nomes das contas presentes no banco de dados, ordernar pelo índice das contas?
run_query("SELECT DISTINCT CONTA, NOME_CONTA FROM bp ORDER BY CONTA")

#Qual a soma do ativo de todas as cooperativas de crédito em cada mês de referência?
run_query("""SELECT DATA_BASE, ROUND(sum(saldo)/1000,2) FROM bp WHERE (CONTA = 10000000 OR CONTA = 20000000 OR CONTA = 30000000) GROUP BY DATA_BASE""")

#Qual a soma do passivo exigível as cooperativas de crédito em cada mês de referência?
run_query("SELECT DATA_BASE, ROUND(sum(saldo)/1000,2) FROM bp WHERE CONTA = 40000000 GROUP BY DATA_BASE")

#Qual o patrimônio líquido de todas as cooperativas de crédito em cada mês de referência?
run_query("SELECT DATA_BASE, ROUND(sum(saldo)/1000,2) FROM bp WHERE CONTA = 60000000 GROUP BY DATA_BASE")

#Qual o índice de liquidez imediata de todas as cooperativas de crédito em cada mês de referência?
print("Índice de Liquidez Imediata:")
run_query("SELECT DATA_BASE, CNPJ, SUM(CASE WHEN CONTA IN (11000000, 12000000) THEN saldo ELSE 0 END)/NULLIF(SUM(CASE WHEN CONTA in (41100000,44000000) THEN saldo ELSE 0 END), 0) AS indice FROM bp GROUP BY DATA_BASE, CNPJ")

#Média do índice de liquidez imediata de todas as cooperativas de crédito em cada mês de referência
print("Índice de Liquidez Imediata:")
run_query("""
    SELECT DATA_BASE, ROUND(AVG(indice), 3) AS media_indice FROM 
        (SELECT 
            DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA IN (11000000, 12000000) THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (41100000,44000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10
                ELSE SUM(CASE WHEN CONTA IN (11000000, 12000000) THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (41100000,44000000) THEN saldo ELSE 0 END), 0) END AS indice
        FROM bp
        GROUP BY DATA_BASE, CNPJ
        )
    GROUP BY DATA_BASE
""")

#Liquidez Corrente de todas as cooperativas de crédito em cada mês de referência
print("Liquidez Corrente:")
run_query("SELECT DATA_BASE, CNPJ, SUM(CASE WHEN CONTA = 10000000 THEN saldo ELSE 0 END)/NULLIF(SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END), 0) AS indice FROM bp GROUP BY DATA_BASE, CNPJ")

#Média do índice de liquidez corrente de todas as cooperativas de crédito em cada mês de referência
print("Média do índice de liquidez corrente:")  
run_query("""
    SELECT DATA_BASE, ROUND(AVG(indice), 3) AS media_indice FROM 
        (SELECT 
            DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA = 10000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END), 0) > 5 THEN 5
                ELSE SUM(CASE WHEN CONTA = 10000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END), 0) END AS indice
        FROM bp
        GROUP BY DATA_BASE, CNPJ
        )
    GROUP BY DATA_BASE
""")

#Qual o índice de individamento de todas as cooperativas de crédito em cada mês de referência?