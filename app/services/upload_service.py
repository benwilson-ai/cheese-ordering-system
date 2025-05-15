import csv
import json
from typing import BinaryIO
from unittest import skipUnless
import chardet
from app.db.vectordb import vector_db
from app.db.mongodb import mongodb
from app.schemas.cheese_data import CheeseData
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def scrape_product_details(product_url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Load the page
        driver.get(product_url)
        
        # Wait for the SKU/UPC div to be present
        wait = WebDriverWait(driver, 10)
        sku_upc_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-ahthbn')))
        
        # Get cheese form
        form_elems = driver.find_elements(By.CLASS_NAME, 'chakra-breadcrumb__link')
        cheese_form = form_elems[1].text.strip() if len(form_elems) > 1 else 'N/A'
        
        # Get SKU and UPC
        b_tags = sku_upc_div.find_elements(By.TAG_NAME, 'b')
        sku = b_tags[0].text.strip() if len(b_tags) > 0 else 'N/A'
        upc = b_tags[1].text.strip().split(',')[0] if len(b_tags) > 1 else 'N/A'
        
        # Get table data
        table_data = {}
        table = sku_upc_div.find_element(By.CLASS_NAME, 'chakra-table')
        if table:
            tbody = table.find_element(By.TAG_NAME, 'tbody')
            rows = tbody.find_elements(By.TAG_NAME, 'tr')
            
            if rows:
                # Get all cells from all rows
                cells = [row.find_elements(By.TAG_NAME, 'td') for row in rows]
                
                # Check if we have both case and each columns
                if len(cells[0]) == 2:
                    table_data = {
                        'case': {
                            'count': cells[0][0].text.strip() if cells[0][0].text.strip() else 'N/A',
                            'volume': cells[1][0].text.strip() if cells[1][0].text.strip() else 'N/A',
                            'weight': cells[2][0].text.strip() if cells[2][0].text.strip() else 'N/A'
                        },
                        'each': {
                            'count': cells[0][1].text.strip() if cells[0][1].text.strip() else 'N/A',
                            'volume': cells[1][1].text.strip() if cells[1][1].text.strip() else 'N/A',
                            'weight': cells[2][1].text.strip() if cells[2][1].text.strip() else 'N/A'
                        }
                    }
                else:
                    # Only each column
                    table_data = {
                        'each': {
                            'count': cells[0][0].text.strip() if cells[0][0].text.strip() else 'N/A',
                            'volume': cells[1][0].text.strip() if cells[1][0].text.strip() else 'N/A',
                            'weight': cells[2][0].text.strip() if cells[2][0].text.strip() else 'N/A'
                        }
                    }
        
        details = {
            'cheese_form': cheese_form,
            'sku': sku,
            'upc': upc,
            'product_info': table_data,
        
        }
        
        # print(f"Scraped results: {details}")
        return details
        
    except Exception as e:
        print(f"Error scraping product details: {e}")
        return {
        }
    finally:
        driver.quit()

def scrape_cheese_department():
    base_url = "https://shop.kimelo.com/department/cheese/3365"
    current_page = 1
    all_cheese_products = []
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        while True:
            url = f"{base_url}?page={current_page}"
            print(f"\nScraping page {current_page}...")
            
            try:
                driver.get(url)
                # Wait for product cards to be present
                wait = WebDriverWait(driver, 10)
                product_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'chakra-card.group.css-5pmr4x')))
                
                cnt = 0
                for card in product_cards:
                    try:
                        # Get product name
                        name_elem = card.find_element(By.CLASS_NAME, 'css-pbtft')

                        # Get image
                        image_elem = card.find_element(By.TAG_NAME, 'img')
                        
                        # Get brand
                        brand_elem = card.find_element(By.CLASS_NAME, 'css-w6ttxb')
                        
                        # Get product URL
                        product_url = card.get_attribute('product_url')
                        
                        product_data = {
                            'cheese_type': name_elem.text.strip() if name_elem else 'N/A',
                            'image_url': image_elem.get_attribute('src') if image_elem else 'N/A',
                            'product_url': product_url if product_url else 'N/A',
                            'brand': brand_elem.text.strip() if brand_elem else 'N/A',    
                        }
                        
                        # Check for bonus text
                        try:
                            bonus_elem = card.find_element(By.CLASS_NAME, 'chakra-text.css-87ralv')
                            if bonus_elem:
                                product_data['bonus'] = bonus_elem.text.strip()
                        except:
                            pass  # No bonus element found, continue without it
                        
                        try:
                            price_elem = card.find_element(By.CLASS_NAME, 'css-1vhzs63')
                            if price_elem:
                                product_data['price'] = price_elem.text.strip()
                        except:
                            pass  # No bonus element found, continue without it
                        
                        try:
                            price_per_lb_elem = card.find_element(By.CLASS_NAME, 'css-ff7g47')
                            if price_per_lb_elem:
                                product_data['price_per_lb'] = price_per_lb_elem.text.strip()
                        except:
                            pass  # No bonus element found, continue without it
                        
                        
                        if product_data['cheese_type'] != 'N/A':
                            # Scrape additional product details
                            if product_url != 'N/A':
                                print(f"Scraping details for {product_data['cheese_type']}...")
                                details = scrape_product_details(product_url)
                                product_data.update(details)
                            print(product_data)
                            all_cheese_products.append(product_data)
                            cnt += 1
                        
                    except Exception as e:
                        print(f"Error processing card on page {current_page}: {e}")
                        continue
                
                print(f"Found {cnt} / {len(product_cards)} product cards on page {current_page}")
                
                # Check if there's a next page
                next_page_link = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Next page"]')
                if not next_page_link or next_page_link[0].get_attribute('disabled'):
                    print("No next page link found or reached last page. Ending pagination.")
                    return all_cheese_products
                    
                current_page += 1
                time.sleep(2)  # Be nice to the server between page requests
                
            except Exception as e:
                print(f"Error processing page {current_page}: {e}")
                break
    
    finally:
        driver.quit()
    
    output_data = {
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_products': len(all_cheese_products),
        'total_pages': current_page - 1,
        'products': all_cheese_products
    }
    
    with open('cheese_products.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    print(f"\nSuccessfully scraped {len(all_cheese_products)} products from {current_page - 1} pages and saved to cheese_products.json")
    return output_data
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
        for cheese in json_data:
            mongodb.insert_cheese(cheese)
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
            mongodb.insert_cheese(cheese)
            vector_db.upsert_cheese(cheese)

    @staticmethod
    def process_auto_update():
        # Read JSON data
        json_data = scrape_cheese_department()
        
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
                each_volume='L 1\" x W 1\" x H 1\"',
                each_weight=each_info.get('weight'),
                sku=int(product.get('sku', 0)),
                upc=int(product.get('upc', 0)),
                image_url=product.get('image_url'),
                product_url=product.get('product_url'),
                wholesale=product.get('bonus', "It has no wholesale price"),
                out_of_stock=product.get('price', "BACK IN STOCK SOON")
            )
            
            # Store in both databases
            mongodb.insert_cheese(cheese)
            vector_db.upsert_cheese(cheese)

upload_service = UploadService()