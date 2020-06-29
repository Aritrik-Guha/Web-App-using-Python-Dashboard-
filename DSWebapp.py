import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import time

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

from PIL import Image
image = Image.open('codepth2.jpg')
st.image(image, caption='Codepth Technologies',use_column_width=True)

#st.write("""Simple Stock Price App Shown are the stock closing price and volume of Google!""")
st.title('DASHBOARD')
t="<div><span class='highlight blue'>Some TITLE</span></div>"
st.markdown(t, unsafe_allow_html=True)
st.write("Here's our first attempt at using data to create a table:")
df=pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'MSFT'
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
st.write(tickerDf)
# Open	High	Low	Close	Volume	Dividends	Stock Splits


if st.checkbox('Show'):
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
    # Update the progress bar with each iteration.
        #latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)
    if st.checkbox('dataframe'):
        df
    if st.checkbox('line chart'):
        st.line_chart(tickerDf)

if st.checkbox('Show line charts'):
    st.line_chart(tickerDf.Close)
    

st.sidebar.title('Sidebar')
st.sidebar.line_chart(tickerDf.Volume)


option1 = st.sidebar.selectbox(
    'Which number do you like best?',
     df['first column'])

option2 = st.sidebar.selectbox(
    'Which number do you like second best?',
     df['second column'])

'You selected: ', option1, option2

df2=pd.DataFrame({
    'first col': [5, 6, 7, 8],
    'second col': [50, 60, 70, 80]
})

option = st.sidebar.selectbox(
    'Which number do you like best?',
     df2['first col'])

'You selected:', option


@st.cache  # ?? This function will be cached
def my_slow_function(x):
    return x**2

x = st.slider('x')
z=my_slow_function(x)
st.write(x,'square is =',z)

df3=pd.read_csv('data.csv')
df3

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
#st.table(df3.style.highlight_min(axis=0))