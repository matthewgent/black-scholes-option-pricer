import math
from scipy.stats import norm
import streamlit as st

st.set_page_config(page_title="Black Scholes Option Pricer", page_icon=":chart_increasing:", layout="wide")

st.sidebar.caption("Linkedin profile:")
st.sidebar.page_link("https://linkedin.com/in/matthewgent", label="Matthew Gent", icon=":material/link:")

st.sidebar.divider()

spot_price_input = st.sidebar.number_input(
    label="Spot price",
    min_value=0.01,
    value="min",
    step=0.01,
    label_visibility="visible",
    icon=":material/attach_money:",
    width="stretch"
)

strike_price_input = st.sidebar.number_input(
    label="Strike price",
    min_value=0.01,
    value="min",
    step=0.01,
    label_visibility="visible",
    icon=":material/attach_money:",
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

st.title("Black Scholes Option Pricer")

def black_scholes_prices(spot_price: float, strike_price: float, days_to_maturity: float, volatility: float, risk_free_interest_rate: float) -> tuple[float, float]:
    years_to_maturity = days_to_maturity / 365

    d1_numerator = math.log(spot_price / strike_price) + (risk_free_interest_rate + 0.5 * volatility**2) * years_to_maturity
    d1_denominator = volatility * math.sqrt(years_to_maturity)
    d1 = d1_numerator / d1_denominator

    d2 = d1 - (volatility * math.sqrt(years_to_maturity))

    d1_cdf = norm.cdf(d1)
    d2_cdf = norm.cdf(d2)
    exponential_component = math.exp(-risk_free_interest_rate * years_to_maturity)
    call = spot_price * d1_cdf - strike_price * exponential_component * d2_cdf
    put = strike_price * exponential_component * (1 - d2_cdf) - spot_price * (1 - d1_cdf)

    return call, put

call_price, put_price = black_scholes_prices(spot_price_input, strike_price_input, days_to_maturity_input, volatility_input, risk_free_interest_rate_input)

call_column, put_column = st.columns(2)
call_column.metric("CALL", f"${call_price:.2f}", border=True)
put_column.metric("PUT", f"${put_price:.2f}", border=True)



st.badge()