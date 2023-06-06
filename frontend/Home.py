import streamlit as st
import requests
from const import BACKEND_URL
from PIL import Image
st.set_page_config(page_title='Mental Health Platform', page_icon=':brain:', layout='wide')
# Listen to the Enter key when the submit button is focused

st.title('Hello!')
c1,c2,c3 = st.columns([1,1,1])
c1.image(Image.open('images/1.png').resize((256,256)), )
c2.image(Image.open('images/2.png').resize((256,256)), )
c3.image(Image.open('images/3.png').resize((256,256)),)

message ='''Social media seems fun, but it can be a total downer. 
Do you ever feel like the more time you spend scrolling, the more likely you are to feel bummed out?
'''
st.write(f'<h2 style="font-size:20;">{message}</h2>', unsafe_allow_html=True)

message ='''Tell us something, we will tell you if you are likely depressed'''
st.write(f'<h3 style="font-size:20;">{message}</h3>', unsafe_allow_html=True)

with st.form('my_form'):
    text =st.text_area('Enter the text to be analyzed')
    submit = st.form_submit_button('Submit',use_container_width=True,)
    
    
if submit:
    # call the backend
    with st.spinner('Analyzing...'):
        response = requests.post(f'{BACKEND_URL}/depressed', json={'text': text}).json()
        if response == 1.0: 
            st.success('it is depression')
        else:
            st.success('it is not depression')
                