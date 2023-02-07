import plotly.express as px
import pandas as pd


def portfolio_chart(data):
    """ Create a portfolio bar chart based on current stock pricing. Stocks are in descending order. """
    df_data = pd.DataFrame(columns=['stock', 'pricing'])
    for stock in data:
        df_data = df_data.append({'stock': stock.stock, 'pricing': stock.pricing}, ignore_index=True)

    df_data.sort_values(ascending=False, by=['pricing'], inplace=True)

    fig = px.bar(df_data, x='stock', y='pricing',
                 color='stock',
                 color_discrete_sequence=px.colors.qualitative.T10,
                 )
    fig.update_layout(height=450,
                      yaxis_title='Close Price in PLN',
                      xaxis_title='',
                      paper_bgcolor='rgb(250,250,250)',
                      plot_bgcolor='rgb(250,250,250)',
                      showlegend=False
                      )

    chart = fig.to_html(config=dict(displayModeBar=False))
    return chart
