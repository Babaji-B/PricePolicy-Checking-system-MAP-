import json
import mysql.connector
import os
from db_connection import get_db_connection

def identify_violating_sellers(date_input):
    """
    Identifies violating sellers based on the threshold JSON and stores them in the violated_sellers table.
    """
    try:
        # Dynamically get the file path of thresholds.json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        thresholds_path = os.path.join(script_dir, "thresholds.json")

        # Load threshold values from JSON file
        with open(thresholds_path, "r") as file:
            thresholds = json.load(file)
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 1: Fetch relevant data from price_monitoring for the given date
        query = """
            SELECT Homologated_Name, Region, Sub_Category, COUNT(*) as violation_count
            FROM price_monitoring
            WHERE Violation_date = %s
            GROUP BY Homologated_Name, Region, Sub_Category
        """
        cursor.execute(query, (date_input,))
        results = cursor.fetchall()
        
        violating_sellers = []
        
        # Step 2: Comparing the vilation count with threshold values
        for seller, region, subcategory, violation_count in results:
            threshold_value = thresholds.get(region, {}).get(subcategory, None)
            if threshold_value is not None and violation_count > threshold_value:
                violating_sellers.append((seller, region, subcategory, violation_count, threshold_value, date_input))
        
        # Step 3: Insert violating sellers into violated_sellers table
        if violating_sellers:
            insert_query = """
                INSERT INTO violated_sellers (homologated_seller, region, subcategory, violation_count, threshold_value, violation_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, violating_sellers)
            conn.commit()
            print("✅ Violating sellers stored successfully!")
        else:
            print("✅ No violations exceeded threshold for this date.")
        
    except Exception as e:
        print(f"❌ Error identifying violating sellers: {e}")
    finally:
        # Closing the Connections
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()