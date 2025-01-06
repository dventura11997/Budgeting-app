import pandas as pd
import requests
from datetime import datetime
import plotly.express as px
import streamlit as st
from io import BytesIO

#This is a function to read in the data
def read_data():
    #df = pd.read_excel('C:/Users/danie/OneDrive/Work/Career/Coding/Folio/Budgeting app/data/Reporting/budgeting_data_rep_8_11_2024.xlsx')
    url = "https://github.com/dventura11997/Budgeting-app/raw/refs/heads/main/data/Reporting/budgeting_data_rep_8_11_2024.xlsx"

    # Fetch the file content from the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(BytesIO(response.content))
        print(df)  # Or use st.write(df) in Streamlit
    else:
        print(f"Error: Unable to fetch the file. Status code: {response.status_code}")

    # Return the DataFrame
    return df

df = read_data()

#This is a function to create doughnut graphs for income and expenses
def create_pie_graphs():
    #Create subset dataframes
    df_credit = df[(df['Debit_credit'] == 'Credit') &  ~df['Transaction_classification'].isin(['Other', 'Extra mortgage repayment', 'Homeloan repayment', 'Fortnightly budget payment'])]
    df_debit = df[(df['Debit_credit'] == 'Debit') & ~df['Transaction_classification'].isin(['Homeloan repayment', 'Settlement'])]
    #Create pie graphs
    colours = ['#0eedc7', '#190079', '#6212e6']
    fig_cred = px.pie(df_credit, values='Amount', names='Transaction_classification', hole=0.3, title='Income by source', color_discrete_sequence=colours)
    fig_deb = px.pie(df_debit, values='Amount', names='Transaction_classification', hole=0.3, title='Expenses by source', color_discrete_sequence=colours)
    # Create two columns
    col1, col2 = st.columns(2)
    # Display fig_cred in the first column and fig_deb in the second column
    with col1:
        st.plotly_chart(fig_cred, use_container_width=True)

    with col2:
        st.plotly_chart(fig_deb, use_container_width=True)

#This is a function to create a time series graph for minimum balance each month
def balance_ts_line_graph(): 
    min_bal = df.copy()
    # Create a YearMonth column for grouping
    min_bal['YearMonth'] = min_bal['Date'].dt.to_period('M')
    # Group by YearMonth and get the minimum Balance
    min_bal = min_bal.groupby('YearMonth', as_index=False)['Balance'].min()
    # Convert YearMonth back to a timestamp for plotting
    min_bal['YearMonth'] = min_bal['YearMonth'].dt.to_timestamp()
    balance_ts = px.line(min_bal, x='YearMonth', y='Balance', title='Minimum Balance by Month')
    st.plotly_chart(balance_ts, use_container_width=True)

#This is a function to calculate income and expenses each month
def mon_in_out():
    df_ie = df[~df['Transaction_classification'].isin(['Other', 'Misc', 'Homeloan repayment'])]
    classification_mapping = {
        'Mortgage payment': 'Expense',
        'Extra mortgage repayment': 'Expense',
        'Gas and electricity bills': 'Expense',
        'Wifi': 'Expense',
        'Fortnightly budget payment': 'Expense',
        'Investments payment': 'Expense',
        'Chant pay': 'Income',
        'Mergy pay': 'Income',
        'Disney plus': 'Expense',
        'Netflix': 'Expense',
        'Stan': 'Expense',
        'Purchases': 'Expense',
        'Homeloan repayment': 'Expense',
        'Council rates': 'Expense'
    }
    df_ie['Category'] = df_ie['Transaction_classification'].map(classification_mapping)
    df_ie['YearMonth'] = df_ie['Date'].dt.to_period('M').astype(str)

    # Aggregate data by month and category
    monthly_summary = df_ie.groupby(['YearMonth', 'Category'])['Amount'].sum().unstack(fill_value=0)
    
    # Create bar graph
    mon_inc_exp_graph = px.bar(
        monthly_summary.reset_index(), 
        x='YearMonth', 
        y=monthly_summary.columns,
        title='Monthly Income and Expenses',
        labels={'YearMonth': 'Month', 'value': 'Amount', 'variable': 'Category'},
        barmode='group',
        #color='Category',
        color_discrete_map={
                     'Income': '#0eedc7',  # Hex color for Chant Pay
                     'Expense': '#190079'   # Hex color for Mergy Pay
                 }
    )

    now = datetime.now()
    cur_ym = now.strftime("%Y-%m")
    
    curm_in = df_ie[(df_ie['YearMonth'] == cur_ym) & (df_ie['Category'] == 'Income')]['Amount'].sum()
    curm_out = df_ie[(df_ie['YearMonth'] == cur_ym) & (df_ie['Category'] == 'Expense')]['Amount'].sum()
    net_income = round((curm_in - curm_out), 2)
    return curm_in, curm_out, net_income, mon_inc_exp_graph

def monthly_pay():
    mon_pay = df[(df['Debit_credit'] == 'Credit') & df['Transaction_classification'].isin(['Chant pay', 'Mergy pay'])]
    mon_pay['YearMonth'] = mon_pay['Date'].dt.to_period('M').astype(str)
    total_pay = mon_pay.groupby(['YearMonth', 'Transaction_classification'], as_index=False)['Amount'].sum()

    # Create a stacked bar chart using Plotly
    pay_bar_graph = px.bar(total_pay, 
                 x='YearMonth', 
                 y='Amount', 
                 color='Transaction_classification', 
                 barmode='stack',
                 color_discrete_map={
                     'Chant pay': '#0eedc7',  # Hex color for Chant Pay
                     'Mergy pay': '#190079'   # Hex color for Mergy Pay
                 },
                 labels={'Amount': 'Total Amount', 'YearMonth': 'Year-Month'}
                )
    st.plotly_chart(pay_bar_graph)

    chant_avg_pay_df = mon_pay.copy()
    chant_avg_pay_df.loc[chant_avg_pay_df['Description'].str.contains('Maxxia', na=False), 'Transaction_classification'] = 'Chant pay - Maxxia'
    avg_chant_pay = round(chant_avg_pay_df[chant_avg_pay_df['Transaction_classification'] == 'Chant pay']['Amount'].mean() + chant_avg_pay_df[chant_avg_pay_df['Transaction_classification'] == 'Chant pay - Maxxia']['Amount'].mean(), 2)
    avg_merg_pay = round(mon_pay[mon_pay['Transaction_classification'] == 'Mergy pay']['Amount'].mean(), 2)

    return avg_chant_pay, avg_merg_pay




