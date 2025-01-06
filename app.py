#Cd directory: cd "C:\Users\danie\OneDrive\Work\Career\Coding\Folio\Budgeting app"
#Launch virtualenv: venv\Scripts\activate
#Run app: streamlit run app.py

import streamlit as st
from functions import *
from pathlib import Path

st.set_page_config(page_title="Budget app", layout="wide")

# Path to the CSS file
css_file_path = Path("styles.css")

# Read the CSS file
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#This line of code removes weird hover links which streamlit puts in
st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

#HTML for the heading
st.markdown(f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css?family=Libre+Bodoni|New+Amsterdam|Fredoka" rel="stylesheet">
        <link href="styles.css" rel="stylesheet">
    </head>
    <div class="header-container"> 
        <h1 class="major-heading">
            Budgeting App
        </h1>
""", unsafe_allow_html=True)

# Read in the data
curm_in, curm_out, net_income, mon_inc_exp_graph = mon_in_out()

# if st.button("Reload page"):
#     streamlit_js_eval(js_expressions="parent.window.location.reload()")

st.markdown(f"""
    <div class="card-grid">
        <div class="card">
            <h2 class="card-heading">
                 Monthly Income:
            </h2>
            ${curm_in}
        </div>
        <div class="card">
            <h2 class="card-heading">
                 Monthly expenses:
            </h2>
            ${curm_out}
        </div>
        <div class="card">
            <h2 class="card-heading">
                 Net income:
            </h2>
            ${net_income}
        </div>
    </div>
""", unsafe_allow_html=True)

st.plotly_chart(mon_inc_exp_graph)
create_pie_graphs()
balance_ts_line_graph()

avg_chant_pay, avg_merg_pay = monthly_pay()

st.markdown(f"""
    <div class="pay-card-grid">
        <div class="card">
            <h2 class="card-heading">
                 Chant avg pay (fortnightly):
            </h2>
            ${avg_chant_pay}
        </div>
        <div class="card">
            <h2 class="card-heading">
                 Mergy avg pay (monthly):
            </h2>
            ${avg_merg_pay}
        </div>
    </div>
""", unsafe_allow_html=True)















