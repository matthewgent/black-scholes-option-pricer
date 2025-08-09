import numpy
import streamlit as st
import plotly.express as plotly
from black_scholes import PricingModel, Option
import heat_map

CHART_SIZE = 11

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


def greek_badge(color: str, symbol: str, value: str) -> str:
    styles = [
        f"background-color:{color}",
        "width:100%",
        "text-align:center",
        "border-radius:2em",
        "font-size:smaller",
        "padding:2px",
        "line-height:1.4em"
    ]
    styles_string = ";".join(styles)
    return f"<div style='{styles_string}'>{symbol}<br>{value}</div>"


def insert_greeks(st_column, heading: str, option: Option) -> None:
    st_column.metric(heading, f"€ {option.price():.2f}")
    col1, col2, col3, col4, col5 = st_column.columns(5)
    col1.html(greek_badge("chocolate", "Δ", f"{option.delta():.3}"))
    col2.html(greek_badge("darkgreen", "Γ", f"{option.gamma():.3}"))
    col3.html(greek_badge("darkorchid", "ν", f"{option.vega():.3}"))
    col4.html(greek_badge("firebrick", "θ", f"{option.theta():.3}"))
    col5.html(greek_badge("steelblue", "ρ", f"{option.rho():.3}"))


pricing_model = PricingModel(
    spot_price_input, strike_price_input, days_to_maturity_input,
    volatility_input, risk_free_interest_rate_input / 100)

call, put = st.columns(2, border=True)

insert_greeks(call, "CALL", pricing_model.call)
insert_greeks(put, "PUT", pricing_model.put)

st.html('<br>')

with st.container(border=True):
    col1, col2, col3 = st.columns([1, 1, 2], gap="medium")
    min_spot_price = col1.number_input(
        label="Min spot price",
        min_value=0.01,
        value=90.0,
        step=0.01,
        label_visibility="visible",
        icon=":material/euro:",
        width="stretch"
    )
    max_spot_price = col2.number_input(
        label="Max spot price",
        min_value=0.01,
        value=110.0,
        step=0.01,
        label_visibility="visible",
        icon=":material/euro:",
        width="stretch"
    )
    min_volatility, max_volatility = col3.slider(
        "Volatility range",
        0.0,
        1.0,
        (0.3, 0.7)
    )

    call_map_col, put_map_col = st.columns(2)

    x_prices = numpy.linspace(min_spot_price, max_spot_price, CHART_SIZE)
    y_volatilities = numpy.linspace(min_volatility, max_volatility, CHART_SIZE)

    call_data, put_data = heat_map.data(
        x_prices,
        y_volatilities,
        strike_price_input,
        days_to_maturity_input,
        risk_free_interest_rate_input,
    )

    heat_map.plot(call_map_col, "CALL", call_data, x_prices, y_volatilities)
    heat_map.plot(put_map_col, "PUT", put_data, x_prices, y_volatilities)
