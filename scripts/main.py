from store_data import store_all_seller_data
from voilated_sellers import identify_violating_sellers
from datetime import datetime

def validate_date(date_str):
    """Validate if the input date is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def main():
    while True:
        date_input = input("Enter the date (YYYY-MM-DD) or type 'exit' to quit: ").strip()
        if date_input.lower() == 'exit':
            print("👋 Exiting the program. Goodbye!")
            break
        
        if not validate_date(date_input):
            print("❌ Invalid date format. Please enter in YYYY-MM-DD format.")
            continue
        
        print(f"📌 Processing data for date: {date_input}")
        try:
            # Step 1: Storing data in price_monitoring
            store_all_seller_data(date_input)
            print("✅ Data stored successfully in price_monitoring table!")

            # Step 2: Identify violating sellers & storing in violated_sellers
            identify_violating_sellers(date_input)
            print("✅ Violating sellers processed successfully!")

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
