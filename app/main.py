import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="COVID-19 India | Dashboard", page_icon="💉", layout="wide")
st.title("COVID-19 Cases in India")

df = pd.DataFrame(np.random.randn(500, 2) /[10,10] + [20.5937, 78.9629],
columns=['lat', 'lon'])
# st.map(df)

url = 'https://data.incovid19.org/v4/min/data.min.json'
def get_timeseries_data(code: str) -> list:
    """Returns the timeseries data"""
    timeseries_url = f"https://data.incovid19.org/v4/min/timeseries-{code}.min.json"
    resp = requests.get(timeseries_url).json()
    all_dates = resp['TT']['dates'] 
    output_data = {'confirmed': [], 'deceased': [], 'recovered': [], 'active': [], 'labels': list(all_dates.keys())}
    
    for key in all_dates.keys():
        output_data['confirmed'].append(all_dates.get(key).get('total').get('confirmed'))
        output_data['deceased'].append(all_dates.get(key).get('total').get('deceased'))
        output_data['recovered'].append(all_dates.get(key).get('total').get('recovered'))
        if output_data['confirmed'][-1] and output_data['deceased'][-1] and output_data['recovered'][-1]:
            output_data['active'].append(output_data['confirmed'][-1] - (output_data['deceased'][-1] + output_data['recovered'][-1]))
        else:
            output_data['active'].append(None)

    return output_data

timeseries_url = 'https://data.incovid19.org/v4/min/timeseries-TN.min.json'
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

drop_down_options = [f"{val} ({key})" for key, val in state_code_dict.items()]
total_confirmed_cases_container, total_active_cases_container, total_deaths_container, total_recovered_cases_container = st.columns(spec=4, gap="large")
totals = data.get('TT').get('total')
last_updated_date = datetime.strptime(data.get('TT').get('meta').get('last_updated'), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
total_active_cases = totals['confirmed'] - (totals['deceased'] + totals['recovered'])

delta = data.get('TT').get('delta')
confirmed_delta = delta.get('confirmed', 0)
deceased_delta = delta.get('deceased', 0)
recovered_delta = delta.get('recovered', 0)
active_delta = confirmed_delta - (deceased_delta + recovered_delta)
st.text(f"Data as on: {last_updated_date} (IST)")

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
    st.metric(format(totals.get('recovered'), ","), "", recovered_delta)

option = st.selectbox('Select State/UT', drop_down_options)
option_code = option[-4:].strip('()')
print(option_code)
timeseries_data = get_timeseries_data('TT')

st.header("Cummulative Cases")
confirmed_chart, active_chart = st.columns(spec=2, gap="medium")
with confirmed_chart:
    st.subheader('Total Confirmed')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('confirmed'), mode='lines+markers', name='Confirmed'))
    fig.update_traces(line_color='#13bdfa')
    # fig = px.line(timeseries_data, x=timeseries_data.get('labels'), y=timeseries_data.get('confirmed'), title='Total Confirmed Cases', markers=True)
    st.plotly_chart(figure_or_data=fig, use_container_width=True,sharing="streamlit")

with active_chart:
    # Active Chart
    st.subheader('Total Active')
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('active'), mode='lines+markers', name='Active'))
    fig1.update_traces(line_color='#f2bb30')
    st.plotly_chart(figure_or_data=fig1, use_container_width=True,sharing="streamlit")

deceased_chart, recovered_chart = st.columns(spec=2, gap="medium")
# Deceased Chart
with deceased_chart:
    st.subheader('Total Deceased')
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('deceased'), mode='lines+markers', name='Deceased'))
    fig1.update_traces(line_color='#f70b0b')
    st.plotly_chart(figure_or_data=fig1, use_container_width=True,sharing="streamlit")
# st.line_chart(data=timeseries_data.get('confirmed'), x=timeseries_data.get('labels'))
# st.line_chart(data=timeseries_data.get('deceased'), x=timeseries_data.get('labels'))
# st.line_chart(data=timeseries_data.get('recovered'), x=timeseries_data.get('labels'))
# fig.show()

# Recovered Chart
with recovered_chart:
    st.subheader('Total Recovered')
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('recovered'), mode='lines+markers', name='Recovered'))
    fig1.update_traces(line_color='#44f534')
    st.plotly_chart(figure_or_data=fig1, use_container_width=True,sharing="streamlit")

