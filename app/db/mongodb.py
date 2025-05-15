import json
from typing import List
from pymongo import MongoClient
from app.core.config import settings
from app.schemas.cheese_data import CheeseData
from typing import Dict, Any, List
class MongoDBService:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://tannergregg38:b52vQT282LvpXw1H@cluster0.pwnh0r4.mongodb.net/"
        )
        self.db = self.client["auto-food-order"]
        self.collection = self.db["cheese"]

    def initialize(self):
        """Create indexes for the cheese_data collection"""
        self.collection.create_index("_id", unique=True)
        self.collection.create_index("sku", unique=True)

    def insert_cheese(self, cheese):
        """Insert or update a cheese document"""
        # cheese_dict = cheese.model_dump(exclude_none=True)
        self.collection.insert_one(
            cheese
        )
    
    def query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute a MongoDB query with optional sorting and return the results.

        :param query: MongoDB query to execute.
        :param sort: Sorting criteria as a dictionary (e.g., {"field_name": 1} for ascending).
        :return: List of query results.
        """
        try:
            
            results = list(self.collection.aggregate(json.loads(query)))
            print(f"Query executed successfully. Found {len(results)} results.")
            return results
        except Exception as e:
            print(f"Error executing MongoDB query: {e}")
            raise


mongodb = MongoDBService()