import numpy as np
import streamlit as st
import plotly.express as plotly
from black_scholes import PricingModel, Option
import heat_map
import greeks
from components import linkedin_link


def build() -> None:

    chart_size = 11
    currency_icon = ":material/euro:"

    st.set_page_config(
        page_title="Black Scholes Option Pricer",
        page_icon=":material/bar_chart:",
        layout="wide",
    )

    st.sidebar.html(linkedin_link(
        "https://linkedin.com/in/matthewgent/",
        "Matthew Gent",
    ))

    st.sidebar.divider()

    spot_price_input = st.sidebar.number_input(
        label="Spot price",
        min_value=0.01,
        value=100.0,
        step=0.01,
        icon=currency_icon,
    )
    strike_price_input = st.sidebar.number_input(
        label="Strike price",
        min_value=0.01,
        value=95.0,
        step=0.01,
        icon=currency_icon,
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

    pricing_model = PricingModel(
        spot_price_input,
        strike_price_input,
        days_to_maturity_input,
        volatility_input,
        risk_free_interest_rate_input / 100,
    )

    call, put = st.columns(2, border=True)

    greeks.insert(call, "CALL", pricing_model.call)
    greeks.insert(put, "PUT", pricing_model.put)

    st.html('<br>')

    with st.container(border=True):
        col1, col2, col3 = st.columns((1, 1, 2), gap="medium")
        min_spot_price = col1.number_input(
            label="Min spot price",
            min_value=0.01,
            value=90.0,
            step=0.01,
            icon=currency_icon,
        )
        max_spot_price = col2.number_input(
            label="Max spot price",
            min_value=0.01,
            value=110.0,
            step=0.01,
            icon=currency_icon,
        )
        min_volatility, max_volatility = col3.slider(
            "Volatility range",
            0.0,
            1.0,
            (0.3, 0.7),
        )

        call_map_col, put_map_col = st.columns(2)

        x_prices = np.linspace(
            min_spot_price,
            max_spot_price,
            chart_size
        )
        y_volatilities = np.linspace(
            min_volatility,
            max_volatility,
            chart_size
        )

        call_data, put_data = heat_map.data(
            x_prices,
            y_volatilities,
            strike_price_input,
            days_to_maturity_input,
            risk_free_interest_rate_input,
        )

        heat_map.plot(
            call_map_col,
            "CALL",
            call_data,
            x_prices,
            y_volatilities
        )
        heat_map.plot(
            put_map_col,
            "PUT",
            put_data,
            x_prices,
            y_volatilities
        )
