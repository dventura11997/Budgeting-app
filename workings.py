import pandas as pd
from datetime import datetime
import numpy as np

df = pd.read_csv('C:/Users/danie/OneDrive/Work/Career/Coding/Folio/Budgeting app/data/Raw/26_oct_24/budgeting_data_raw.csv')
#Drop unnecesary columns
df.drop(['SmartPlan status'], axis=1, inplace=True)
#Rename columns
df = df.rename(columns={
    'Date. This column is sortable sorted descending': 'Date',
    'Debit. This column is sortable': 'Debit',
    'Credit. This column is sortable': 'Credit',
    'Description. This column is sortable': 'Description',
    'Balance\xa0Footnote message1': 'Balance'
})
# Troubleshooting block for the 'Balance Footnote message1' column
# balance_column = [col for col in df.columns if 'Balance' in col]
# print(balance_column)

#Convert columns to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')

#Create Amount column through coalesce of debit and credit
df['Amount'] = df['Debit'].combine_first(df['Credit'])
#Convert amount to float (number)
df['Amount'] = df['Amount'].replace({'\$': '', ',': ''}, regex=True).astype(float)
#Use numpt where statement
df['Amount'] = np.where(df['Amount'] < 0, df['Amount'] * -1, df['Amount'])

df['Debit_credit'] = np.where(pd.notna(df['Debit']), 'Debit', 'Credit')

conditions = [
    df['Description'].str.contains('Maxxia|Southern Health', case=False, na=False),  # Chant pay
    df['Description'].str.contains('COVAU', case=False, na=False),   # Gas and electricity bills
    df['Description'].str.contains('Dyson|Kmart|Kogan|SoapBarRichmnd', case=False, na=False),  # Purchases combined
    df['Description'].str.contains('Netflix|stan.com.au|Disney', case=False, na=False),  # Streaming combined
    df['Description'].str.contains('Spintel', case=False, na=False),    # Wifi
    df['Description'].str.contains('Rocket Repa', case=False, na=False),  # Extra mortgage repayment
    df['Description'].str.contains('Westpac', case=False, na=False),   # Mortgage payment
    df['Description'].str.contains('Chantelle|Daniel Ven', case=False, na=False),  # Fortnightly budget payment combined
    df['Description'].str.contains('Homeloan', case=False, na=False),   # Homeloan repayment
    df['Description'].str.contains('Mergy', case=False, na=False),      # Investments payment
    df['Description'].str.contains('Settlement', case=False, na=False),  # Settlement
    df['Description'].str.contains('EYBS', case=False, na=False),       # Mergy pay
    df['Description'].str.contains('YARRA CITY COUNC RATES', case=False, na=False),       # Council rates
]

choices = [
    "Chant pay",                               # For Maxxia
    "Gas and electricity bills",               # For COVAU
    "Purchases",                               # For combined purchases
    "Streaming",                               # For combined Netflix, DisneyPlus and Stan
    "Wifi",                                    # For Spintel
    "Extra mortgage repayment",                # For Rocket Repa
    "Mortgage payment",                        # For Westpac
    "Fortnightly budget payment",              # For combined Chantelle and Daniel Ven
    "Homeloan repayment",                      # For Homeloan
    "Investments payment",                     # For Mergy
    "Settlement",                              # For Settlement
    "Mergy pay",                               # For EYBS
    "Council rates",                           # For council rates
]

# Create a new column with the classification
df['Transaction_classification'] = np.select(conditions, choices, default='Other')

#See unclassified values
df_unclassified = df[df['Transaction_classification'] == 'Other'][['Description', 'Transaction_classification']]
#print(df_unclassified['Description'].unique())

df.to_excel('C:/Users/danie/OneDrive/Work/Career/Coding/Folio/Budgeting app/data/Reporting/budgeting_data_rep.xlsx', index=False)

#print(df)









