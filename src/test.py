#create an example of streamlit library program in python
import streamlit as st
import pandas as pd
import numpy as np
import requests
from mftool import Mftool
import matplotlib.pyplot as plt 
import plotly.express as px
import math
import mpld3
import streamlit.components.v1 as components



st.title("Hello, World!")
st.write("This is a simple Streamlit app.")

# Add some interactive elements to the app
# name = st.text_input("Enter your name:")
# if st.button("Submit"):
#     st.write(f"Hello, {name}!")

# Display some data in a table
# data = {
#     "Name": ["Alice", "Bob", "Charlie"],
#     "Age": [25, 30, 35]
# }
# st.table(data)
# Add a map to the app with sample langitude and latitude data
# df = pd.DataFrame(
#     {
#         "col1": np.random.randn(1000) / 50 + 37.76,
#         "col2": np.random.randn(1000) / 50 + -122.4,
#         "col3": np.random.randn(1000) * 100,
#         "col4": np.random.rand(1000, 4).tolist(),
#     }
# )

# st.map(df, latitude="col1", longitude="col2", size="col3", color="col4")


#get data from https://api.mfapi.in/mf/122639/latest and create a df
# url = "https://api.mfapi.in/mf/122639/latest"
# response = requests.get(url)
# data = response.json()
# # df = pd.DataFrame(data)
# st.write(data)
# st.write(data['meta']['fund_house'])

# get timedate from https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam and show it on streamlit page
# url = "https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam"
# response = requests.get(url)
# data = response.json()
# st.write(data['dateTime'])

# mf=Mftool()
# df1 = mf.get_scheme_historical_nav("122639",as_Dataframe=True)
# df1=df1.sort_index()
# st.line_chart(df1, y='nav')

# # get data from https://api.mfapi.in/mf/122639 and convert json to pandas dataframe
# url = "https://api.mfapi.in/mf/122639"
# response = requests.get(url)
# data = response.json()
# df = pd.DataFrame(data['data'])
# df1=df
# df1['date']=pd.to_datetime(df1['date'], format="%d-%m-%Y")
# df1['nav'] = df1['nav'].astype(float)
# #create a line chart in streamlit for df1
# # st.write(df1.dtypes)
# # st.dataframe(df1)
# st.line_chart(df1, x='date', y='nav')


# from mftool import Mftool
mf = Mftool()
# print(mf)
# result = mf.get_available_schemes('ICICI')
# # st.write(result)
# df_schemes=pd.DataFrame(result, index=["scheme_name"])
# df_schemes = df_schemes.T
# df_schemes['scheme_code'] = df_schemes.index
# # df_schemes=df_schemes.rename(columns={'0':'scheme_name'})
# # df_schemes=df_schemes.reset_index(drop=True)
# # print(df_schemes)
# # st.write(df_schemes.iloc[[0]]['scheme_name'])
# # for key, value in result.items():
# #     st.write(key,value)
# #     df_schemes['scheme_code']=key
# #     df_schemes['scheme_name']=value
# # st.dataframe(df_schemes,on_select="tempu" , selection_mode="single-row")

# def tempu():
#     st.write("Tempu")
# df_schemes=pd.read_csv(result, delimiter=":")
# st.altair_chart(df_schemes)
# st.dataframe(df_schemes)
# queue =[]
if 'queue' not in st.session_state:
    st.session_state.queue = []
# if 'result' not in st.session_state:
#     st.session_state.result = result
# if 'mf' not in st.session_state:
#     st.session_state.mf = mf

fig=plt.figure()
all_scheme_codes = mf.get_scheme_codes()
df_schemes=pd.DataFrame(all_scheme_codes, index=["scheme_name"])
df_schemes = df_schemes.T
df_schemes['scheme_code'] = df_schemes.index

# df_schemes['scheme_code'] = df_schemes.index
df_schemes['comb'] = df_schemes['scheme_code'] + " - " + df_schemes['scheme_name']
# st.dataframe(df_schemes)

option = st.selectbox(
    'Select Fund', df_schemes['comb'])
    # ('Email', 'Home phone', 'Mobile phone'))

st.write('You selected:', option)
if option != 'Scheme Code - Scheme Name':
    if st.session_state.queue.__len__()==5:
        st.session_state.queue.pop(0)
        st.session_state.queue.append(option)
    else:
        st.session_state.queue.append(option)

    for scheme in st.session_state.queue:
        url = "https://api.mfapi.in/mf/"+scheme.split(" - ")[0]
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data['data'])
        df1=df
        df1['date']=pd.to_datetime(df1['date'], format="%d-%m-%Y").dt.date
        df1['nav'] = df1['nav'].astype(float)
        # df1['nav'] = df1['nav'].apply(lambda x: 0 if x ==0 else math.log(x))
        df1.sort_values('date', ascending=False)
        # df1.set_index('date')
        # st.dataframe(df1)
        means=df1
        means.set_index('date', inplace=True)
        means.sort_index(inplace=True)
        # st.dataframe(means)
        df_pct=means.pct_change(1260)            
        # st.dataframe(df_pct)
        df_pct['nav']+=1

        df_pct['cagr5']=(pow(df_pct['nav'],(1/5))-1)*100
        # st.dataframe(df_pct)
        #create a line chart in streamlit for df1
        # st.write(df1.dtypes)
        # st.dataframe(df1)
        # st.line_chart(df1, x='date', y='nav')
        plt.plot(df_pct.index   , df_pct['cagr5'], label = scheme)
    # plt.plot(y, x, label = "line 2")
    plt.legend()
    # plt.ion()
    # plt.show()
    st.pyplot(plt)
    # fig_html = mpld3.fig_to_html(fig)
    # components.html(fig_html, height=600)

# x = [10,20,30,40,50]
# y = [30,30,30,30,30]

# # plot lines
# plt.plot(x, y, label = "line 1")
# plt.plot(y, x, label = "line 2")
# plt.legend()
# plt.show()
# st.pyplot(plt)