import requests
def fetch_all_products(products):
    products = 'https://dummyjson.com/products?limit=100'
    # send to get request
    try:
        response = requests.get(products)
        
        if response.status_code==200:
            print("Products fetched successfully")
            data_dict = response.json()
            return data_dict.get("products", [])
        else:
            print(f"Failed to fetch products. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print("API connection failed:", e)
        return []
    
def create_product_mapping(api_product):
    mapping = {}
    for product in api_product:
        p_id = product['id']
        if p_id is not None:
            mapping[p_id]={"title":product.get('title'),
                       'category':product.get('category'),
                       'brand':product.get('brand'),
                       'rating':product.get('rating')}
    return mapping

def enrich_sales_data(transactions,product_mapping):
    mapped_transaction = []
    for t in transactions:
        try:
            num_string = t['ProductID'].replace("P", "")
            P_id = int(num_string)
        except (ValueError, TypeError):
            P_id = None
        if P_id not in product_mapping:
            t['API_Category'] = None
            t['API_Brand'] = None
            t['API_rating'] = None
            t['API_match'] = False
            mapped_transaction.append(t)
        else:
            P_info = product_mapping[P_id]
            t['API_Category'] = P_info.get('category')
            t['API_Brand'] = P_info.get('brand')
            t['API_rating'] = P_info.get('rating')
            t['API_match'] = True
            mapped_transaction.append(t)
    # Define the header based on the keys in the first transaction
    if mapped_transaction:
        header = list(mapped_transaction[0].keys())
        
        with open('data/enriched_sales_data.txt', 'w') as f:
            # Write the header row
            f.write("|".join(header) + "\n")
            
            # Write each data row
            for row in mapped_transaction:
                # Convert all values to strings so they can be joined
                line = "|".join(str(row.get(column, "")) for column in header)
                f.write(line + "\n")
    return mapped_transaction
