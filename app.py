from math import isnan

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout='wide',page_title='Startup_Analysis',page_icon='company.png')

df=pd.read_csv('startup_cleaned.csv')

df['city']=df['city'].str.replace('Bengaluru','Bangalore')
df['city']=df['city'].str.replace('Gurugram','Gurgaon')
df['startup']=df['startup'].str.replace("'",'',regex=False)
df['startup'] = df['startup'].str.replace('"', '', regex=False)

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df=df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'Rs in Crore']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    # biggest investments
    if df[df['investors'].str.contains(investor)]['Rs in Crore'].sum() != 0:
        st.subheader('Biggest Investments')
        col1, col2 = st.columns(2)
        with col2:
            big_series=df[df['investors'].str.contains(investor)].groupby('startup')['Rs in Crore'].sum().sort_values(ascending=False).head(6)
            st.dataframe(big_series)
        with col1:
            fig,ax=plt.subplots()
            ax.bar(big_series.index,big_series.values)
            st.pyplot(fig)
    else:
        pass

    # Sector Wise Investment
    if df[df['investors'].str.contains(investor)]['Rs in Crore'].sum()!=0:
        # Sector Wise Investment
        st.subheader('Sector Wise Investment')
        col1, col2 = st.columns(2)
        with col1:
            vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['Rs in Crore'].sum()
            fig1, ax1 = plt.subplots()
            ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')
            st.pyplot(fig1)
        with col2:
            st.dataframe(vertical_series)

        st.subheader('Investment')
        col1, col2, col3= st.columns(3)
        # year wise Investments
        with col1:
            # Year Wise Investment
            st.subheader('Year Wise')
            year_series = df[df['investors'].str.contains(investor)].groupby('year')['Rs in Crore'].sum()
            fig4, ax4 = plt.subplots()
            ax4.plot(year_series.index,year_series.values)
            st.pyplot(fig4)
        # city wise Investments
        with col2:
            # City Wise Investment
            st.subheader('City Wise')
            city_series = df[df['investors'].str.contains(investor)].groupby('city')['Rs in Crore'].sum()
            fig3, ax3 = plt.subplots()
            ax3.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
            st.pyplot(fig3)
        # Round wise Investments
        with col3:
            # Round Wise Investment
            st.subheader('Round Wise')
            round_series = df[df['investors'].str.contains(investor)].groupby('round')['Rs in Crore'].sum()
            fig2, ax2 = plt.subplots()
            ax2.pie(round_series, labels=round_series.index, autopct='%0.01f%%')
            st.pyplot(fig2)
    else:
        pass

    # Similar Investors
    st.subheader('Similar Investors')
    sector = df[df['investors'].str.contains(investor)]['vertical'].unique()
    invest = pd.Series(list(set(df[df['vertical'].isin(sector)]['investors'].str.split(',').sum())),name='Similar Investors')
    invest = invest[invest.values != '']
    st.dataframe(invest.sample(5).reset_index()['Similar Investors'])

