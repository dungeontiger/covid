import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

layout_font=dict(
    family='verdana, courier new'
)


def create_country_charts():
    # create the images directory
    if not os.path.exists("images"):
        os.mkdir("images")
    # read the covid country data
    df = pd.read_csv('data/covid_country.csv')
    create_canada_charts(df)


def create_canada_charts(df):
    canada = df[df['Country'] == 'Canada']
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
                    text='New Confirmed Cases'
                )
            ),
            yaxis2=dict(
                showgrid=False,
                ticks='outside',
                ticklen=10,
                tickformat=',',
                title=dict(
                    text='Total Confirmed Cases'
                )),
            title=dict(
                text='Canada',
                font=dict(
                    size=24
                )
            ),
            legend=dict(
                title='<b> Cases</b>',
                x=0.01,
                y=0.99
            )
    ))
    # add the trace for new cases
    fig.add_trace(
        go.Scatter(x=canada.Date,
                   y=canada['New Confirmed Cases'],
                   mode='lines+markers',
                   name='New'
                   ),
        secondary_y=False,
    )
    # add the trace for cumulative confirmed cases
    fig.add_trace(
        go.Scatter(x=canada.Date,
                   y=canada['Confirmed Cases'],
                   mode='lines+markers',
                   name='Total'
                   ),
        secondary_y=True,
    )

    fig.write_image('images/canada_cases.png')


if __name__ == "__main__":
    create_country_charts()
