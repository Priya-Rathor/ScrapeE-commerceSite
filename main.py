import requests
import json
import csv
import time
from datetime import datetime

class EcommerceScraper:
    def __init__(self, base_url="https://fakestoreapi.com"):
        self.base_url = base_url
        self.products_data = []
        self.categories_data = []
        
    def fetch_categories(self):
        """Fetch all product categories"""
        try:
            response = requests.get(f"{self.base_url}/products/categories")
            response.raise_for_status()
            self.categories_data = response.json()
            print(f"✓ Fetched {len(self.categories_data)} categories")
            return self.categories_data
        except requests.RequestException as e:
            print(f"✗ Error fetching categories: {e}")
            return []
    
    def fetch_products(self, limit=None):
        """Fetch all products or limited number"""
        try:
            url = f"{self.base_url}/products"
            if limit:
                url += f"?limit={limit}"
            
            response = requests.get(url)
            response.raise_for_status()
            self.products_data = response.json()
            print(f"✓ Fetched {len(self.products_data)} products")
            return self.products_data
        except requests.RequestException as e:
            print(f"✗ Error fetching products: {e}")
            return []
    
    def fetch_product_by_category(self, category):
        """Fetch products by specific category"""
        try:
            response = requests.get(f"{self.base_url}/products/category/{category}")
            response.raise_for_status()
            category_products = response.json()
            print(f"✓ Fetched {len(category_products)} products from {category}")
            return category_products
        except requests.RequestException as e:
            print(f"✗ Error fetching products for category {category}: {e}")
            return []
    
    def process_product_data(self, product):
        """Process and clean product data"""
        return {
            'id': product.get('id', ''),
            'title': product.get('title', ''),
            'price': product.get('price', 0),
            'description': product.get('description', ''),
            'category': product.get('category', ''),
            'image': product.get('image', ''),
            'rating_rate': product.get('rating', {}).get('rate', 0),
            'rating_count': product.get('rating', {}).get('count', 0),
            'scraped_at': datetime.now().isoformat()
        }
    
    def save_to_csv(self, filename='products_data.csv'):
        """Save products data to CSV file"""
        if not self.products_data:
            print("No products data to save")
            return
        
        processed_data = [self.process_product_data(product) for product in self.products_data]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'price', 'description', 'category', 
                         'image', 'rating_rate', 'rating_count', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(processed_data)
        
        print(f"✓ Saved {len(processed_data)} products to {filename}")
    
    def save_to_json(self, filename='ecommerce_data.json'):
        """Save all data to JSON file"""
        complete_data = {
            'metadata': {
                'source': self.base_url,
                'scraped_at': datetime.now().isoformat(),
                'total_products': len(self.products_data),
                'total_categories': len(self.categories_data)
            },
            'categories': self.categories_data,
            'products': [self.process_product_data(product) for product in self.products_data]
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(complete_data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved complete data to {filename}")
    
    def scrape_all_data(self):
        """Main method to scrape all required data"""
        print("🚀 Starting e-commerce data scraping...")
        print("-" * 50)
        
        # Fetch categories
        self.fetch_categories()
        time.sleep(0.5)  # Be respectful to the API
        
        # Fetch all products
        self.fetch_products()
        time.sleep(0.5)
        
        # Save data in both formats
        self.save_to_csv()
        self.save_to_json()
        
        print("-" * 50)
        print("✅ Scraping completed successfully!")
        
        return {
            'categories': self.categories_data,
            'products': self.products_data
        }

# Example usage
if __name__ == "__main__":
    # Initialize scraper
    scraper = EcommerceScraper()
    
    # Scrape all data
    data = scraper.scrape_all_data()
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"Categories: {len(data['categories'])}")
    print(f"Products: {len(data['products'])}")
    print(f"Files created: products_data.csv, ecommerce_data.json")