# Dictionary to map region names to currency codes
region_to_currency = {
    "USA": "USD",
    "UAE": "AED",
    "UK": "GBP",
    "IND": "INR",
    "CAN": "CAD"
}

def get_currency_code(region):
    """Return the currency code for a given region name."""
    return region_to_currency.get(region.upper(), None)