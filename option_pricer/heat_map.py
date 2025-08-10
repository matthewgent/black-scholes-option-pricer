import plotly.express as plotly
from black_scholes import PricingModel


def data(
        x_prices: tuple[float],
        y_volatilities: tuple[float],
        strike_price_input: float,
        days_to_maturity_input: float,
        risk_free_interest_rate_input: float) -> (list, list):
    call_data = []
    put_data = []
    for y_volatility in y_volatilities:
        call_x_data = []
        put_x_data = []
        for x_price in x_prices:
            pricing_model = PricingModel(
                x_price, strike_price_input, days_to_maturity_input,
                y_volatility, risk_free_interest_rate_input / 100
            )
            call_x_data.append(f"{pricing_model.call.price():.2f}")
            put_x_data.append(f"{pricing_model.put.price():.2f}")
        call_data.append(call_x_data)
        put_data.append(put_x_data)

    return call_data, put_data


def plot(
        st_column,
        title: str,
        map_data: list,
        x_prices,
        y_volatilities) -> None:
    heat_map = plotly.imshow(
        map_data,
        text_auto=True,
        title=title,
        labels=dict(x="Spot Price (€)", y="Volatility"),
        aspect="equal",
    )
    heat_map.update_layout(
        margin=dict(l=50, r=50, t=50, b=70)
    )
    heat_map.update_coloraxes(showscale=False)
    heat_map.update_xaxes(
        tickangle=90,
        tickmode="array",
        tickvals=list(range(len(x_prices))),
        ticktext=[f"{price:.2f}" for price in x_prices]
    )
    heat_map.update_yaxes(
        tickmode="array",
        tickvals=list(range(len(y_volatilities))),
        ticktext=[f"{volatility:.2g}" for volatility in y_volatilities]
    )
    st_column.plotly_chart(heat_map, theme=None)
