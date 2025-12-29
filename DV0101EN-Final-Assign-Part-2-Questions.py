#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

# Generate list of years for dropdown
year_list = [i for i in range(1980, 2024)]

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    # Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}
    ),

    # Dropdown for selecting report type
    html.Div([
            dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value=None
    )

    ], style={'padding': '10px'}),

    # Dropdown for selecting year
    html.Div([
            dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select Year',
        value=None,
        disabled=True
    )

    ], style={'padding': '10px'}),

    # Output container for charts
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

# Callback to enable/disable year dropdown based on report type
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_report):
    if selected_report == 'Yearly Statistics':
        return False
    else:
        return True

# Callback to update charts based on selections
@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_report, selected_year):

    # ------------------ Recession Period Statistics ------------------
    if selected_report == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Over Recession Period'
            )
        )

        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type During Recession'
            )
        )

        exp_data = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertisement Expenditure Share by Vehicle Type'
            )
        )

        unemp_data = recession_data.groupby(
            ['Vehicle_Type', 'unemployment_rate']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='Vehicle_Type',
                y='Automobile_Sales',
                color='unemployment_rate',
                title='Effect of Unemployment Rate on Vehicle Sales'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[R_chart1, R_chart2],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[R_chart3, R_chart4],
                style={'display': 'flex'}
            )
        ]

    # ------------------ Yearly Statistics ------------------
    elif selected_report == 'Yearly Statistics' and selected_year != 'Select Year':

        yearly_data = data[data['Year'] == selected_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales (Whole Period)'
            )
        )

        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title=f'Total Monthly Automobile Sales in {selected_year}'
            )
        )

        avg_vehicle = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avg_vehicle,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f'Average Vehicles Sold by Type in {selected_year}'
            )
        )

        adv_exp = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                adv_exp,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f'Advertisement Expenditure in {selected_year}'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[Y_chart1, Y_chart2],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[Y_chart3, Y_chart4],
                style={'display': 'flex'}
            )
        ]

    # ------------------ Default ------------------
    else:
        return html.Div(
            "Please select a report type and year",
            style={'textAlign': 'center', 'fontSize': 20}
        )


# Run the app
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8050,
        debug=True
    )


