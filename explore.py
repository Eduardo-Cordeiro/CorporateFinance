import sqlite3
import pandas as pd
import streamlit as st

def run_query(query):
    with sqlite3.connect('balance_sheet.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        r = cursor.fetchall()
        for row in r:
            print(row)

def queryintoDF(query):
    with sqlite3.connect('balance_sheet.db') as conn:
        df = pd.read_sql_query(query, conn)
        return df

# Load CSV data into the SQLite database
bs = pd.read_csv("balance_sheets.csv",sep=";")
conn = sqlite3.connect('balance_sheet.db')
bs.to_sql('bp', conn, if_exists='replace', index=False)
cursor = conn.cursor()

# What are the names of the credit unions present in the database, ordered alphabetically?
run_query("""SELECT DISTINCT NOME_INSTITUICAO FROM bp ORDER BY NOME_INSTITUICAO""")

# What are the names of the accounts present in the database, ordered by the account index?
run_query("SELECT DISTINCT CONTA, NOME_CONTA FROM bp ORDER BY CONTA")

# What is the sum of assets of all credit unions for each reference month?
run_query("""SELECT DATA_BASE, ROUND(sum(saldo)/1000,2) FROM bp WHERE (CONTA = 10000000 OR CONTA = 20000000 OR CONTA = 30000000) GROUP BY DATA_BASE""")

# What is the sum of liabilities payable by the credit unions for each reference month?
run_query("SELECT DATA_BASE, ROUND(sum(saldo)/1000,2) FROM bp WHERE CONTA = 40000000 GROUP BY DATA_BASE")

# What is the equity of all credit unions for each reference month?
run_query("SELECT DATA_BASE, ROUND(sum(saldo)/1000,2) FROM bp WHERE CONTA = 60000000 GROUP BY DATA_BASE")

# What is the immediate liquidity ratio of all credit unions for each reference month?
print("Immediate Liquidity Ratio:")
run_query("SELECT DATA_BASE, CNPJ, SUM(CASE WHEN CONTA IN (11000000, 12000000) THEN saldo ELSE 0 END)/NULLIF(SUM(CASE WHEN CONTA in (41100000,44000000) THEN saldo ELSE 0 END), 0) AS indice FROM bp GROUP BY DATA_BASE, CNPJ")

# Average immediate liquidity ratio of all credit unions for each reference month
print("Immediate Liquidity Ratio:")
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

# Current liquidity ratio of all credit unions for each reference month
print("Current Liquidity Ratio:")
run_query("SELECT DATA_BASE, CNPJ, SUM(CASE WHEN CONTA = 10000000 THEN saldo ELSE 0 END)/NULLIF(SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END), 0) AS indice FROM bp GROUP BY DATA_BASE, CNPJ")

# Average current liquidity ratio of all credit unions for each reference month
print("Average Current Liquidity Ratio:")  
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

# What is the debt ratio of each credit union for each reference month?
print("Debt Ratio (Liabilities/Assets):")
run_query("""SELECT 
            DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10
                ELSE SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) END AS indice
        FROM bp
        GROUP BY DATA_BASE, CNPJ
        """)

# What is the debt ratio of all credit unions for each reference month?
print("Debt Ratio (Liabilities/Assets):")
a = run_query("""
    SELECT DATA_BASE, ROUND(AVG(indice), 4) AS media_indice FROM 
        (SELECT 
            DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10
                ELSE SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) END AS indice
        FROM bp
        GROUP BY DATA_BASE, CNPJ
        )
    GROUP BY DATA_BASE
""")

a = queryintoDF("""
    SELECT DATA_BASE, ROUND(AVG(indice), 4) AS media_indice FROM 
        (SELECT 
            DATA_BASE, CNPJ, CASE WHEN SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) > 10 THEN 10
                ELSE SUM(CASE WHEN CONTA = 40000000 THEN saldo ELSE 0 END) / NULLIF(SUM(CASE WHEN CONTA in (10000000, 20000000, 30000000) THEN saldo ELSE 0 END), 0) END AS indice
        FROM bp
        GROUP BY DATA_BASE, CNPJ
        )
    GROUP BY DATA_BASE
""")
print(a.head())