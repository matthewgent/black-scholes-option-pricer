import streamlit as st
from black_scholes import PricingModel
import plotly.express as plotly
import numpy

st.set_page_config(
    page_title="Black Scholes Option Pricer",
    page_icon=":chart_increasing:",
    layout="wide")

st.sidebar.caption("Linkedin profile:")
st.sidebar.page_link(
    "https://linkedin.com/in/matthewgent",
    label="Matthew Gent",
    icon=":material/link:")

st.sidebar.divider()

spot_price_input = st.sidebar.number_input(
    label="Spot price",
    min_value=0.01,
    value=100.0,
    step=0.01,
    label_visibility="visible",
    icon=":material/euro:",
    width="stretch"
)

strike_price_input = st.sidebar.number_input(
    label="Strike price",
    min_value=0.01,
    value=95.0,
    step=0.01,
    label_visibility="visible",
    icon=":material/euro:",
    width="stretch"
)

days_to_maturity_input = st.sidebar.number_input(
    label="Days to maturity",
    min_value=1,
    value=30,
    step=1,
    label_visibility="visible",
    width="stretch"
)

volatility_input = st.sidebar.number_input(
    label="Volatility (σ)",
    min_value=0.01,
    value=0.5,
    step=0.01,
    label_visibility="visible",
    width="stretch"
)

risk_free_interest_rate_input = st.sidebar.number_input(
    label="Risk free interest rate",
    min_value=0.0,
    value=1.0,
    step=0.01,
    label_visibility="visible",
    width="stretch"
)


def badge(color: str, symbol: str, value: str) -> str:
    styles = [
        f"background-color:{color}",
        "width:100%",
        "text-align:center",
        "border-radius:2em",
        "font-size:smaller",
        "padding:2px",
        "line-height:1.4em"
    ]
    return f"<div style='{";".join(styles)}'>{symbol}<br>{value}</div>"


def greeks(column, heading: str, model: PricingModel) -> None:
    column.metric(heading, f"€ {model.price():.2f}")
    col1, col2, col3, col4, col5 = column.columns(5)
    col1.html(badge("chocolate", "Δ", f"{model.delta():.3}"))
    col2.html(badge("darkgreen", "Γ", f"{model.gamma():.3}"))
    col3.html(badge("darkorchid", "ν", f"{model.vega():.3}"))
    col4.html(badge("firebrick", "θ", f"{model.theta():.3}"))
    col5.html(badge("steelblue", "ρ", f"{model.rho():.3}"))


pricing_model = PricingModel(
    spot_price_input, strike_price_input, days_to_maturity_input,
    volatility_input, risk_free_interest_rate_input / 100)

call, put = st.columns(2, border=True)
greeks(call, "CALL", pricing_model.call)
greeks(put, "PUT", pricing_model.put)

st.html('<br>')

with st.container(border=True):
    col1, col2, col3 = st.columns([1, 1, 2], gap="medium")
    min_spot_price = col1.number_input(
        label="Min spot price",
        min_value=0.01,
        value=spot_price_input * 0.9,
        step=0.01,
        label_visibility="visible",
        icon=":material/euro:",
        width="stretch"
    )
    max_spot_price = col2.number_input(
        label="Max spot price",
        min_value=0.01,
        value=spot_price_input * 1.1,
        step=0.01,
        label_visibility="visible",
        icon=":material/euro:",
        width="stretch"
    )
    min_volatility, max_volatility = col3.slider(
        "Volatility range",
        0.0,
        1.0,
        (max(volatility_input - 0.2, 0.0), min(volatility_input + 0.2, 1.0))
    )

    call_map, put_map = st.columns(2)

    chart_size = 10
    x_prices = numpy.linspace(min_spot_price, max_spot_price, chart_size)
    y_volatilities = numpy.linspace(min_volatility, max_volatility, chart_size)

    call_data = []
    put_data = []
    for x_price in x_prices:
        call_x_data = []
        put_x_data = []
        for y_volatility in y_volatilities:
            pricing_model = PricingModel(
                x_price, strike_price_input, days_to_maturity_input,
                y_volatility, risk_free_interest_rate_input / 100
            )
            call_x_data.append(f"{pricing_model.call.price():.3}")
            put_x_data.append(f"{pricing_model.put.price():.3}")
        call_data.append(call_x_data)
        put_data.append(put_x_data)

    call_figure = plotly.imshow(
        call_data,
        text_auto=True,
        title="CALL",
        labels=dict(x="Spot Price (€)", y="Volatility"),
    )
    call_map.plotly_chart(call_figure, theme=None)

    put_figure = plotly.imshow(
        put_data,
        text_auto=True,
        title="PUT",
        labels=dict(x="Spot Price (€)", y="Volatility"),
    )
    put_map.plotly_chart(put_figure, theme=None)

