import requests
import json

# Data for the new product
product_data = {
    "name": "Té Verde Matcha",
    "description": "Té verde japonés premium en polvo para ceremonias",
    "price": "18.50",
    "category_id": 4,
    "image": "http://127.0.0.1:8000/media/products/te_verde.jpg",
    "stock": 40,
    "available": True
}

# Make the API request to create product
response = requests.post('http://127.0.0.1:8000/api/products/', 
                        json=product_data)

# Print the results
print(f'Product Creation Status Code: {response.status_code}')
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text) 