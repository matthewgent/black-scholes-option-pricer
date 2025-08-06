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

call, put = st.columns(2, border=True)
call.metric("CALL", f"€ {model.call.price():.2f}")
call_delta, call_gamma, call_vega, call_theta, call_rho = call.columns(5)
call_delta.badge(
    "Δ = " + f"{model.call.delta():.3f}",
    color="blue",
    )
call_gamma.badge(
    "Γ = " + f"{gamma:.3e}",
    color="green",
    width="stretch")
call_vega.badge("ν = " + f"{vega:.3f}", color="orange")
call_theta.badge("θ = " + f"{model.call.theta():.3f}", color="red")
call_rho.badge("ρ = " + f"{model.call.rho():.3f}", color="violet")


put.metric("CALL", f"€ {model.call.price():.2f}")
put_delta, put_gamma, put_vega, put_theta, put_rho = put.columns(5)
put_delta.badge(
    "Δ = " + f"{model.call.delta():.3f}",
    color="blue",
    )
put_gamma.badge(
    "Γ = " + f"{gamma:.3e}",
    color="green",
    width="stretch")
put_vega.badge("ν = " + f"{vega:.3f}", color="orange")
put_theta.badge("θ = " + f"{model.call.theta():.3f}", color="red")
put_rho.badge("ρ = " + f"{model.call.rho():.3f}", color="violet")
