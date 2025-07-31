import math
from scipy.stats import norm
import streamlit as st
from abc import ABC, abstractmethod

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

st.title("Black Scholes Option Pricer")

class BlackScholesEnvironment:
    __days_per_year = 365

    def __init__(self, spot_price: float, strike_price: float, days_to_maturity: float, volatility: float, risk_free_interest_rate: float):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.days_to_maturity = days_to_maturity
        self.volatility = volatility
        self.risk_free_interest_rate = risk_free_interest_rate

        self.years_to_maturity = days_to_maturity / self.__days_per_year
        d1_numerator = math.log(spot_price / strike_price) + (risk_free_interest_rate + 0.5 * volatility ** 2) * self.years_to_maturity
        d1_denominator = volatility * math.sqrt(self.years_to_maturity)
        self.d1 = d1_numerator / d1_denominator
        self.d2 = self.d1 - (volatility * math.sqrt(self.years_to_maturity))
        self.d1_cdf = norm.cdf(self.d1)
        self.d2_cdf = norm.cdf(self.d2)
        self.exponential_component = math.exp(-risk_free_interest_rate * self.years_to_maturity)

class Option(ABC):
    def __init__(self, env: BlackScholesEnvironment):
        self.env = env

    @abstractmethod
    def price(self):
        pass

    @abstractmethod
    def delta(self):
        pass

class Call(Option):
    def price(self) -> float:
        return self.env.spot_price * self.env.d1_cdf - self.env.strike_price * self.env.exponential_component * self.env.d2_cdf

    def delta(self) -> float:
        return self.env.exponential_component * self.env.d1_cdf

class Put(Option):
    def price(self) -> float:
        return self.env.strike_price * self.env.exponential_component * (1 - self.env.d2_cdf) - self.env.spot_price * (1 - self.env.d1_cdf)

    def delta(self) -> float:
        return self.env.exponential_component * (self.env.d1_cdf - 1)

environment = BlackScholesEnvironment(spot_price_input, strike_price_input, days_to_maturity_input, volatility_input, risk_free_interest_rate_input)
call = Call(environment)
put = Put(environment)

call_column, put_column = st.columns(2)

call_column.metric("CALL", f"€{call.price():.2f}", border=True)
call_column.badge("Δ = " + f"{call.delta():.3f}", color="blue")
call_column.badge("Γ = " + f"", color="green")

put_column.metric("PUT", f"€{put.price():.2f}", border=True)
put_column.badge("Δ = " + f"{put.delta():.3f}", color="blue")
put_column.badge("Γ = " + f"", color="green")
