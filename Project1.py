#!/usr/bin/env python
# coding: utf-8

# In[68]:


get_ipython().system('pip install yfinance')
#!pip install pandas
#!pip install requests
get_ipython().system('pip install bs4')
get_ipython().system('pip install plotly')


# In[69]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[70]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()


# # Question 1: Use yfinance to Extract Stock Data

# In[71]:


tesla = yf.Ticker("TSLA")


# In[72]:


tesla_data = tesla.history(period="max")


# In[73]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# # Question 2: Use Webscraping to Extract Tesla Revenue Data

# In[74]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[75]:


soup = BeautifulSoup(html_data,'html5lib')


# In[76]:


tesla_revenue=pd.read_html(url, match="Tesla Quarterly Revenue", flavor='bs4')[0]
tesla_revenue.head()


# In[77]:


tesla_revenue = tesla_revenue.rename(columns={"Tesla Quarterly Revenue(Millions of US $)":"Date","Tesla Quarterly Revenue(Millions of US $).1":"Revenue"}) #Rename df columns to 'Date' and 'Revenue'
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"") # remove the comma and dollar sign from the 'Revenue' column
tesla_revenue.head() # Display df


# In[78]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[79]:


tesla_revenue.tail()


# # Question 3: Use yfinance to Extract Stock Data

# In[80]:


game_stop = yf.Ticker("GME")


# In[81]:


gme_data = game_stop.history(period="max")


# In[82]:


gme_data.reset_index(inplace=True)
gme_data.head()


# # Question 4: Use Webscraping to Extract GME Revenue Data

# In[83]:


url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text


# In[84]:


soup = BeautifulSoup(html_data,'html5lib')


# In[85]:


gme_revenue=pd.read_html(url,match="GameStop Quarterly Revenue", flavor='bs4')[0]
#gme_revenue.head()
gme_revenue = gme_revenue.rename(columns={"GameStop Quarterly Revenue(Millions of US $)":"Date","GameStop Quarterly Revenue(Millions of US $).1":"Revenue"}) #Rename df columns to 'Date' and 'Revenue'
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"") # remove the comma and dollar sign from the 'Revenue' column
gme_revenue.head() # Display df


# In[86]:


# remove an null or empty strings in the Revenue column.
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

gme_revenue.tail() # Display last five (5) rows of df


# # Question 5: Plot Tesla Stock Graph

# In[87]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# # Question 6: Plot GameStop Stock Graph

# In[67]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




