from currency_cache import get_exchange_rate_for_region  # Import existing function
from db_connection import get_db_connection
from decimal import Decimal

def store_all_seller_data(date_input):
    """Fetch seller data, apply real-time exchange rates, and store violations."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Checking if data for the given date is already in price_monitoring
    check_query = """
        SELECT COUNT(*) FROM price_monitoring WHERE Violation_date = %s;
    """
    cursor.execute(check_query, (date_input,))
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"⚠️ The data is already available for {date_input} in the price_monitoring table. No new records added.")
        cursor.close()
        conn.close()
        return

    # Defining seller table dynamically
    seller_table = f"{date_input.replace('-', '_')}"
    
    # Fetching seller data
    query = f'''
        SELECT 
            s.SKU, s.adv_price, s.region, s.Marketplace, 
            s.seller_name AS Seller_Name, sm.Homologated_sellers AS Homologated_Name, 
            p.MAP, p.LPP, cm.PL, cm.Category, cm.Subcategory, pr.Season, pr.Promotion 
        FROM {seller_table} s
        LEFT JOIN pricelist p ON s.SKU = p.SKU
        LEFT JOIN category_mapping cm ON s.SKU = cm.SKU
        LEFT JOIN seller_mapping sm ON s.seller_name = sm.sellers_name
        LEFT JOIN promotion pr ON s.SKU = pr.SKU;
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()

    processed_data = []
    for row in results:
        (
            SKU, adv_price, region, marketplace, seller_name, homologated_name, 
            MAP, LPP, PL, category, subcategory, season, promotion_price
        ) = row

        # Converting prices to Decimal to avoid float precision loss
        adv_price = Decimal(adv_price) if adv_price else Decimal("0.0")
        MAP = Decimal(MAP) if MAP else Decimal("0.0")
        LPP = Decimal(LPP) if LPP else Decimal("0.0")
        promotion_price = Decimal(promotion_price) if promotion_price else Decimal("0.0")

        # Get exchange rates safely as Decimal
        region_exchange_rate = Decimal(get_exchange_rate_for_region(region) or 1.0)
        inr_exchange_rate = Decimal(get_exchange_rate_for_region("IND") or 1.0)

        # Converting prices to a base form
        adv_price_converted = adv_price / region_exchange_rate
        MAP_converted = MAP / inr_exchange_rate
        LPP_converted = LPP / inr_exchange_rate
        promotion_price_converted = promotion_price / inr_exchange_rate

        # Finding violation status
        violation_date = date_input if adv_price_converted < (LPP_converted - promotion_price_converted) else None

        # Append processed data to processed_data list
        processed_data.append((
            SKU, violation_date, PL, category, subcategory, region, marketplace, 
            seller_name, homologated_name, MAP_converted, LPP_converted, 
            adv_price_converted, season, promotion_price_converted
        ))

    # Inserting processed data into price_monitoring table
    if processed_data:
        insert_query = '''
            INSERT INTO price_monitoring (
                SKU, Violation_date, PL, Category, Sub_category, 
                Region, Marketplace, Seller_Name, Homologated_Name, 
                MAP_Price, LPP, Advertised_Price, Season, Promotional_Price
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.executemany(insert_query, processed_data)
        conn.commit()
        print(f"✅ Successfully stored {cursor.rowcount} records in price_monitoring with real-time exchange rates.")

    else:
        print("✅ No data found in the seller table.")

    cursor.close()
    conn.close()