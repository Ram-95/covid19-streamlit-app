import requests
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="COVID-19 India | Dashboard", page_icon="💉")
st.title("COVID-19 Cases in India")

df = pd.DataFrame(np.random.randn(500, 2) /[10,10] + [20.5937, 78.9629],
columns=['lat', 'lon'])
# st.map(df)
url = 'https://api.covid19tracker.in/data/static/data.min.json'
response = requests.get(url)
data = response.json()
state_code_dict = {
        'AN': 'Andaman and Nicobar', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'TT': 'Total',
        'CH': 'Chandigarh', 'CT': 'Chattisgarh', 'DL': 'Delhi', 'DN': 'Dadra and Nagar Haveli', 'GA': 'Goa', 'GJ': 'Gujarat',
        'HP': 'Himachal Pradesh', 'HR': 'Haryana', 'JH': 'Jharkhand', 'JK': 'Jammu and Kashmir', 'KA': 'Karnataka', 'KL': 'Kerala',
        'LA': 'Ladakh', 'LD': 'Lakshadweep', 'MH': 'Maharashtra', 'ML': 'Meghalaya', 'MN': 'Manipur', 'MP': 'Madhya Pradesh',
        'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Odisha', 'PB': 'Punjab', 'PY': 'Puducherry', 'RJ': 'Rajasthan', 'SK': 'Sikkim',
        'TG': 'Telangana', 'TN': 'Tamil Nadu', 'TR': 'Tripura', 'UP': 'Uttar Pradesh', 'UT': 'Uttarakhand', 'WB': 'West Bengal'
    }

total_confirmed_cases_container, total_active_cases_container, total_deaths_container, total_recovered_cases_container = st.columns(spec=4, gap="large")
totals = data.get('TT').get('total')
total_active_cases = totals['confirmed'] - (totals['deceased'] + totals['recovered'])

delta = data.get('TT').get('delta')
confirmed_delta = delta.get('confirmed')
deceased_delta = delta.get('deceased')
recovered_delta = delta.get('recovered')
active_delta = confirmed_delta - (deceased_delta + recovered_delta)

with total_confirmed_cases_container:
    st.header(":blue[Confirmed]")
    st.subheader(format(totals.get('confirmed'), ","))
    st.metric("", "", confirmed_delta)

with total_active_cases_container:
    st.header(":orange[Active]")
    st.subheader(format(total_active_cases, ","))
    st.metric("", "", active_delta)

with total_deaths_container:
    st.header(":red[Deaths]")
    st.subheader(format(totals.get('deceased'), ","))
    st.metric("", "", deceased_delta)

with total_recovered_cases_container:
    st.header(":green[Recovered]")
    st.subheader(format(totals.get('recovered'), ","))
    st.metric("", "", recovered_delta)

st.selectbox('Select State/UT', state_code_dict.values())