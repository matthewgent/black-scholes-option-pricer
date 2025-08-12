import pytest
from option_pricer.black_scholes import PricingModel


class TestPricingModel:
    model: PricingModel = None

    @classmethod
    def setup_class(cls) -> None:
        cls.model = PricingModel(100, 90, 365, 0.5, 0.02)

    # CALL

    def test_call_price(self) -> None:
        assert pytest.approx(self.model.call.price(), abs=0.005) == 25.04

    def test_call_delta(self) -> None:
        assert pytest.approx(self.model.call.delta(), abs=0.0005) == 0.692

    def test_call_gamma(self) -> None:
        assert pytest.approx(self.model.call.gamma(), abs=5e-6) == 0.00704

    def test_call_vega(self) -> None:
        assert pytest.approx(self.model.call.vega(), abs=0.05) == 35.2

    def test_call_theta(self) -> None:
        assert pytest.approx(self.model.call.theta(), abs=0.005) == -9.68

    def test_call_rho(self) -> None:
        assert pytest.approx(self.model.call.rho(), abs=0.05) == 44.1

    # PUT

    def test_put_price(self) -> None:
        assert pytest.approx(self.model.put.price(), abs=0.005) == 13.26

    def test_put_delta(self) -> None:
        assert pytest.approx(self.model.put.delta(), abs=0.0005) == -0.308

    def test_put_theta(self) -> None:
        assert pytest.approx(self.model.put.theta(), abs=0.005) == -9.68

    def test_put_rho(self) -> None:
        assert pytest.approx(self.model.put.rho(), abs=0.05) == -44.1
