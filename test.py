# from config import load_env, FIXTURES
# from src.tools.db_utils import query_sql

# load_env()
cheese = {
    "cheese_type": "Cheese, Blend, Mozz, Wm & Ps, Premio Shred, 6/5 Lb - 112492",
    "image_url": "https://shop.kimelo.com/_next/image?url=https%3A%2F%2Fd3tlizm80tjdt4.cloudfront.net%2Fimage%2F13860%2Fimage%2Fsm-1505a5e7aa7570e69e7ca77cf4c49a97.png&w=3840&q=50",
    "product_url": "https://shop.kimelo.com/sku/cheese-blend-mozz-wm-ps-premio-shred-65-lb-112492/112492",
    "brand": "Galbani Premio",
    "bonus": "Buy 10+ pay $98.46",
    "price": "$101.51",
    "price_per_lb": "$3.38/LB",
    "cheese_form": "Shredded Cheese",
    "sku": "112492",
    "upc": "112492",
    "product_info": {
        "each": {
            "count": "1 Item",
            "volume": "L 1\" x W 1\" x H 1\"",
            "weight": "30 lbs"
        }
    }
}
temp = float(cheese.get('price').replace('$', '')) if cheese.get('price') else None,
print(temp)
# import_csv_to_vector(f"{FIXTURES}/retail-leases_2025-01-21_014339.csv")
# query_sql("SELECT AVG(CurrentRentPa) AS average_rent FROM retail_leases WHERE CentreName LIKE '%Townsville%';")