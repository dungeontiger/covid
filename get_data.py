import pandas as pd
import os


def get_data():
    """Top level method that builds all the datasets"""
    covid = get_covid_data()
    if not os.path.exists('data'):
        os.makedirs('data')
    covid.to_csv('data/covid_country.csv', index = False)


def get_covid_data():
    confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    confirmed = pivot_covid_date(confirmed)
    deaths = pivot_covid_date(deaths)
    confirmed = aggregate_covid_to_country_level(confirmed, 'Cases', 'Confirmed Cases')
    deaths = aggregate_covid_to_country_level(deaths, 'Cases', 'Deaths')
    covid_country_data = pd.merge(confirmed, deaths, how='left', left_index=True, right_index=True)
    covid_country_data['Mortality Rate'] = (covid_country_data['Deaths'] / covid_country_data['Confirmed Cases'])
    covid_country_data['Percent Change Confirmed Cases'] = covid_country_data['Confirmed Cases'].pct_change()
    covid_country_data = covid_country_data.reset_index()
    covid_country_data['New Confirmed Cases'] = covid_country_data.groupby('Country/Region')['Confirmed Cases'].diff()
    covid_country_data = covid_country_data.rename(columns={'Country/Region': 'Country'})
    covid_country_data = covid_country_data[['Country', 'Date', 'Confirmed Cases', 'New Confirmed Cases',
                                             'Percent Change Confirmed Cases', 'Deaths', 'Mortality Rate']]
    return covid_country_data


def pivot_covid_date(df):
    df_new = df.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_name='Cases',var_name='Date')
    df_new = df_new.set_index(['Country/Region', 'Province/State', 'Date'])
    return df_new


def aggregate_covid_to_country_level(df, old_name, new_name):
    df_new = df.groupby(['Country/Region', 'Date'])['Cases'].sum().reset_index()
    df_new = df_new.set_index(['Country/Region', 'Date'])
    df_new.index = df_new.index.set_levels([df_new.index.levels[0], pd.to_datetime(df_new.index.levels[1])])
    df_new = df_new.sort_values(['Country/Region', 'Date'], ascending=True)
    df_new = df_new.rename(columns={old_name: new_name})
    return df_new


if __name__ == "__main__":
    get_data()
