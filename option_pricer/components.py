def linkedin_link(profile_url: str, name: str) -> str:
    logo_url = ("https://upload.wikimedia.org/wikipedia/commons/thumb/8"
                "/81/LinkedIn_icon.svg/144px-LinkedIn_icon.svg.png")

    return f"""
        <a
            style='display:flex;align-items:center;text-decoration:none;color:white;'
            href='{profile_url}'
            target='_blank'
        >
            <img
                src='{logo_url}'
                style='width:30px;margin-right:1rem;'
                alt='Linkedin logo'
            >
            <div>{name}</div>
        </a>
    """


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
