from typing import List
import pymysql
from app.core.config import settings
from app.schemas.retail_lease import RetailLease

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
        """Create the retail_leases table if it doesn't exist"""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS retail_leases (
                    id INT PRIMARY KEY,
                    start_date DATE,
                    expiry_date DATE,
                    current_rent_pa DECIMAL(10,2),
                    current_rent_sqm DECIMAL(10,2),
                    centre_name VARCHAR(255),
                    tenant_category VARCHAR(255),
                    tenant_subcategory VARCHAR(255),
                    lessor VARCHAR(255),
                    lessee VARCHAR(255),
                    area DECIMAL(10,2)
                )
                """)
            connection.commit()
        finally:
            connection.close()

    def insert_lease(self, lease: RetailLease):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO retail_leases 
                        (id, start_date, expiry_date, current_rent_pa, current_rent_sqm,
                         centre_name, tenant_category, tenant_subcategory, lessor, lessee, area)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    lease.id,
                    lease.start_date,
                    lease.expiry_date,
                    lease.current_rent_pa,
                    lease.current_rent_sqm,
                    lease.centre_name,
                    lease.tenant_category,
                    lease.tenant_subcategory,
                    lease.lessor,
                    lease.lessee,
                    lease.area
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