def load_overall_analysis():
    st.title('StartUp Overall Analysis')
    col1,col2,col3,col4=st.columns(4)
    with col1:
        # total invested amount
        total = round(df['Rs in Crore'].sum())
        st.metric('Total Investment',str(total)+' Cr.')
    with col2:
        # Maximum invested Amount
        max = round(df.groupby('startup')['Rs in Crore'].sum().sort_values(ascending=False).head(1).iloc[0])
        st.metric('Maximum Investment',str(max)+' Cr.')
    with col3:
        # Average invested Amount
        avg = round(df.groupby('startup')['Rs in Crore'].sum().mean())
        st.metric('Average Investment', str(avg) + ' Cr.')
    with col4:
        # Total Funded Startups
        total_startup = df['startup'].drop_duplicates().count()
        st.metric('Total Funded StartUps', total_startup)

    # Month wise investment Graph
    st.header('MoM Graph')
    mom_chart=st.selectbox('Select Type',['Total','Count'],key='MoM Graph')
    # As per amount
    if mom_chart=='Total':
        temp_df = df.groupby(['year', 'month'])['Rs in Crore'].sum().reset_index()
    # As per count
    else:
        temp_df = df.groupby(['year', 'month'])['Rs in Crore'].count().reset_index()

    temp_df['month_year'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    # Plot Graph
    fig5, ax5 = plt.subplots(figsize=(10, 4))
    ax5.plot(temp_df['month_year'],temp_df['Rs in Crore'], marker='o')
    plt.xticks(rotation=90)
    st.pyplot(fig5)

    # Top 5 Startups
    st.header('Top 5 Funded Startups')
    sec = st.selectbox('Select Type', ['Overall', 'Year wise'], key='Top Startups')
    # Overall
    if sec == 'Overall':
        st.dataframe(df.groupby('startup')['Rs in Crore'].sum().sort_values(ascending=False).head(5))
    # Year wise
    else:
        selected_year = st.selectbox('Select Year', sorted(set(df['year'])))
        st.dataframe(df[df['year'] == selected_year].groupby('startup')['Rs in Crore'].sum().sort_values(
            ascending=False).head(5))

    # Top 5 Investor
    st.header('Top 5 Investor')
    sec = st.selectbox('Select Type', ['Overall', 'Year wise'], key='Top Investor')
    # Overall
    if sec == 'Overall':
        st.dataframe(df.groupby('investors')['Rs in Crore'].sum().sort_values(ascending=False).head(5))
    # Year wise
    else:
        selected_year = st.selectbox('Select Year', sorted(set(df['year'])),key='Top Investors')
        st.dataframe(df[df['year'] == selected_year].groupby('investors')['Rs in Crore'].sum().sort_values(
            ascending=False).head(5))

    #Top 10 Sector Analysis
    st.header('Top 10 Sector Analysis')
    sec=st.selectbox('Select Type',['Total','Count'],key='Sector Analysis')
    # As per Amount
    if sec=='Total':
        temp_df = df.groupby('vertical')['Rs in Crore'].sum().sort_values(ascending=False).head(10)
    # As per Count
    else:
        temp_df = df.groupby('vertical')['Rs in Crore'].count().sort_values(ascending=False).head(10)
    # Plot Graph
    fig5, ax5 = plt.subplots()
    ax5.pie(temp_df, labels=temp_df.index, autopct='%0.01f%%')
    st.pyplot(fig5)

    # Type of funding
    st.header('Type of funding')
    type_of_funding=df.groupby('round')['Rs in Crore'].sum().sort_values(ascending=False)
    st.dataframe(type_of_funding)

    # Top 10 City funding
    st.header('Top 10 City funded')
    city_wise_funding=df.groupby('city')['Rs in Crore'].sum().sort_values(ascending=False).head(10)
    st.dataframe(city_wise_funding)

    # Funding Heatmap
    st.header('Funding Heatmap')
    funding_heatmap=df.groupby(['year','month'])['Rs in Crore'].sum().reset_index()
    pivot_df = funding_heatmap.pivot_table(index='year', columns='month', values='Rs in Crore', aggfunc='sum', fill_value=0)
    # Plot Graph
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    cax = ax6.matshow(pivot_df, cmap='coolwarm')
    fig6.colorbar(cax)
    ax6.set_xticks(range(len(pivot_df.columns)))
    ax6.set_yticks(range(len(pivot_df.index)))
    ax6.set_xticklabels(pivot_df.columns)
    ax6.set_yticklabels(pivot_df.index)
    ax6.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
    ax6.set_xlabel('Months', fontsize=12, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig6)

def load_startup_details(startup):
    st.title(startup)
    col1, col2=st.columns(2)
    with col1:
        # Industry Name
        industry=df[df['startup']==startup]['vertical'].iloc[0]
        st.metric('Industry',industry)

    col1, col2 = st.columns(2)
    with col1:
        # Sub Industry Name
        sub_industry = df[df['startup'] ==startup]['subvertical'].iloc[0]
        st.metric('Sub Industry', sub_industry)
    with col2:
        # City/Location Name
        location=df[df['startup']==startup]['city'].iloc[0]
        st.metric('City', location)

    # Investor of Startup
    st.header('Investors')
    x = set(df[df['startup'] == startup]['investors'].str.split(',').sum())
    for i in x:
        st.write(i)

    # Funding Round Details
    st.header('Funding Rounds')
    funding=df[df['startup']=="Paytm"][['date','investors','round','Rs in Crore']].set_index('investors')
    st.dataframe(funding)

    # Similar Startups
    st.subheader('Similar Startups')
    sector = df[df['startup'] == startup]['vertical'].unique()
    invest = df[df['vertical'].isin(sector)]['startup']
    similar_startup=invest.sample(5,replace=True).reset_index()
    similar_startup=similar_startup.rename(columns={'startup': 'Similar StartUps'})
    st.dataframe(similar_startup['Similar StartUps'])

st.sidebar.title('Startup Funding Analysis')
# Sidebar And Sidebar selectBox
option=st.sidebar.selectbox('',['Overall Analysis','StartUp','Investor'])

# if Overall Analysis select by user
if option == 'Overall Analysis':
    btn0=st.sidebar.button('Show Overall Analysis')
    load_overall_analysis()

# if Startup select by user
elif option == 'StartUp':
    # Startup Name selectbox
    selected_startup=st.sidebar.selectbox('Select StartUp',sorted(list(df['startup'].unique())))
    btn1=st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)
# if Investor select by user
else:
    # Investor Name selectbox
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)

