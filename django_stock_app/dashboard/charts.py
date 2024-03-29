import pandas as pd
import plotly.graph_objects as go


def stock_chart(data):
    """Function to create a candlestick chart using plotly."""
    data = pd.DataFrame.from_records(
        data.values_list("date", "open_price", "max_price", "min_price", "close_price"),
        columns=["date", "open_price", "max_price", "min_price", "close_price"],
    )
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data["date"],
                open=data["open_price"],
                high=data["max_price"],
                low=data["min_price"],
                close=data["close_price"],
            )
        ]
    )

    fig.update_layout(
        height=450,
        yaxis_title="Close Price in PLN",
        xaxis_title="",
        paper_bgcolor="rgb(250,250,250)",
        plot_bgcolor="rgb(250,250,250)",
        xaxis=dict(type="category"),
    )
    fig.update_xaxes(rangeslider_visible=True, categoryorder="category ascending")

    chart = fig.to_html(config=dict(displayModeBar=False))
    return chart
