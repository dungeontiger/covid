import json
import pandas as pd
import os, datetime
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
    # get the list of countries
    countries = df['Country'].unique()
    # create a JSON list of countries and save it for country selection
    with open('specs/countries.json','w') as f:
        json.dump(countries.tolist(), f)
    # create charts for each country
    for country in countries:
        create_country_charts(df[df['Country'] == country], country)


def create_country_charts(df, country):
    print(country + '...')
    now = datetime.datetime.now()
    # create a scatter plot with two y axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # update the layout
    fig.update_layout(
        dict(
            hovermode='x',
            plot_bgcolor='#DBDCDE',
            font=layout_font,
            width=1200,
            height=800,
            xaxis=dict(
                tickformat='%d %b (%a)',
                ticklen=5,
                ticks='outside',
                tickcolor='#ffffff',
                showspikes=True
            ),
            yaxis=dict(
                tickformat=',',
                rangemode='nonnegative',
                title=dict(
                    text='<span style="color:blue">New</span> Confirmed Cases'
                ),
                showspikes=True
            ),
            yaxis2=dict(
                showgrid=False,
                ticks='outside',
                ticklen=10,
                rangemode='nonnegative',
                tickformat=',',
                title=dict(
                    text='<span style="color:red">Total</span> Confirmed Cases'
                )),
            title=dict(
                text='Confirmed Cases: {}'.format(country),
                font=dict(
                    size=24
                )
            ),
            legend=dict(
                title='<b style="font-size:14"> Cases</b>',
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

    # add a footer
    fig.add_annotation(
        y=0,
        x=0,
        showarrow=False,
        xref='paper',
        yref='paper',
        yshift=-50,
        text='Source of data: John Hopkins (https://github.com/CSSEGISandData/COVID-19)',
        font=dict(
            size=10
        )
    )
    fig.add_annotation(
        y=0,
        x=0,
        showarrow=False,
        xref='paper',
        yref='paper',
        yshift=-65,
        text='Produced on {} at {} EST.'.format(now.strftime('%a, %b %d, %Y'), now.strftime('%H:%M')),
        font=dict(
            size=10
        )
    )
    fig.add_annotation(
        y=0,
        x=0,
        showarrow=False,
        xref='paper',
        yref='paper',
        yshift=-65,
        xshift=900,
        text='Provided by Stephen D. Gibson',
        font=dict(
            size=10
        )
    )

    try:
        fig.write_image('images/{}_cases.png'.format(country.replace(' ', '-')))
    except ValueError as err:
        print(err)
    with open('specs/{}_cases.json'.format(country.replace(' ', '-')), 'w') as f:
        f.write(fig.to_json())


if __name__ == "__main__":
    create_charts()
