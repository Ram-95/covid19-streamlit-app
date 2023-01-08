import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="COVID-19 India | Dashboard", page_icon="📈", layout="wide")
config = {'displayModeBar': False}  # configuration to hide the plotly toolbar

df = pd.DataFrame(np.random.randn(500, 2) /[10,10] + [20.5937, 78.9629],
columns=['lat', 'lon'])
# st.map(df)
state_code_dict = {
        'AN': 'Andaman and Nicobar', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'TT': 'India',
        'CH': 'Chandigarh', 'CT': 'Chattisgarh', 'DL': 'Delhi', 'DN': 'Dadra and Nagar Haveli', 'GA': 'Goa', 'GJ': 'Gujarat',
        'HP': 'Himachal Pradesh', 'HR': 'Haryana', 'JH': 'Jharkhand', 'JK': 'Jammu and Kashmir', 'KA': 'Karnataka', 'KL': 'Kerala',
        'LA': 'Ladakh', 'LD': 'Lakshadweep', 'MH': 'Maharashtra', 'ML': 'Meghalaya', 'MN': 'Manipur', 'MP': 'Madhya Pradesh',
        'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Odisha', 'PB': 'Punjab', 'PY': 'Puducherry', 'RJ': 'Rajasthan', 'SK': 'Sikkim',
        'TG': 'Telangana', 'TN': 'Tamil Nadu', 'TR': 'Tripura', 'UP': 'Uttar Pradesh', 'UT': 'Uttarakhand', 'WB': 'West Bengal'
    }

reverse_state_code_dict = {val: key for key,val in state_code_dict.items()}


def get_timeseries_data(type_of_graph: str, code: str) -> list:
    """Returns the timeseries data"""
    timeseries_url = f"https://data.incovid19.org/v4/min/timeseries-{code}.min.json"
    resp = requests.get(timeseries_url).json()
    all_dates = resp[code]['dates'] 
    output_data = {'confirmed': [], 'deceased': [], 'recovered': [], 'active': [], 'labels': list(all_dates.keys())}
    filter = 'total' if type_of_graph == 'Cummulative' else 'delta'
    
    for key in all_dates.keys():
        current_date = all_dates.get(key).get(filter)
        if current_date:
            output_data['confirmed'].append(current_date.get('confirmed', None))
            output_data['deceased'].append(current_date.get('deceased', None))
            output_data['recovered'].append(current_date.get('recovered', None))
        else:
            output_data['confirmed'].append(None)
            output_data['deceased'].append(None)
            output_data['confirmed'].append(None)
        if output_data['confirmed'][-1] and output_data['deceased'][-1] and output_data['recovered'][-1]:
            output_data['active'].append(max(output_data['confirmed'][-1] - (output_data['deceased'][-1] + output_data['recovered'][-1]), 0))
        else:
            output_data['active'].append(None)

    return output_data


def plot_data(type_of_graph: str, st_code: str) -> None:
    """Plots the trend graph."""
    st.header(f"{type_of_graph} Cases - {state_code_dict.get(st_code)}")
    confirmed_chart, active_chart = st.columns(spec=2, gap="medium")
    deceased_chart, recovered_chart = st.columns(spec=2, gap="medium")
    timeseries_data = get_timeseries_data(type_of_graph, st_code)
    graph_mode = 'lines'
    
    with confirmed_chart:
        st.subheader('Confirmed')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('confirmed'), mode=graph_mode, name='Confirmed'))
        fig.update_traces(line_color='#13bdfa')
        fig.update_layout(xaxis_title='Date', yaxis_title='Cases', hovermode="x unified")
        st.plotly_chart(figure_or_data=fig, use_container_width=True,sharing="streamlit", config=config)

    with active_chart:
        st.subheader('Active')
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('active'), mode=graph_mode, name='Active'))
        fig1.update_traces(line_color='#f2bb30')
        fig1.update_layout(xaxis_title='Date', yaxis_title='Cases', hovermode="x unified")
        st.plotly_chart(figure_or_data=fig1, use_container_width=True,sharing="streamlit", config=config)

    # Deceased Chart
    with deceased_chart:
        st.subheader('Deceased')
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('deceased'), mode=graph_mode, name='Deceased'))
        fig2.update_traces(line_color='#f70b0b')
        fig2.update_layout(xaxis_title='Date', yaxis_title='Cases', hovermode="x unified")
        st.plotly_chart(figure_or_data=fig2, use_container_width=True,sharing="streamlit", config=config)

    # Recovered Chart
    with recovered_chart:
        st.subheader('Recovered')
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=timeseries_data.get('labels'), y=timeseries_data.get('recovered'), mode=graph_mode, name='Recovered'))
        fig3.update_traces(line_color='#44f534')
        fig3.update_layout(xaxis_title='Date', yaxis_title='Cases', hovermode="x unified")
        st.plotly_chart(figure_or_data=fig3, use_container_width=True,sharing="streamlit", config=config)


