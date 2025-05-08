import csv
from typing import BinaryIO
import chardet
from app.db.vectordb import vector_db
from app.db.mysql import mysql_db
from app.schemas.retail_lease import RetailLease
from datetime import datetime

class UploadService:
    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            try:
                return datetime.strptime(date_str, '%m/%d/%Y')
            except ValueError:
                return datetime.strptime(date_str, '%Y-%m-%d')

    @staticmethod
    def process_csv(file: BinaryIO):
        # Detect encoding
        raw_data = file.read()
        file.seek(0)  # Reset file pointer
        encoding = chardet.detect(raw_data)['encoding']

        # Read CSV
        csv_data = csv.reader(file.read().decode(encoding).splitlines())
        next(csv_data)  # Skip header

        for row in csv_data:
            lease = RetailLease(
                id=int(row[2]),
                start_date=UploadService._parse_date(row[6]),
                expiry_date=UploadService._parse_date(row[7]),
                current_rent_pa=float(row[25]),
                current_rent_sqm=float(row[26]),
                centre_name=row[12],
                tenant_category=row[32],
                tenant_subcategory=row[33],
                lessor=row[20],
                lessee=row[21],
                area=float(row[17])
            )
            
            # Store in both databases
            mysql_db.insert_lease(lease)
            vector_db.upsert_lease(lease)

upload_service = UploadService()