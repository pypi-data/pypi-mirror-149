from typing import Optional


def format_symbol(symbol: str):
    return symbol.upper().replace("/", "_")


def format_market(market: str):
    return market.lower().replace("/", "_")


def format_websocket_market(market: str):
    return market.lower().replace("/", "").replace("_", "")


def format_websocket_user_market(market: str):
    suffix = "default"
    market = market.lower()
    if market.endswith(suffix):
        return market[: len(market) - len(suffix)]
    return market


def format_endpoint(
    endpoint: str,
    symbol: Optional[str] = None,
    future_account_type: int = 1,
    currency: Optional[str] = None,
) -> str:
    if symbol is not None:
        quote = symbol.partition("/")[2]
        if quote == "ZUSD":
            quote = "usdt"
        return endpoint.format(quote=quote.lower())
    if currency is not None:
        return endpoint.format(quote=currency.lower())

    if future_account_type == 1:
        return endpoint.format(quote="usdt")
    elif future_account_type == 2:
        return endpoint.format(quote="qc")
    else:
        raise ValueError(f"{future_account_type} account type not supported")
