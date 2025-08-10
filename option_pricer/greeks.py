from components import greek_badge as badge
from black_scholes import Option


def insert(st_column, heading: str, option: Option) -> None:
    st_column.metric(heading, f"€ {option.price():.2f}")
    col1, col2, col3, col4, col5 = st_column.columns(5)
    col1.html(badge("chocolate", "Δ", f"{option.delta():.3}"))
    col2.html(badge("darkgreen", "Γ", f"{option.gamma():.3}"))
    col3.html(badge("darkorchid", "ν", f"{option.vega():.3}"))
    col4.html(badge("firebrick", "θ", f"{option.theta():.3}"))
    col5.html(badge("steelblue", "ρ", f"{option.rho():.3}"))
