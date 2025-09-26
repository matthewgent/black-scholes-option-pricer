from abc import ABC, abstractmethod
from scipy.stats import norm
import math


class Option(ABC):
    def __init__(
            self, spot_price: float, strike_price: float,
            years_to_maturity: float, volatility: float, d1_cdf: float,
            d2_cdf: float, d1_pdf: float, risk_free_interest_rate: float,
            continuous_discounting_factor: float):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.years_to_maturity = years_to_maturity
        self.volatility = volatility
        self.d1_cdf = d1_cdf
        self.d2_cdf = d2_cdf
        self.d1_pdf = d1_pdf
        self.risk_free_interest_rate = risk_free_interest_rate
        self.continuous_discounting_factor = continuous_discounting_factor

    @abstractmethod
    def price(self) -> float:
        pass

    @abstractmethod
    def delta(self) -> float:
        pass

    @abstractmethod
    def theta(self) -> float:
        pass

    @abstractmethod
    def rho(self) -> float:
        pass

    # The following greeks have shared value for both call and put options
    def gamma(self) -> float:
        denominator = (self.spot_price
                       * self.volatility
                       * math.sqrt(self.years_to_maturity))
        return self.d1_pdf / denominator

    def vega(self) -> float:
        return (self.spot_price
                * self.d1_pdf
                * math.sqrt(self.years_to_maturity))


class Call(Option):
    def price(self) -> float:
        return (self.spot_price
                * self.d1_cdf
                - self.strike_price
                * self.continuous_discounting_factor
                * self.d2_cdf)

    def delta(self) -> float:
        return self.d1_cdf

    def theta(self) -> float:
        numerator = self.spot_price * self.d1_pdf * self.volatility
        denominator = 2 * self.years_to_maturity
        final_component = (self.risk_free_interest_rate
                           * self.strike_price
                           * self.continuous_discounting_factor
                           * self.d2_cdf)
        return -(numerator / denominator) - final_component

    def rho(self) -> float:
        return (self.strike_price
                * self.years_to_maturity
                * self.continuous_discounting_factor
                * self.d2_cdf)


class Put(Option):
    def price(self) -> float:
        return (self.strike_price * self.continuous_discounting_factor *
                (1 - self.d2_cdf) - self.spot_price * (1 - self.d1_cdf))

    def delta(self) -> float:
        return self.d1_cdf - 1

    def theta(self) -> float:
        numerator = self.spot_price * self.d1_pdf * self.volatility
        denominator = 2 * self.years_to_maturity
        final_component = (self.risk_free_interest_rate
                           * self.strike_price
                           * self.continuous_discounting_factor
                           * (self.d2_cdf - 1))
        return -(numerator / denominator) + final_component

    def rho(self) -> float:
        return (self.strike_price
                * self.years_to_maturity
                * self.continuous_discounting_factor
                * (self.d2_cdf - 1))


class PricingModel:
    __days_per_year: int = 365

    def __init__(
            self, spot_price: float, strike_price: float,
            days_to_maturity: float, volatility: float,
            risk_free_interest_rate: float):
        years_to_maturity = days_to_maturity / self.__days_per_year

        d1_numerator = (math.log(spot_price / strike_price)
                        + (risk_free_interest_rate + 0.5 * volatility ** 2)
                        * years_to_maturity)
        d1_denominator = volatility * math.sqrt(years_to_maturity)
        d1 = d1_numerator / d1_denominator
        d2 = d1 - (volatility * math.sqrt(years_to_maturity))

        d1_cdf = norm.cdf(d1)
        d2_cdf = norm.cdf(d2)
        d1_pdf = norm.pdf(d1)

        continuous_discounting_factor = math.exp(
            -risk_free_interest_rate * years_to_maturity)

        self.call: Call = Call(
            spot_price, strike_price, years_to_maturity, volatility, d1_cdf,
            d2_cdf, d1_pdf, risk_free_interest_rate,
            continuous_discounting_factor)

        self.put: Put = Put(
            spot_price, strike_price, years_to_maturity, volatility, d1_cdf,
            d2_cdf, d1_pdf, risk_free_interest_rate,
            continuous_discounting_factor)
