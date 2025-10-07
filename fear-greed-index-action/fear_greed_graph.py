import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

# Load the CSV file
file_path = os.path.join('..', 'data', 'daily_crypto_fear_greed_index.csv')
df = pd.read_csv(file_path)

# Convert 'date' to datetime and sort
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Create base interactive line chart
fig = px.line(
    df,
    x='date',
    y='value',
    title='Daily Crypto Fear & Greed Index',
    labels={'value': 'Index Value', 'date': 'Date'},
    hover_data={'value_classification': True, 'date': True, 'value': True},
)

# Remove dots and set line color
fig.update_traces(line=dict(color='green'), mode='lines')

# Add background zones (updated ranges)
fig.add_shape(type="rect", xref="paper", yref="y",
              x0=0, x1=1, y0=0, y1=19,
              fillcolor="rgba(255, 102, 102, 0.2)", line_width=0, layer="below")  # Extreme Fear

fig.add_shape(type="rect", xref="paper", yref="y",
              x0=0, x1=1, y0=20, y1=39,
              fillcolor="rgba(255, 178, 102, 0.2)", line_width=0, layer="below")  # Fear

fig.add_shape(type="rect", xref="paper", yref="y",
              x0=0, x1=1, y0=40, y1=59,
              fillcolor="rgba(255, 255, 153, 0.25)", line_width=0, layer="below")  # Neutral

fig.add_shape(type="rect", xref="paper", yref="y",
              x0=0, x1=1, y0=60, y1=79,
              fillcolor="rgba(153, 255, 153, 0.2)", line_width=0, layer="below")  # Greed

fig.add_shape(type="rect", xref="paper", yref="y",
              x0=0, x1=1, y0=80, y1=100,
              fillcolor="rgba(102, 178, 255, 0.2)", line_width=0, layer="below")  # Extreme Greed

# Add zone labels
fig.add_annotation(xref="paper", yref="y", x=1.01, y=10, text="Extreme Fear", showarrow=False, font=dict(color="red"))
fig.add_annotation(xref="paper", yref="y", x=1.01, y=30, text="Fear", showarrow=False, font=dict(color="darkorange"))
fig.add_annotation(xref="paper", yref="y", x=1.01, y=50, text="Neutral", showarrow=False, font=dict(color="goldenrod"))
fig.add_annotation(xref="paper", yref="y", x=1.01, y=70, text="Greed", showarrow=False, font=dict(color="green"))
fig.add_annotation(xref="paper", yref="y", x=1.01, y=90, text="Extreme Greed", showarrow=False, font=dict(color="blue"))

# Layout improvements
fig.update_layout(
    hovermode='x unified',
    xaxis_title='Date',
    yaxis_title='Index Value',
    xaxis_tickangle=-45,
    template='plotly_white',
    margin=dict(r=120)
)

# Export and open in browser
fig.write_html("fear_greed_plot.html", auto_open=True)