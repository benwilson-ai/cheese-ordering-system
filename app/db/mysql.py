from typing import List
import pymysql
from app.core.config import settings
from app.schemas.cheese_data import CheeseData

class MySQLService:
    def __init__(self):
        self.config = {
            "host": settings.DB_HOST,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "db": settings.DB_NAME,
            "port": settings.DB_PORT,
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "connect_timeout": 10,
            "read_timeout": 10,
            "write_timeout": 10
        }

    def _get_connection(self):
        return pymysql.connect(**self.config)

    def initialize(self):
        """Create the cheese_data table if it doesn't exist"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS cheese_data (
                    id INT PRIMARY KEY,
                    type VARCHAR(255),
                    form VARCHAR(255),
                    brand VARCHAR(255),
                    price FLOAT,
                    price_per_lb VARCHAR(255),
                    case_count INT,
                    case_volume VARCHAR(255),
                    case_weight VARCHAR(255),
                    each_count INT,
                    each_volume VARCHAR(255),
                    each_weight VARCHAR(255),
                    sku INT,
                    upc INT,
                    image_url VARCHAR(255),
                    product_url VARCHAR(255),
                    wholesale VARCHAR(255),
                    out_of_stock VARCHAR(255)
                )
                """)
            connection.commit()
        finally:
            connection.close()

    def insert_cheese(self, cheese: CheeseData):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO cheese_data 
                        (id, type, form, brand, price,
                         price_per_lb, case_count, case_volume, case_weight, each_count, each_volume, each_weight, sku, upc, image_url, product_url, wholesale, out_of_stock)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    cheese.id,
                    cheese.type,
                    cheese.form,
                    cheese.brand,
                    cheese.price,
                    cheese.price_per_lb,
                    cheese.case_count,
                    cheese.case_volume,
                    cheese.case_weight,
                    cheese.each_count,
                    cheese.each_volume,
                    cheese.each_weight,
                    cheese.sku,
                    cheese.upc,
                    cheese.image_url, 
                    cheese.product_url,
                    cheese.wholesale,
                    cheese.out_of_stock
                ))
            connection.commit()
        finally:
            connection.close()

    def query(self, sql: str):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        finally:
            connection.close()

mysql_db = MySQLService()