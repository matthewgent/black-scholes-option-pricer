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
    value="min",
    step=0.01,
    label_visibility="visible",
    icon=":material/euro:",
    width="stretch"
)

strike_price_input = st.sidebar.number_input(
    label="Strike price",
    min_value=0.01,
    value="min",
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
    value="min",
    step=0.01,
    label_visibility="visible",
    width="stretch"
)

risk_free_interest_rate_input = st.sidebar.number_input(
    label="Risk free interest rate",
    min_value=0.0,
    value="min",
    step=0.01,
    label_visibility="visible",
    width="stretch"
)

# Main page
st.title("Black Scholes Option Pricer")

model = PricingModel(
    spot_price_input, strike_price_input, days_to_maturity_input,
    volatility_input, risk_free_interest_rate_input)

# Calculate constant greeks only once
gamma = model.call.gamma()
vega = model.call.vega()

call_column, put_column = st.columns(2)

call_column.metric("CALL", f"€ {model.call.price():.2f}", border=True)
call_column.badge("Δ = " + f"{model.call.delta():.3f}", color="blue")
call_column.badge("Γ = " + f"{gamma:.3e}", color="green")
call_column.badge("ν = " + f"{vega:.3f}", color="orange")
call_column.badge("θ = " + f"{model.call.theta():.3f}", color="red")
call_column.badge("ρ = " + f"{model.call.rho():.3f}", color="violet")

put_column.metric("PUT", f"€ {model.put.price():.2f}", border=True)
put_column.badge("Δ = " + f"{model.put.delta():.3f}", color="blue")
put_column.badge("Γ = " + f"{gamma:.3e}", color="green")
put_column.badge("ν = " + f"{vega:.3f}", color="orange")
put_column.badge("θ = " + f"{model.put.theta():.3f}", color="red")
put_column.badge("ρ = " + f"{model.put.rho():.3f}", color="violet")
