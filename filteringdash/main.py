from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('C:/Users/dhana/coding/Personal Projects/DiversifyNow/diversifynow/static/HR.csv')

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# # App layout
# app.layout = html.Div([
#     html.Div(className='row', children='Filtering with Data, Graph, and Controls',
#              style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

#     html.Div(className='row', children=[
#         dcc.RadioItems(options=['Gender', 'Department', 'Attrition'],
#                        value='Gender',
#                        inline=True,
#                        id='my-radio-buttons-final')
#     ]),

#     html.Div(className='row', children=[
#         html.Div(className='six columns', children=[
#             dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
#         ]),
#         html.Div(className='six columns', children=[
#             dcc.Graph(figure={}, id='histo-chart-final')
#         ])
#     ])
# ])

# # Add controls to build the interaction
# @callback(
#     Output(component_id='histo-chart-final', component_property='figure'),
#     Input(component_id='my-radio-buttons-final', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(df, x='Job Satisfaction', y=col_chosen, histfunc='avg')
#     return fig


app.layout = html.Div([
    html.H4('Analysis of the HR Data'),
    dcc.Graph(id="graph"),
    html.P("Names:"),
    dcc.Dropdown(id='names',
        options=['Gender', 'Attrition', 'Department'],
        value='Gender', clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(id='values',
        options=['Percent Salary Hike', 'Monthly Income', 'Years At Company', 'Total Working Years', 'Work Life Balance', 'Job Satisfaction'],
        value='Years At Company', clearable=False
    ),
])


@app.callback(
    Output("graph", "figure"), 
    Input("names", "value"), 
    Input("values", "value"))
def generate_chart(names, values):
    #df = px.data.tips() # replace with your own data source
    fig = px.pie(df, values=values, names=names, hole=.3)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)