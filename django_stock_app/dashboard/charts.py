import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def stock_chart(data):
    data = pd.DataFrame.from_records(data.values_list('date', 'open_price', 'max_price', 'min_price', 'close_price'),
                                     columns=['date', 'open_price', 'max_price', 'min_price', 'close_price'])
    fig = go.Figure(data=[go.Candlestick(x=data['date'],
                                         open=data['open_price'],
                                         high=data['max_price'],
                                         low=data['min_price'],
                                         close=data['close_price'])])

    fig.update_layout(height=450,
                      yaxis_title='Close Price in PLN',
                      xaxis_title='',
                      paper_bgcolor='rgb(250,250,250)',
                      plot_bgcolor='rgb(250,250,250)'
                      )
    fig.update_xaxes(rangeslider_visible=True)

    chart = fig.to_html(config=dict(displayModeBar=False))
    return chart
