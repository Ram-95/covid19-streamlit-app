import streamlit as st

st.set_page_config(page_title="Maximum of 3 numbers", page_icon="⨊", layout="wide")
st.title(f"Largest among 3 given numbers")

with st.form(key='my_form'):
    input1 = st.text_input(label='Input 1', placeholder='Enter the first digit')
    input2 = st.text_input(label='Input 2', placeholder='Enter the second digit')
    input3 = st.text_input(label='Input 3', placeholder='Enter the third digit')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    try:
        input1 = int(input1)
        input2 = int(input2)
        input3 = int(input3)
    except Exception:
        st.write(":red[Please enter all integers]")
    else:
        ans = max(int(input1), int(input2), int(input3))
        st.header(f"Largest number is: :green[{ans}]")
    

