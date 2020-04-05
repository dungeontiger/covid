import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

layout_font=dict(
    family='verdana, courier new'
)


def create_charts():
    # create the images directory
    if not os.path.exists("images"):
        os.mkdir("images")
    # read the covid country data
    df = pd.read_csv('data/covid_country.csv')
    # create a world summary chart
    world = df.drop(['Country'], axis=1).groupby('Date').sum().reset_index()
    # treat the world as a country
    create_country_charts(world, 'World')
    # get the list of countries and create charts for each
    countries = df['Country'].unique()
    for country in countries:
        create_country_charts(df[df['Country'] == country], country)


def create_country_charts(df, country):
    print(country + '...')
    # create a scatter plot with two y axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # update the layout
    fig.update_layout(
        dict(
            plot_bgcolor='#DBDCDE',
            font=layout_font,
            width=1200,
            height=800,
            xaxis=dict(
                tickformat='%d %b (%a)'
            ),
            yaxis=dict(
                tickformat=',',
                title=dict(
                    text='<span style="color:blue">New</span> Confirmed Cases'
                )
            ),
            yaxis2=dict(
                showgrid=False,
                ticks='outside',
                ticklen=10,
                tickformat=',',
                title=dict(
                    text='<span style="color:red">Total</span> Confirmed Cases'
                )),
            title=dict(
                text=country,
                font=dict(
                    size=24
                )
            ),
            legend=dict(
                title='<b> Cases</b>',
                x=0.01,
                y=0.99,
                font=dict(
                    size=14
                )
            )
    ))
    # add the trace for new cases
    fig.add_trace(
        go.Scatter(x=df.Date,
                   y=df['New Confirmed Cases'],
                   mode='lines+markers',
                   name='New'
                   ),
        secondary_y=False,
    )
    # add the trace for cumulative confirmed cases
    fig.add_trace(
        go.Scatter(x=df.Date,
                   y=df['Confirmed Cases'],
                   mode='lines+markers',
                   name='Total'
                   ),
        secondary_y=True,
    )

    fig.write_image('images/{}_cases.png'.format(country.replace(' ', '-')))


if __name__ == "__main__":
    create_charts()
