import plotly.express as px
import pandas as pd


def portfolio_chart(data):
    df_data = pd.DataFrame(columns=['stock', 'pricing'])
    for stock in data:
        df_data = df_data.append({'stock': stock.stock, 'pricing': stock.pricing}, ignore_index=True)

    df_data.sort_values(ascending=False, by=['pricing'], inplace=True)

    fig = px.bar(df_data, x='stock', y='pricing',
                 color_discrete_sequence=[px.colors.qualitative.G10[5]])
    fig.update_layout(height=450,
                      yaxis_title='Close Price in PLN',
                      xaxis_title='',
                      paper_bgcolor='rgb(250,250,250)',
                      plot_bgcolor='rgb(250,250,250)'
                      )

    chart = fig.to_html(config=dict(displayModeBar=False))
    return chart
