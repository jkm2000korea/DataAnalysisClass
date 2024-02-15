#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pandas import json_normalize
import pandas as pd
import requests
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt


# In[3]:


def get_data(url):

    contents = requests.get(url)
    data = contents.json()
    df = pd.json_normalize(data)

    return df


# In[5]:


def permission_preprocessing(df):
    df = df[['PRD_DE', 'C1_NM', 'DT']]
#     df = df.pivot("PRD_DE", "C1_NM", "DT")
    df = df.pivot(index="PRD_DE", columns= "C1_NM", values="DT")

    df[['전국', '수도권', '지방소계']]
    df['수도권'] = pd.to_numeric(df['수도권'])
    df['지방소계'] = pd.to_numeric(df['지방소계'])
    df['수도권_월'] = np.where(df.index.str[-2:] == '01', df['수도권'], df['수도권'].diff()).astype(int)
    df['지방권_월'] = np.where(df.index.str[-2:] == '01', df['지방소계'], df['지방소계'].diff()).astype(int)
    df['연'] = df.index.str[:4]
    df['월'] = df.index.str[-2:]

    df.index = df['연'] + "-" + df['월']
    df.index = pd.to_datetime(df.index)
    df = df[['수도권_월','지방권_월']]
    df = df.groupby(df.index.year).sum()
    
    return df


# In[6]:


def permission__graph(df):
    plt.rcParams['font.family'] = "NanumGothic"
    plt.figure(figsize=(20, 8))
    
    down =  df.loc[:,'수도권_월']# 수도권
    top =  df.loc[:,'지방권_월'] # 지방권

    plt.bar(df.index, down, color='firebrick',hatch="///",edgecolor='white')#수도권
    plt.bar(df.index, top, bottom=down, color='midnightblue', hatch=".",edgecolor='yellow') #지방권

    y = down + top

    plt.ylim(0, y.max()*1.1)
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%i')) #%i 는 int , %f 는 float, %.3f 백만호 : 0.001 백만호
    plt.grid(True, axis='y', color='gray', alpha=0.5, linestyle='-')

    plt.legend(['수도권', '지방권'])
    plt.title('전국 주택건설 인허가 물량(2002~2023)', fontsize='20')
    plt.xticks(df.index)
    plt.figure(figsize=(20,5))
    
    return plt.show()


# In[7]:


def presale_preprocessing(url):
    
    contents = requests.get(url)
    test_data =contents.json()
    df = pd.json_normalize(test_data)

    df = df[['PRD_DE', 'C1_NM', 'DT']]
#     df = df.pivot("PRD_DE", "C1_NM", "DT")
    df = df.pivot(index="PRD_DE", columns= "C1_NM", values="DT")

    df = df.astype(int)
    
    df['지방권'] = df['전국'] - df['수도권']
    df = df.loc[:,['수도권', '지방권']]
    df.drop(['201510', '201511', '201512'], inplace=True)
    
    df['연'] = df.index.str[:4]
    df['월'] = df.index.str[-2:]    
    df['시점']= df['연'] + "-" + df['월']
    
    df.index = df['시점']
    df['시점'] = pd.to_datetime(df['시점'])    
    df = df.groupby(['연']).sum(['수도권','지방권'])
    
    return df


# In[8]:


def presale_graph(df_presale):
    
    plt.rcParams['font.family'] = "NanumGothic"
    plt.figure(figsize=(20, 8))
    
    down =  df_presale.iloc[:,0] #수도권
    top =  df_presale.iloc[:,1] #지방권

    plt.bar(df_presale.index, down, color='firebrick')#수도권
    plt.bar(df_presale.index, top, bottom=down, color='midnightblue', hatch="..",edgecolor='white') #지방권
    
    y = down + top
    
    plt.ylim(0, y.max()*1.1)
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%i')) #%i 는 int , %f 는 float, %.3f : 0.001
    # gca() : get current axis 현재 Axes 객체를 반환

    plt.grid(True, axis='y', color='gray', alpha=0.5, linestyle='-')

    plt.legend(['수도권', '지방권'])
    plt.title('전국 분양 물량(2016 ~ 2022)', fontsize='20')
    plt.figure(figsize=(20,5))
    
    return plt.show()

