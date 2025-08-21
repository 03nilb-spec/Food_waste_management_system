import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='food_wastage'
    )

def run_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# --- Query functions ---
def count_providers_and_receivers_per_city():
    query = """
    SELECT City, 
           COUNT(DISTINCT Provider_ID) AS num_providers,
           (SELECT COUNT(*) FROM receiver) AS num_receivers
    FROM providers
    GROUP BY City
    """
    return run_query(query)

def top_provider_type_by_food():
    query = """
    SELECT p.type, SUM(f.Quantity) AS total_food_quantity
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.type
    ORDER BY total_food_quantity DESC
    LIMIT 1
    """
    return run_query(query)


def get_providers_contact_info_by_city(city):
    query = """
    SELECT name, contact
    FROM providers
    WHERE City = %s
    """
    return run_query(query, params=(city,))



def top_food_receiver():
    query = """
    SELECT r.Name, r.Receiver_ID, SUM(f.Quantity) AS total_claimed
    FROM receiver r
    JOIN claim_data c ON r.Receiver_ID = c.Receiver_ID
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY r.Name, r.Receiver_ID
    ORDER BY total_claimed DESC
    LIMIT 10;
    """
    return run_query(query)

def total_quantity_of_food_available_from_all_providers():
    query = """
    SELECT SUM(Quantity) AS total_food_available
    FROM food_listings
    """
    return run_query(query)

def food_claim_percentage_by_status():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
    query = """
    SELECT 
        Status,
        COUNT(*) AS count,
        ROUND((COUNT(*) * 100.0) / total.total_count, 2) AS percentage
    FROM claim_data
    JOIN (SELECT COUNT(*) AS total_count FROM claim_data) total
    GROUP BY Status
    """
    df = pd.read_sql(query, conn)
    cursor.close()
    conn.close()
    return df

def average_food_claimed_per_receiver():
    query = """
    SELECT 
        AVG(receiver_total) AS avg_quantity_claimed_per_receiver
    FROM (
        SELECT 
            c.Receiver_ID, 
            SUM(f.Quantity) AS receiver_total
        FROM claim_data c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY c.Receiver_ID
    ) AS subquery
    """
    return run_query(query)

def top_city_with_highest_food_listing():
    query ="""
    SELECT p.City, COUNT(*) AS listings_count
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.City
    ORDER BY listings_count DESC
    LIMIT 1
    """
    return run_query(query)

def most_commomn_available_food_by_type():
    query  = """
    SELECT Food_Type, COUNT(*) AS count
    FROM food_listings
    GROUP BY Food_Type
    ORDER BY count DESC
    """
    return run_query(query)

def food_claim_made_for_each_item():
    query = """
    SELECT Food_ID, COUNT(*) AS claim_count
    FROM claim_data
    GROUP BY Food_ID
    ORDER BY claim_count DESC
    """
    return run_query(query)

def highest_number_of_food_claims_by_provider():
    query = """
    SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS successful_claims
    FROM providers p
    JOIN food_listings f ON p.Provider_ID = f.Provider_ID
    JOIN claim_data c ON f.Food_ID = c.Food_ID
    WHERE c.Status = 'completed'
    GROUP BY p.Provider_ID, p.Name
    ORDER BY successful_claims DESC
    LIMIT 1
    """
    return run_query(query)

def most_claimed_meal_by_type():
    query = """
    SELECT 
        f.Meal_Type,
        SUM(f.Quantity) AS total_quantity_claimed
    FROM claim_data c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Meal_Type
    ORDER BY total_quantity_claimed DESC
    LIMIT 1
    """
    return run_query(query)

def total_food_donated_by_provider():
    query = """
    SELECT 
        p.Provider_ID,
        p.type,
        SUM(f.Quantity) AS total_quantity_donated
    FROM providers p
    JOIN food_listings f ON p.Provider_ID = f.Provider_ID
    GROUP BY p.Provider_ID, p.type
    ORDER BY total_quantity_donated DESC
    """
    return run_query(query,())


def execute_write(sql, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    cur.close()
    conn.close()

# CREATE: add a food listing
def add_food_listing(food_id, food_name, qty, expiry_date, provider_id, provider_type, location, food_type, meal_type):
    sql = """
    INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    execute_write(sql, (food_id, food_name, qty, expiry_date, provider_id, provider_type, location, food_type, meal_type))

# UPDATE: change claim status
def update_claim_status(claim_id, new_status):
    sql = "UPDATE claim_data SET Status = %s WHERE Claim_ID = %s"
    execute_write(sql, (new_status, claim_id))

# DELETE: remove a food listing
def delete_food_listing(food_id):
    sql = "DELETE FROM food_listings WHERE Food_ID = %s"
    execute_write(sql, (food_id,))
