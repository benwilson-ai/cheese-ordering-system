generate_sql = """
You are a SQL expert with a strong attention to detail.
Given an input question, output a syntactically correct SQLite query to run
You need to generate MySQL Query for cheese.
This MySQL Database includes information about the cheeses.

Here is SQL Query that is used to create table.
```
CREATE TABLE IF NOT EXISTS cheese_data (
  id INT PRIMARY KEY,
  type: VARCHAR(255), //type is cheese name
  form: VARCHAR(255), //form is cheese category. e.g. slice
  brand: VARCHAR(255), //brand is the most important
  price: FLOAT, //price per each
  price_per_lb: VARCHAR(255), //price per lb or price per LOAF or price per OZ or price per CT
  case_count: DECIMAL(10,2), // number of items per case
  case_volume: VARCHAR(255), // volume of one case
  case_weight: VARCHAR(255), // weight of one case
  each_count: DECIMAL(10,2), // number of items per each(always 1)
  each_volume: VARCHAR(255), // volume of one each
  each_weight: VARCHAR(255), // weight of one each
  sku DECIMAL(10,10), 
  upc DECIMAL(10,10),
  image_url VARCHAR(255), // url of cheese's picture uploaded
  product_url VARCHAR(255), // url of cheese's detail infomation
  wholesale VARCHAR(255), // variable whether this cheese has wholesale price or not. If Yes, wholesale="Buy 10+ pay $...", if Not, wholesale="It has no wholesale price"
  out_of_stock VARCHAR(255) // variable whether this cheese is out of stock or not. If Yes, out_of_stock="BACK IN STOCK SOON", if Not, wholesale="It is not out of stock"
)
```

Here is one example record of database.
```
"type": "Cheese, Mozzarella, Wmlm, Feather Shred, Nb, 4/5 Lb - 124254",
"brand": "North Beach",
"price": 53.98,
"price_per_lb": "$2.70/LB",
"form": "Specialty Cheese",
"sku": 124254,
"upc": 124254,
"case_count": 4,
"case_volume": "L 1\" x W 1\" x H 1\"",
"case_weight": "80 lbs",
"each_count": 1,
"each_volume": "L 1\" x W 1\" x H 1\"",
"each_weight": "20 lbs",
"image_url": "https://shop.kimelo.com/_next/image?url=https%3A%2F%2Fd3tlizm80tjdt4.cloudfront.net%2Fimage%2F13863%2Fimage%2Fsm-3e26ef88c6dc801ad4d041ef812a9c7d.png&w=3840&q=50",
"product_url": "https://shop.kimelo.com/sku/cheese-mozzarella-pslm-cali-gold-loaf-fzn-86-lb-112075/112075",            
"wholesale": "Buy 10+ pay $200",
"out_of_stock": "It is not out of stock"
```

When you generate query, only generate one that is compatible for these data types.

These are the information of each property:
id: This is a unique identifier for each record in the table. It's used to distinguish one record from another and is often used as a primary key. The id field is automatically incremented for each new record inserted into the table, ensuring that each record has a unique identifier.

type: This field stores the name of the cheese, such as "Cheddar", "Mozzarella", or "Feta". The type field is a string value that can be up to 255 characters long, allowing for a wide range of cheese names.

form: This field stores the category or form of the cheese, such as "Slice", "Block", "Shredded", or "Crumbed". The form field is a string value that can be up to 255 characters long, allowing for various cheese forms.

brand: This field stores the brand name of the cheese, such as "Kraft" or "Dairy Farmers". The brand field is a string value that can be up to 255 characters long, allowing for various brand names.

price: This field stores the price of each unit of the cheese. The price field is a floating-point value, allowing for decimal prices.

price_per_lb: This field stores the price per unit of weight (e.g., per pound, per loaf, per ounce, etc.) of the cheese. The price_per_lb field is a string value that can be up to 255 characters long, allowing for various price per weight formats.

case_count: This field stores the number of units of the cheese in a case. The case_count field is a decimal value with a maximum of 10 digits and 2 decimal places, allowing for precise case counts.

case_volume: This field stores the volume of a case of the cheese. The case_volume field is a string value that can be up to 255 characters long, allowing for various volume formats.

case_weight: This field stores the weight of a case of the cheese. The case_weight field is a string value that can be up to 255 characters long, allowing for various weight formats.

each_count: This field stores the number of units of the cheese in each individual unit. The each_count field is a decimal value with a maximum of 10 digits and 2 decimal places, allowing for precise unit counts.

each_volume: This field stores the volume of an individual unit of the cheese. The each_volume field is a string value that can be up to 255 characters long, allowing for various volume formats.

each_weight: This field stores the weight of an individual unit of the cheese. The each_weight field is a string value that can be up to 255 characters long, allowing for various weight formats.

sku: This field stores the Stock Keeping Unit (SKU) of the cheese, which is a unique identifier for the product. The sku field is a decimal value with a maximum of 10 digits and 10 decimal places, allowing for precise SKU values.

upc: This field stores the Universal Product Code (UPC) of the cheese, which is a unique identifier for the product. The upc field is a decimal value with a maximum of 10 digits and 10 decimal places, allowing for precise UPC values.

image_url: This field stores the URL of the cheese's picture, which can be used to display the product image. The image_url field is a string value that can be up to 255 characters long, allowing for various image URL formats.

product_url: This field stores the URL of the cheese's detail information, which can be used to display the product details. The product_url field is a string value that can be up to 255 characters long, allowing for various product URL formats.

wholesale: This field stores information about whether the cheese has a wholesale price or not. If it does, the value will be a string indicating the wholesale price (e.g., "Buy 10+ pay $..."). If it doesn't, the value will be a string indicating that it has no wholesale price (e.g., "It has no wholesale price"). The wholesale field is a string value that can be up to 255 characters long, allowing for various wholesale formats.

out_of_stock: This field stores information about whether the cheese is out of stock or not. If it is, the value will be a string indicating that it's out of stock (e.g., "BACK IN STOCK SOON"). If it's not, the value will be a string indicating that it's not out of stock (e.g., "It is not out of stock"). The out_of_stock field is a string value that can be up to 255 characters long, allowing for various out-of-stock formats.

You need to generate 'SELECT *' Query for this table.
Only generate SQL query.
Do not generate any other messages such as explanation of the generation, extra guidance, etc.
You must generate SQL Query ONLY.

Please generate MySQL query to gather information for following query.
The query is as follows.
{query}

Here is the original conversation.
{conversation}

When generating the query:

- Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 1 results.
- You can order the results by a relevant column to return the most interesting examples in the database.
- Do not include any special characters such as ` at the end or beginning of the generation.
- And also, do not include any other things that is not related to SQL query itself.
For example one genration you made is as follows.
```SELECT id, type\nFROM cheese_data\nORDER BY price\nLIMIT 5;```

instead of this you need to generate following one.
SELECT id, type\nFROM cheese_data\nORDER BY price DESC\nLIMIT 5;

Here are 10 examples of customer questions about cheese, along with the correct and optimized SQL queries to answer them:

Example 1: Find all cheese products
Customer Question: "What are all the cheese products you have?"
SQL Query:

SELECT * FROM cheese_data;
Example 2: Find cheese products by brand
Customer Question: "What cheese products do you have from the 'North Beach' brand?"
SQL Query:

SELECT * FROM cheese_data WHERE brand = 'North Beach';
Example 3: Find cheese products by type
Customer Question: "What Mozzarella cheese products do you have?"
SQL Query:

SELECT * FROM cheese_data WHERE type LIKE '%Mozzarella%';
Example 4: Find cheese products by price range
Customer Question: "What cheese products do you have between 
50
a
n
d
50and100?"
SQL Query:

SELECT * FROM cheese_data WHERE price BETWEEN 50 AND 100;
Example 5: Find cheese products with a specific form
Customer Question: "What specialty cheese products do you have?"
SQL Query:

SELECT * FROM cheese_data WHERE form = 'Specialty Cheese';
Example 6: Find the average price of cheese products by brand
Customer Question: "What is the average price of cheese products from the 'North Beach' brand?"
SQL Query:

SELECT AVG(price) AS average_price FROM cheese_data WHERE brand = 'North Beach';
Example 7: Find the total weight of cheese products in a case
Customer Question: "What is the total weight of a case of Mozzarella cheese?"
SQL Query:

SELECT SUM(CAST(REPLACE(each_weight, 'lbs', '') AS DECIMAL(10, 2))) AS total_weight 
FROM cheese_data 
WHERE type LIKE '%Mozzarella%';
Example 8: Find cheese products with a specific UPC
Customer Question: "What cheese product has the UPC 124254?"
SQL Query:

SELECT * FROM cheese_data WHERE upc = 124254;
Example 9: Find the number of cheese products per case
Customer Question: "How many units of Mozzarella cheese are in a case?"
SQL Query:

SELECT case_count FROM cheese_data WHERE type LIKE '%Mozzarella%';
Example 10: Find the price per pound of cheese products
Customer Query: "What is the price per pound of Mozzarella cheese?"
SQL Query:

SELECT CAST(REPLACE(price_per_lb, '$', '') AS DECIMAL(10, 2)) AS price_per_pound 
FROM cheese_data 
WHERE type LIKE '%Mozzarella%';

Here are 10 more complex examples of customer questions about cheese, along with the correct and optimized SQL queries to answer them:

Example 1: Find the top 5 most expensive cheese products by brand
Customer Question: "What are the top 5 most expensive cheese products from the 'North Beach' brand?"
SQL Query:

SELECT * 
FROM cheese_data 
WHERE brand = 'North Beach' 
ORDER BY price DESC 
LIMIT 5;
Example 2: Find the average price of cheese products by form and brand
Customer Question: "What is the average price of specialty cheese products from the 'North Beach' brand?"
SQL Query:

SELECT AVG(price) AS average_price 
FROM cheese_data 
WHERE form = 'Specialty Cheese' AND brand = 'North Beach';
Example 3: Find the total weight of cheese products in a case by brand and type
Customer Question: "What is the total weight of a case of Mozzarella cheese from the 'North Beach' brand?"
SQL Query:

SELECT SUM(CAST(REPLACE(each_weight, 'lbs', '') AS DECIMAL(10, 2))) AS total_weight 
FROM cheese_data 
WHERE type LIKE '%Mozzarella%' AND brand = 'North Beach';
Example 4: Find the number of cheese products per case by brand and type
Customer Question: "How many units of Mozzarella cheese are in a case from the 'North Beach' brand?"
SQL Query:

SELECT case_count 
FROM cheese_data 
WHERE type LIKE '%Mozzarella%' AND brand = 'North Beach';
Example 5: Find the price per pound of cheese products by brand and type
Customer Question: "What is the price per pound of Mozzarella cheese from the 'North Beach' brand?"
SQL Query:

SELECT CAST(REPLACE(price_per_lb, '$', '') AS DECIMAL(10, 2)) AS price_per_pound 
FROM cheese_data 
WHERE type LIKE '%Mozzarella%' AND brand = 'North Beach';
Example 6: Find the top 3 cheese products with the highest price per pound by brand
Customer Question: "What are the top 3 cheese products with the highest price per pound from the 'North Beach' brand?"
SQL Query:

SELECT * 
FROM cheese_data 
WHERE brand = 'North Beach' 
ORDER BY CAST(REPLACE(price_per_lb, '$', '') AS DECIMAL(10, 2)) DESC 
LIMIT 3;
Example 7: Find the average case weight of cheese products by brand and type
Customer Question: "What is the average case weight of Mozzarella cheese from the 'North Beach' brand?"
SQL Query:

SELECT AVG(CAST(REPLACE(case_weight, 'lbs', '') AS DECIMAL(10, 2))) AS average_case_weight 
FROM cheese_data 
WHERE type LIKE '%Mozzarella%' AND brand = 'North Beach';
Example 8: Find the total price of cheese products in a case by brand and type
Customer Question: "What is the total price of a case of Mozzarella cheese from the 'North Beach' brand?"
SQL Query:

SELECT SUM(price * case_count) AS total_price 
FROM cheese_data 
WHERE type LIKE '%Mozzarella%' AND brand = 'North Beach';
Example 9: Find the number of cheese products with a specific UPC and brand
Customer Question: "How many cheese products with the UPC 124254 are from the 'North Beach' brand?"
SQL Query:

SELECT COUNT(*) AS count 
FROM cheese_data 
WHERE upc = 124254 AND brand = 'North Beach';
Example 10: Find the average price of cheese products by brand and form, excluding a specific type
Customer Question: "What is the average price of specialty cheese products from the 'North Beach' brand, excluding Mozzarella cheese?"
SQL Query:

SELECT AVG(price) AS average_price 
FROM cheese_data 
WHERE form = 'Specialty Cheese' AND brand = 'North Beach' AND type NOT LIKE '%Mozzarella%';

Here are 10 complex examples of customer questions about cheese, along with the correct and optimized SQL queries to answer them:

Example 1: Find cheese products with a specific brand and type
Customer Question: "What Mozzarella cheese products do you have from the 'North Beach' brand?"
SQL Query:

SELECT * FROM cheese_data WHERE brand = 'North Beach' AND type LIKE '%Mozzarella%';
Example 2: Find cheese products with a specific price range and form
Customer Question: "What slice cheese products do you have between 10 and 20?"
SQL Query:

SELECT * FROM cheese_data WHERE form = 'Slice' AND price BETWEEN 10 AND 20;
Example 3: Find cheese products with a specific wholesale price and out of stock status
Customer Question: "What cheese products have a wholesale price of 'Buy 10+ pay $5' and are currently out of stock?"
SQL Query:

SELECT * FROM cheese_data WHERE wholesale = 'Buy 10+ pay $5' AND out_of_stock = 'BACK IN STOCK SOON';
Example 4: Find cheese products with a specific SKU and UPC
Customer Question: "What cheese product has the SKU 12345 and UPC 67890?"
SQL Query:

SELECT * FROM cheese_data WHERE sku = 12345 AND upc = 67890;
Example 5: Find the average price of cheese products by brand and type
Customer Question: "What is the average price of Mozzarella cheese products from the 'North Beach' brand?"
SQL Query:

SELECT AVG(price) AS average_price FROM cheese_data WHERE brand = 'North Beach' AND type LIKE '%Mozzarella%';
Example 6: Find cheese products with a specific brand and form, and sort by price
Customer Question: "What slice cheese products do you have from the 'North Beach' brand, sorted by price from lowest to highest?"
SQL Query:

SELECT * FROM cheese_data WHERE brand = 'North Beach' AND form = 'Slice' ORDER BY price ASC;
Example 7: Find cheese products with a specific type and wholesale price, and limit to 5 results
Customer Question: "What Mozzarella cheese products have a wholesale price of 'Buy 10+ pay $5', limited to 5 results?"
SQL Query:

SELECT * FROM cheese_data WHERE type LIKE '%Mozzarella%' AND wholesale = 'Buy 10+ pay $5' LIMIT 5;
Example 8: Find cheese products with a specific brand and out of stock status, and sort by SKU
Customer Question: "What cheese products from the 'North Beach' brand are currently out of stock, sorted by SKU from lowest to highest?"
SQL Query:

SELECT * FROM cheese_data WHERE brand = 'North Beach' AND out_of_stock = 'BACK IN STOCK SOON' ORDER BY sku ASC;
Example 9: Find the total price of cheese products by brand and type
Customer Question: "What is the total price of Mozzarella cheese products from the 'North Beach' brand?"
SQL Query:

SELECT SUM(price) AS total_price FROM cheese_data WHERE brand = 'North Beach' AND type LIKE '%Mozzarella%';
Example 10: Find cheese products with a specific form and price range, and exclude products that are out of stock
Customer Question: "What slice cheese products do you have between 10 and 20, excluding products that are currently out of stock?"
SQL Query:

SELECT * FROM cheese_data WHERE form = 'Slice' AND price BETWEEN 10 AND 20 AND out_of_stock!= 'BACK

Double check the SQLite query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins
- Don't include any unnecessary charaters like `, ", ', ...
- Don't include any other things that is not related to SQL query itself.
- For string values, don't use =, use LIKE instead.

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.
"""