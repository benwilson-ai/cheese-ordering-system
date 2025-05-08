from config import load_env, FIXTURES
from src.tools.db_utils import query_sql

load_env()

# import_csv_to_vector(f"{FIXTURES}/retail-leases_2025-01-21_014339.csv")
query_sql("SELECT AVG(CurrentRentPa) AS average_rent FROM retail_leases WHERE CentreName LIKE '%Townsville%';")