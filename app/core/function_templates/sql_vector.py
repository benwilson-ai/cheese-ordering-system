import json

function_list = [
    {
        "type": "function",
        "function": {
            "name": "determine_is_available",
            "description": "This function is using conversation between user and assistant as input and determine whether user is asking about cheese or not",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_available": {
                        "type": "string",
                        "enum": ["yes", "no", "unknown"],
                        "description": "If user is asking about cheese you have this property returns 'yes', and if user is not asking about cheese or asking about contents not related to all contents recorded to DB or insulting you is good return 'no', and if information is not provided, return 'unknown'"
                    }
                },
                "required": ["is_available"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "determine_sql_or_vector",
            "description": "This function is using conversation between user and assistant as input and determine whether using sql is good or using vectordb is good",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_sql": {
                        "type": "string",
                        "enum": ["yes", "no", "unknown"],
                        "description": "Every questions asking about cheese is about your cheese recorded in Sql database. If user's question is about cheese, especially type, form, brand, price, price per each, price per lb, case count, size, volume, case and each weight and sku, upc wholesale(Buy 10+ with ...$) back in stock again, You must this property returns 'yes'. If using SQL is good this property returns 'yes', and if using vectordb is good return 'no', and if information is not provided, return 'unknown'"
                    }
                },
                "required": ["is_sql"]
            }
        }
    }
]

sql_vector_tool = json.loads(json.dumps(function_list))