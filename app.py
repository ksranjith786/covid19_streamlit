import streamlit as st
import pandas as pd 
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

#import plotly.io as pio
#pio.renderers.default = 'browser'

from services.get.all import get_all
from services.get.countries import get_country
from services.get.historical import get_historical

import datetime

# https://corona.lmao.ninja/docs/#/
# https://github.com/disease-sh/API

#@st.cache

countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Caribbean Netherlands', 'Cayman Islands', 'Central African Republic', 'Chad', 'Channel Islands', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czechia'
    "Côte d'Ivoire" 'DRC', 'Denmark', 'Diamond Princess', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan'
    "Lao People's Democratic Republic" 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libyan Arab Jamahiriya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'MS Zaandam', 'Macao', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Réunion', 'S. Korea', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Pierre Miquelon', 'Saint Vincent and the Grenadines', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'St. Barth', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turks and Caicos Islands', 'UAE', 'UK', 'USA', 'Uganda', 'Ukraine', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']

def getDataFrame(data_list):
    data = dict()
    df_country = pd.DataFrame()
   
    data['data'] = data_list 

    for each_country_data in data['data']:
        df_country = df_country.append(pd.DataFrame.from_dict(each_country_data, orient='index').T)
        
    return df_country
# end getDataFrame

def get_country_data(country=""):
    country_data = get_country(country)
    #st.write(country_data)
    data_list = []
    if country == '':
        data_list.append(country_data)
    else:
        data_list = [country_data] # Since the Country is only one, we convert to LIST so below for loop will parse
        
    return getDataFrame(data_list)
# end get_country_data

def get_historical_data(country=""):
    history_data = get_historical(country)
    #st.write(history_data)
    data_list = []
    if country == '':
        data_list.append(history_data)
    else:
        data_list = [history_data] # Since the Country is only one, we convert to LIST so below for loop will parse
        
    return getDataFrame(data_list)
# end get_historical_data

def getCases(cases):
    pass

def getDeaths(deaths):
    pass

def getRecovered(recovered):
    pass

def getTimeline(df_country_history):
    return pd.DataFrame.from_dict(df_country_history['timeline'][0], orient='index').T

def plotExpress(df, x, y):
    fig = px.bar(data_frame=df, x=x , y=y)
    return fig
# end plotExpress

def plotGraph(df, x, y):
    fig = go.Figure(
        data = [
            go.Bar(name='Confirmed Cases', x=df.index, y=df['cases']),
            go.Bar(name='Deaths', x=df.index, y=df['deaths']),
            go.Bar(name='Recovered', x=df.index, y=df['recovered'])
            ]
        )
        # Change the bar mode
    fig.update_layout(barmode='relative', xaxis_tickangle=-45)
    return fig
# end plotGraph

def run():
    st.header('Coronavirus Tracker')

    all_data = get_all()
    #st.json(all_data)

    df_all = pd.DataFrame.from_dict(all_data, orient='index').T
    st.dataframe(df_all)

    data_load_state = st.text('Loading each Country data...')

    country_select = st.selectbox('Which Country do you track?', countries)
    st.write('You have chosen ' + country_select)
    # get the data for selected country
    df_country = get_country_data(country_select)
    st.dataframe(df_country)

    data_load_state.text("Loaded country's data...done!")

    data_load_state = st.text('Loading historical data for ' + country_select + '...')

    df_country_history = get_historical_data(country_select)
    df_timeline = getTimeline(df_country_history)
    st.dataframe(df_timeline.sort_index(ascending=False))

    data_load_state.text("Loaded historical country's data...done!")

    data_load_state = st.text('Plotting historical data for ' + country_select + '...')


    df_timeline['date'] = pd.to_datetime(df_timeline.index)
    df_timeline.reset_index(inplace=True, drop=True)

    #st.bar_chart(df_timeline)

    #plotly_fig = plotGraph(df_timeline)
    plotly_fig_cases = plotExpress(df_timeline, 'date', 'cases')
    plotly_fig_deaths = plotExpress(df_timeline, 'date', 'deaths')
    plotly_fig_recovered = plotExpress(df_timeline, 'date', 'recovered')

    st.write(plotly_fig_cases)
    st.write(plotly_fig_deaths)
    st.write(plotly_fig_recovered)
    # st.bar_chart(df_timeline) # Not being sorted by index (date)

    data_load_state.text("Plotted historical country's data...done!")
# end run()

if __name__ == "__main__":
    run()
# end main()
