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
    
    def query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a MongoDB query and return the results.

        :param query: MongoDB query as a string. Should be a valid JSON string with double quotes.
        :return: List of query results.
        """
        try:
            # First, try to parse the query as JSON to validate it
            query_obj = json.loads(query)
            
            # Execute the aggregation pipeline
            results = list(self.collection.aggregate(query_obj))
            print(f"Query executed successfully. Found {len(results)} results.")
            return results
        except json.JSONDecodeError as e:
            print(f"Invalid JSON query format: {e}")
            raise
        except Exception as e:
            print(f"Error executing MongoDB query: {e}")
            raise


mongodb = MongoDBService()