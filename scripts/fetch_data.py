from db_connection import get_db_connection

def fetch_seller_data(date_input):
    """Fetch all rows from the seller table for the specified date."""
    seller_table = date_input.replace("-", "_")
    query = f"SELECT * FROM {seller_table};"  # Query to fetch all rows
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        seller_data = cursor.fetchall()
        
        # Close cursor and connection
        cursor.close()
        conn.close()
        
        return seller_data
    return None
