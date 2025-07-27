import streamlit as st

st.set_page_config(page_title="Black Scholes Option Pricer", page_icon=":chart_increasing:", layout="wide")

st.sidebar.caption("Linkedin profile:")
st.sidebar.page_link("https://linkedin.com/in/matthewgent", label="Matthew Gent", icon=":material/link:")

st.sidebar.divider()

st.sidebar.number_input(
    label="Current asset price",
    min_value=0.0,
    value="min",
    step=0.01,
    label_visibility="visible",
    icon=":material/attach_money:",
    width="stretch"
)

st.sidebar.number_input(
    label="Strike price",
    min_value=0.0,
    value="min",
    step=0.01,
    label_visibility="visible",
    icon=":material/attach_money:",
    width="stretch"
)

st.sidebar.number_input(
    label="Time to maturity (days)",
    min_value=1,
    value=30,
    step=1,
    label_visibility="visible",
    width="stretch"
)

st.sidebar.number_input(
    label="Volatility (σ)",
    min_value=0.0,
    value="min",
    step=0.01,
    label_visibility="visible",
    width="stretch"
)

st.sidebar.number_input(
    label="Risk free interest rate",
    min_value=0.0,
    value="min",
    step=0.01,
    label_visibility="visible",
    width="stretch"
)

st.title("Black Scholes Option Pricer")