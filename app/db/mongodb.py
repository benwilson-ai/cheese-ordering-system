from typing import List
from pymongo import MongoClient
from app.core.config import settings
from app.schemas.cheese_data import CheeseData
from typing import Dict, Any, List
class MongoDBService:
    def __init__(self):
        self.client = MongoClient(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            username=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        self.db = self.client[settings.DB_NAME]
        self.collection = self.db.cheese_data

    def initialize(self):
        """Create indexes for the cheese_data collection"""
        self.collection.create_index("id", unique=True)
        self.collection.create_index("sku", unique=True)
        self.collection.create_index("upc", unique=True)

    def insert_cheese(self, cheese: CheeseData):
        """Insert or update a cheese document"""
        cheese_dict = cheese.model_dump(exclude_none=True)
        self.collection.update_one(
            {"id": cheese.id},
            {"$set": cheese_dict},
            upsert=True
        )

    def query(self, query: Dict[str, Any], sort: Dict[str, int] = None) -> List[Dict[str, Any]]:
        """
        Execute a MongoDB query with optional sorting and return the results.

        :param query: MongoDB query to execute.
        :param sort: Sorting criteria as a dictionary (e.g., {"field_name": 1} for ascending).
        :return: List of query results.
        """
        try:
            print(f"Executing query: {query}, with sort: {sort}")
            if sort:
                results = list(self.collection.find(query).sort(list(sort.items())))
            else:
                results = list(self.collection.find(query))
            print(f"Query executed successfully. Found {len(results)} results.")
            return results
        except Exception as e:
            print(f"Error executing MongoDB query: {e}")
            raise


mongodb = MongoDBService()