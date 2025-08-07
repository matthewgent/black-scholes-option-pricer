import streamlit as st
from black_scholes import PricingModel

st.set_page_config(
    page_title="Black Scholes Option Pricer",
    page_icon=":chart_increasing:",
    layout="wide")

# Sidebar
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

# Main page
st.title("Black Scholes Option Pricer")


def badge(color: str, symbol: str, value: str) -> str:
    styles = [
        f"background-color:{color}",
        "width:100%",
        "text-align:center",
        "border-radius:4px",
        "font-size:smaller",
        "padding:2px",
        "line-height:1.4em"
    ]
    return f"<div style='{";".join(styles)}'>{symbol}<br>{value}</div>"


def greeks(column, heading: str, pricing_model: PricingModel) -> None:
    column.metric(heading, f"€ {pricing_model.price():.2f}")
    col1, col2, col3, col4, col5 = column.columns(5)
    col1.html(badge("chocolate", "Δ", f"{pricing_model.delta():.3}"))
    col2.html(badge("darkgreen", "Γ", f"{pricing_model.gamma():.3}"))
    col3.html(badge("darkorchid", "ν", f"{pricing_model.vega():.3}"))
    col4.html(badge("firebrick", "θ", f"{pricing_model.theta():.3}"))
    col5.html(badge("steelblue", "ρ", f"{pricing_model.rho():.3}"))


pricing_model = PricingModel(
    spot_price_input, strike_price_input, days_to_maturity_input,
    volatility_input, risk_free_interest_rate_input / 100)

call, put = st.columns(2, border=True)
greeks(call, "CALL", pricing_model.call)
greeks(put, "PUT", pricing_model.put)
