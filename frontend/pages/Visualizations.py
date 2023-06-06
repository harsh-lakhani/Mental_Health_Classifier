import streamlit as st
import requests
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from wordcloud import WordCloud
from collections import Counter


from const import BACKEND_URL

st.set_page_config(page_title='Mental Health Analysis', page_icon=':bar_chart:', layout='wide')
# Listen to the Enter key when the submit button is focused

# hyperlink  to r/teenagers
link = 'https://www.reddit.com/r/teenagers/'
text = 'R/Teenagers'
message = f'<span style="font-size: 25px;"><a href="{link}">{text}</a></span> Visualizations'
st.write(f'<h1 style="font-size:10;">{message}</h1>', unsafe_allow_html=True)

def fetch_data():
    response = requests.get(f'{BACKEND_URL}/get_stream_result')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def pie(df ):    
    # Example list of sentences and their sentiment labels
    sentiment_labels =  df['Is Depressed'].tolist()

    # Pie chart of the distribution of sentiment labels
    fig1 = px.pie(values=[sentiment_labels.count(0), sentiment_labels.count(1)], 
                  names=["Not Depressed", "Is Depressed"], 
                  color=["Not Depressed", "Is Depressed"],
                    color_discrete_sequence=['#FF7F0E','#1F77B4'],
                  title="Sentiment Label Distribution")
    st.plotly_chart(fig1, use_container_width=True)

def wc(df ):    
    # Example list of sentences and their sentiment labels
    sentences =  df['Post title'].tolist()
    # Word cloud of the most frequent words in the sentences
    text = " ".join(sentences)
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap='prism', max_words=100).generate(text)
    fig3 = go.Figure(go.Image(z=wordcloud.to_array()))
    fig3.update_layout(title="Word Cloud of Sentences", xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
    st.plotly_chart(fig3, use_container_width=True)
def all_results(df ):
    st.title('Detailed Results')
    st.table(df, )

# add a input for user to filter, which is a drop down menu
with st.sidebar.expander('Filter', expanded=False):
    st.sidebar.subheader('Filter by:')
    st.sidebar.markdown('''
    - **Depression**: Whether the post is about depression or not
    - **Title**: The title of the post
    ''')
    st.sidebar.markdown('---')
    st.sidebar.subheader('Filter by Depression')
    depression = st.sidebar.radio('Depression', ['All', 'Depression', 'Not Depression'])
    st.sidebar.markdown('---')
    st.sidebar.subheader('Filter by Title')
    title = st.sidebar.text_input('Title', '')
    st.sidebar.markdown('---')


col1, col2 = st.columns(2)
with col1:
    pie_placeholder = st.empty()
with col2:
    wordcloud_placeholder = st.empty()
table_placeholder = st.empty()


# Constantly pull the backend for new results 
# and replace the old  table with the new one
while True:
    with st.spinner('Pulling Any New Posts from reddit...'):
        data = fetch_data()
    # Update the table with the new data
    if data is not None:
        df = pd.DataFrame(data, columns=['Post title', 'Is Depressed'], )
        df = df[df['Post title'].str.contains(title)]
        if depression == 'Depression':
            df = df[df['Is Depressed'] == 1.0]
        elif depression == 'Not Depression':
            df = df[df['Is Depressed'] == 0.0]
            
        with pie_placeholder.container():
            pie(df)
        with wordcloud_placeholder.container():
            wc(df)
        with table_placeholder.container():
            all_results(df)
    else:
        st.error('Failed to fetch data from the backend API.')

    # Wait for 5 seconds
    time.sleep(5)