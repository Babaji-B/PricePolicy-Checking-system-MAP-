import requests
import time
import json
import os
from config import EXCHANGE_RATE_API_URL
from region_to_curr import get_currency_code

# Cache file path
CACHE_FILE = os.path.join(os.path.dirname(__file__), "exchange_cache.json")
CACHE_EXPIRATION = 24 * 60 * 60  # 24 hours


# Load cache from file (if it exists)
def load_cache():
    """Load exchange rate cache from file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("⚠️ Warning: Cache file is corrupted. Resetting cache.")
            return {}
    return {}

# Save cache to file
def save_cache(cache):
    """Save exchange rate cache to file."""
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file)

# Load cache at the start
exchange_rate_cache = load_cache()

def fetch_all_exchange_rates():
    """Fetch all exchange rates from API and store in cache (single call)."""
    print(f" Fetching exchange rates from API...")
    response = requests.get(EXCHANGE_RATE_API_URL)

    if response.status_code == 200:
        data = response.json()
        conversion_rates = data.get("conversion_rates", {})

        if conversion_rates:
            exchange_rate_cache["rates"] = conversion_rates
            exchange_rate_cache["timestamp"] = time.time()
            save_cache(exchange_rate_cache)
            print(f"✅ Exchange rates fetched and stored in cache.")
            return conversion_rates

    print(f"❌ API request failed with status code {response.status_code}")
    return None

def get_exchange_rate(currency_code):
    """Fetch exchange rate for a given currency from cache or API."""
    current_time = time.time()

    # Check if cache is available and not expired
    if "rates" in exchange_rate_cache and current_time - exchange_rate_cache["timestamp"] < CACHE_EXPIRATION:
        rates = exchange_rate_cache["rates"]
        if currency_code in rates:
            #print(f"✅ Using cached exchange rate for {currency_code}: {rates[currency_code]}")
            return rates[currency_code]
    else:
        # If cache is empty or expired, fetch new rates from API
        rates = fetch_all_exchange_rates()
        if rates and currency_code in rates:
            #print(f"✅ Fresh exchange rate for {currency_code}: {rates[currency_code]}")
            return rates[currency_code]

    print(f"❌ Exchange rate for {currency_code} not found.")
    return None

def get_exchange_rate_for_region(region):
    """Retrieve exchange rate based on region name."""
    currency_code = get_currency_code(region)  # Converting region to currency

    if not currency_code:
        print(f"❌ Error: No currency mapping found for region '{region}'")
        return None

    return get_exchange_rate(currency_code)
