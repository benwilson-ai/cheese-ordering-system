import json

function_list = {
        "type": "function",
        "function": {
            "name": "determine_selected",
            "description": "This function is using conversation between user and assistant as input and determine whether using mongoDB is good or using vectordb is good",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_mongo": {
                        "type": "string",
                        "enum": ["yes", "no", "unknown"],
                        "description": "Every questions asking about cheese is about your cheese recorded in mongoDB. If user's question is about cheese, especially type, form, brand, price, price per each, price per lb, case count, size, volume, case and each weight and sku, upc wholesale(Buy 10+ with ...$) back in stock again, You must this property returns 'yes'. If using mongoDB is good this property returns 'yes'"
                    }
                },
                "required": ["is_mongo"]
            }
        }
}

determine_selected = json.loads(json.dumps(function_list))