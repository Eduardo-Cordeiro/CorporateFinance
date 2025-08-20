# CorporateFinance
Measuring Liquidity and Capital Indicators for Financial Institutions

## Data
In this mini-project, we will use a five-month dataset of Brazilian credit union balance sheets obtained from the Central Bank of Brazil (BACEN).

After downloading the [balance sheets](https://www.bcb.gov.br/estabilidadefinanceira/balancetesbalancospatrimoniais) for each month (February, March, April, and May of 2025), they were merged into a single file named 'balance_sheets.csv'.

The balance sheets available from BACEN are constituted by COSIF accounts, you can get the description for each account in this [link](https://www3.bcb.gov.br/aplica/cosif)

## Exploring Data
After the data was prepared we begin to explore our dataset.

The `explore.py` script is used for loading, processing, and analyzing the balance sheet data of Brazilian credit unions. It imports the merged CSV file into a SQLite database and provides several SQL queries to explore key financial indicators, such as assets, liabilities, equity, and liquidity ratios. The script includes utility functions to run SQL queries and display results, making it easy to extract insights and perform custom analyses.

**Note:** The ratios obtained from the queries are not exact representations of the concepts they were originally intended to capture, but rather approximations. While the project aims to demonstrate how these financial concepts can be queried using SQL, the calculations are not as refined as they could be.

## Visualizing Data
The `st_app.py` script provides an interactive web interface for visualizing and querying the balance sheet data using Streamlit. Users can filter data by period and institution, view account balances, and execute custom SQL queries directly from the browser. The app displays results in a user-friendly format, making it easy to analyze.

You can access the app through this [link](https://corporatefinance-ftaofx9a7pp6m2dfqiybgc.streamlit.app/).