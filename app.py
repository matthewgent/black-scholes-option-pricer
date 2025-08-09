import numpy
import streamlit as st
import plotly.express as plotly
from black_scholes import PricingModel, Option
import heat_map

CHART_SIZE = 11
CURRENCY_ICON = ":material/euro:"
LINKEDIN_PROFILE_URL = "https://linkedin.com/in/matthewgent/"
LINKEDIN_LOGO_URL = ("https://upload.wikimedia.org/wikipedia/commons/thumb/8"
                     "/81/LinkedIn_icon.svg/144px-LinkedIn_icon.svg.png")

st.set_page_config(
    page_title="Black Scholes Option Pricer",
    page_icon=":material/bar_chart:",
    layout="wide",
)

st.sidebar.html(f"""
    <a
        style='display:flex;align-items:center;text-decoration:none;color:white;'
        href='{LINKEDIN_PROFILE_URL}'
        target='_blank'
    >
        <img
            src='{LINKEDIN_LOGO_URL}'
            style='width:30px;margin-right:1rem;'
            alt='Linkedin logo'
        >
        <div>Matthew Gent</div>
    </a>
""")

st.sidebar.divider()

spot_price_input = st.sidebar.number_input(
    label="Spot price",
    min_value=0.01,
    value=100.0,
    step=0.01,
    icon=CURRENCY_ICON,
)
strike_price_input = st.sidebar.number_input(
    label="Strike price",
    min_value=0.01,
    value=95.0,
    step=0.01,
    icon=CURRENCY_ICON,
)
days_to_maturity_input = st.sidebar.number_input(
    label="Days to maturity",
    min_value=1,
    value=30,
    step=1,
)
volatility_input = st.sidebar.number_input(
    label="Volatility (σ)",
    min_value=0.01,
    value=0.5,
    step=0.01,
)
risk_free_interest_rate_input = st.sidebar.number_input(
    label="Risk free interest rate",
    min_value=0.0,
    value=1.0,
    step=0.01,
)


def greek_badge(color: str, symbol: str, value: str) -> str:
    return f"""
        <div
            style='
                background-color:{color};
                width:100%;
                text-align:center;
                border-radius:2em;
                font-size:smaller;
                padding:2px;
                line-height:1.4em;
            '
        >
            {symbol}<br>{value}
        </div>
    """


def insert_greeks(st_column, heading: str, option: Option) -> None:
    st_column.metric(heading, f"€ {option.price():.2f}")
    col1, col2, col3, col4, col5 = st_column.columns(5)
    col1.html(greek_badge("chocolate", "Δ", f"{option.delta():.3}"))
    col2.html(greek_badge("darkgreen", "Γ", f"{option.gamma():.3}"))
    col3.html(greek_badge("darkorchid", "ν", f"{option.vega():.3}"))
    col4.html(greek_badge("firebrick", "θ", f"{option.theta():.3}"))
    col5.html(greek_badge("steelblue", "ρ", f"{option.rho():.3}"))


pricing_model = PricingModel(
    spot_price_input,
    strike_price_input,
    days_to_maturity_input,
    volatility_input,
    risk_free_interest_rate_input / 100,
)

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
        icon=CURRENCY_ICON,
    )
    max_spot_price = col2.number_input(
        label="Max spot price",
        min_value=0.01,
        value=110.0,
        step=0.01,
        icon=CURRENCY_ICON,
    )
    min_volatility, max_volatility = col3.slider(
        "Volatility range",
        0.0,
        1.0,
        (0.3, 0.7),
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
