import streamlit as st
import numpy
import plotly.express as plotly
from black_scholes import PricingModel, Option

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

    chart_size = 11
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
            call_x_data.append(f"{pricing_model.call.price():.2f}")
            put_x_data.append(f"{pricing_model.put.price():.2f}")
        call_data.append(call_x_data)
        put_data.append(put_x_data)

    def plot_heat_map(st_column, title: str, map_data: list) -> None:
        heat_map = plotly.imshow(
            map_data,
            text_auto=True,
            title=title,
            labels=dict(x="Spot Price (€)", y="Volatility"),
            aspect="equal",
        )
        heat_map.update_layout(
            margin=dict(l=50, r=50, t=50, b=70),
        )
        heat_map.update_coloraxes(showscale=False)
        heat_map.update_xaxes(
            tickangle=90,
            tickmode="array",
            tickvals=list(range(11)),
            ticktext=[f"{price:.2f}" for price in x_prices]
        )
        heat_map.update_yaxes(
            tickmode="array",
            tickvals=list(range(11)),
            ticktext=[f"{volatility:.2g}" for volatility in y_volatilities]
        )
        st_column.plotly_chart(heat_map, theme=None)

    plot_heat_map(call_map_col, "CALL", call_data)
    plot_heat_map(put_map_col, "PUT", put_data)
