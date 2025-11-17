import plotly.express as plotly
from black_scholes import PricingModel
import numpy as np


def data(
        x_prices: np.ndarray,
        y_volatilities: np.ndarray,
        strike_price_input: float,
        days_to_maturity_input: float,
        risk_free_interest_rate_input: float
) -> (np.ndarray, np.ndarray):
    string_format = '%.2f'

    def prices(price, volatility):
        model = PricingModel(
            price, strike_price_input, days_to_maturity_input,
            volatility, risk_free_interest_rate_input / 100
        )
        return model.call.price(), model.put.price()

    vectorized_prices = np.vectorize(
        prices,
        signature='(), () -> (), ()'
    )
    calls, puts = vectorized_prices(
        x_prices[:, np.newaxis],
        y_volatilities[np.newaxis, :]
    )
    call_strings = np.char.mod(string_format, calls)
    put_strings = np.char.mod(string_format, puts)

    return call_strings, put_strings


def plot(
        st_column,
        title: str,
        map_data: np.ndarray,
        x_prices: np.ndarray,
        y_volatilities: np.ndarray
) -> None:
    tick_values = np.arange(1, x_prices.size)
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
        tickvals=tick_values,
        ticktext=[f"{price:.2f}" for price in x_prices]
    )
    heat_map.update_yaxes(
        tickmode="array",
        tickvals=tick_values,
        ticktext=[f"{volatility:.2g}" for volatility in y_volatilities]
    )
    st_column.plotly_chart(heat_map, theme=None)
