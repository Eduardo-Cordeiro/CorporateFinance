# CorporateFinance
Measuring Liquidity and Capital Indicators for Financial Institutions

## Data
In this mini-project, we will use a five-month dataset of Brazilian credit union balance sheets obtained from the Central Bank of Brazil (BACEN) [Bacen Balance Sheets](https://www.bcb.gov.br/estabilidadefinanceira/balancetesbalancospatrimoniais)

After downloading the [balance sheets](https://www.bcb.gov.br/estabilidadefinanceira/balancetesbalancospatrimoniais) for each month (February, March, April, and May of 2025), they were merged into a single file named 'balance_sheets.csv'.

The balance sheets available from BACEN are constituted by COSIF accounts, you can get the description for each account in this [link](https://www3.bcb.gov.br/aplica/cosif)

## Exploring Data
After the data was prepared we begin to explore our dataset.

The `explore.py` script is used for loading, processing, and analyzing the balance sheet data of Brazilian credit unions. It imports the merged CSV file into a SQLite database and provides several SQL queries to explore key financial indicators, such as assets, liabilities, equity, and liquidity ratios. The script includes utility functions to run SQL queries and display results, making it easy to extract insights and perform custom analyses

