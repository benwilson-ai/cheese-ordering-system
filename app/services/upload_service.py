import csv
import json
from typing import BinaryIO
from unittest import skipUnless
import chardet
from app.db.vectordb import vector_db
from app.db.mysql import mysql_db
from app.schemas.cheese_data import CheeseData
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
    def process_json(file: BinaryIO):
        # Read JSON data
        json_data = json.load(file)
        
        # Process each product in the JSON
        for idx, product in enumerate(json_data['products']):
            # Extract product info
            product_info = product.get('product_info', {})
            case_info = product_info.get('case', {})
            each_info = product_info.get('each', {})
            # Create CheeseData object
            cheese = CheeseData(
                id=idx + 1,  # Generate sequential IDs
                type=product.get('cheese_type'),
                form=product.get('cheese_form'),
                brand=product.get('brand'),
                price=float(product.get('price').replace('$', '')) if product.get('price') else None,
                price_per_lb=product.get('price_per_lb', None),
                case_count=float(case_info.get('count', '0').split()[0]) if case_info.get('count') else None,
                case_volume=case_info.get('volume', None),
                case_weight=case_info.get('weight', None),
                each_count=float(each_info.get('count', '0').split()[0]) if each_info.get('count') else None,
                # each_volume=each_info.get('volume'),
                each_volume='L 1\" x W 1\" x H 1\"',
                each_weight=each_info.get('weight'),
                sku=int(product.get('sku', 0)),
                upc=int(product.get('upc', 0)),
                image_url=product.get('image_url'),
                product_url=product.get('product_url'),
                wholesale=product.get('bonus', "It has no wholesale price"),  # Default value
                out_of_stock=product.get('price', "It is not out of stock")   # Default value
            )
            
            # Store in both databases
            mysql_db.insert_cheese(cheese)
            print("We are Here")
            vector_db.upsert_cheese(cheese)

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
            print(row)
            cheese = CheeseData(
                id=int(row[0]),
                type = str(row[1]),
                brand = str(row[2]),
                price = int(row[3]),
                price_per_lb = str(row[4]),
                form = str(row[5]),
                case_count = int(row[6]),
                case_volume = str(row[7]),
                case_weight = str(row[8]),
                each_count = int(row[9]),
                each_volume = str(row[10]),
                each_weight = str(row[11]),
                sku = int(row[12]),
                upc = int(row[13]),
                image_url = str(row[14]),
                product_url = str(row[15]),
                wholesale = str(row[16]),
                out_of_stock = str(row[17]),
            )
            
            # Store in both databases
            mysql_db.insert_cheese(cheese)
            vector_db.upsert_cheese(cheese)

upload_service = UploadService()