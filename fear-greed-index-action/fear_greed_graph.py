import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

# Load the CSV file
file_path = os.path.join('..', 'data', 'daily_crypto_fear_greed_index.csv')
df = pd.read_csv(file_path)

# Convert 'date' to datetime format and sort by date
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Create interactive line plot with green line and hover info
fig = px.line(
    df,
    x='date',
    y='value',
    title='Daily Crypto Fear & Greed Index',
    labels={'value': 'Index Value', 'date': 'Date'},
    line_shape='linear',
    hover_data={'value_classification': True, 'date': True, 'value': True},
)

# Style adjustments
fig.update_traces(line=dict(color='green'), mode='lines')  # no markers/dots
fig.update_layout(
    hovermode='x unified',
    xaxis_title='Date',
    yaxis_title='Index Value',
    xaxis_tickangle=-45,
    template='plotly_white'
)

# Show the plot
fig.write_html("fear_greed_plot.html", auto_open=True)