def load_dashboard(st_code: str) -> None:
    """Loads the total summary of COVID-19 cases by the state code."""
    url = 'https://data.incovid19.org/v4/min/data.min.json'
    response = requests.get(url)
    data = response.json()
    st.title(f"COVID-19 Cases in {state_code_dict.get(st_code)}")
    last_updated_date = datetime.strptime(data.get(st_code).get('meta').get('last_updated'), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
    st.text(f"Data as on: {last_updated_date} (IST)")
    total_confirmed_cases_container, total_active_cases_container, total_deaths_container, total_recovered_cases_container = st.columns(spec=4, gap="large")
    totals = data.get(st_code).get('total')
    total_active_cases = totals['confirmed'] - (totals['deceased'] + totals['recovered'])

    delta = data.get(st_code).get('delta')
    confirmed_delta = delta.get('confirmed', 0)
    deceased_delta = delta.get('deceased', 0)
    recovered_delta = delta.get('recovered', 0)
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
        st.metric(format(totals.get('recovered'), ","), "", recovered_delta)

def get_total_states_data() -> list:
    """Returns the summary of all states."""
    url = 'https://data.incovid19.org/v4/min/data.min.json'
    response = requests.get(url)
    data = response.json()
    states_summary = {'Confirmed': {}, 'Deceased': {}, 'Active': {}, 'Recovered': {}}
    for st_code, st_name in state_code_dict.items():
        if st_code != 'TT':
            totals = data.get(st_code).get('total')
            total_active_cases = totals['confirmed'] - (totals['deceased'] + totals['recovered'])
            # 1 Day Change
            delta = data.get(st_code).get('delta')
            confirmed_delta = delta.get('confirmed', 0)
            deceased_delta = delta.get('deceased', 0)
            recovered_delta = delta.get('recovered', 0)
            active_delta = confirmed_delta - (deceased_delta + recovered_delta)
            
            states_summary['Confirmed'][st_name] = format(totals['confirmed'], ",") + f" ({confirmed_delta})"
            states_summary['Recovered'][st_name] = format(totals['recovered'], ",") + f" ({recovered_delta})"
            states_summary['Deceased'][st_name] = format(totals['deceased'], ",") + f" ({deceased_delta})"
            states_summary['Active'][st_name] = format(total_active_cases, ",") + f" ({max(active_delta, 0)})"
        
    return states_summary


drop_down_options = [f"{val}" for val in reverse_state_code_dict.keys()]
option = st.selectbox('Select State/UT', drop_down_options, index=5)
option_code = reverse_state_code_dict.get(option)
load_dashboard(option_code)

# Initial Display
plot_data("Cummulative", option_code)
plot_data("Daily", option_code)
states_data = get_total_states_data()
temp = {'row-1': {'confirmed': 1, 'recovered': 2, 'deaths': 3}}

# Show the summary only when India is selected
if option_code == 'TT':
    st.subheader("COVID-19 Summary")
    st.table(states_data)

