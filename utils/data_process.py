def calculate_total_revenue(transactions):
    total_revenue = 0
    for t in transactions:
        row_value = t['Quantity']*t['UnitPrice']
        total_revenue += row_value
    return total_revenue

def region_wise_sales(transactions):
    #initializing variables
    total_sales = 0
    transaction_count = 0
    percentage  = 0
    grouped = {}
    total_sales_all = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    
    for t in transactions:
        region = t['Region']
        if not region:  # Skip transactions with empty region
            continue
        if region not in grouped:
            grouped[region] = []
        grouped[region].append(t)
    region_grouped = {}
    
    for region, trans in grouped.items():
        total_sales = sum(t['Quantity'] * t['UnitPrice'] for t in trans)
        transaction_count = len(trans)
        percentage = (total_sales/total_sales_all)*100 
        region_grouped[region] = {
            'total_sales': total_sales,
            'transaction_count': transaction_count,
            'percentage': round(percentage, 2)
        }
    region_grouped = dict(sorted(region_grouped.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    return region_grouped
        
    
def top_selling_products(transactions, n = 5):

    grouped = {}

    for t in transactions:
        ProductName = t['ProductName']
        if not ProductName:
            continue
        if ProductName not in grouped:
            grouped[ProductName] = []
        grouped[ProductName].append(t)
    Product_grouped = []
    for ProductName , trans in grouped.items():
        Total_Quantity = sum(t['Quantity'] for t in trans)
        Total_revenue = sum(t['Quantity']*t['UnitPrice'] for t in trans)
        Product_grouped.append((ProductName,Total_Quantity,Total_revenue))
    
    # sort by quantity desc
    Product_grouped.sort(key=lambda x: x[1], reverse=True)

    # return top N
    return Product_grouped[:n]

def customer_analysis(transactions):
    grouped = {}

    for t in transactions:
        customer_id = t['CustomerID']
        if not customer_id:
            continue
        if customer_id not in grouped:
            grouped[customer_id] = []
        grouped[customer_id].append(t)
    customer_grouped = {}
   
    for customer_id,trans in grouped.items():
        Total_spent = sum(t['Quantity']*t['UnitPrice'] for t in trans)
        purchase_count = len(trans)
        Avg_order_value = round(Total_spent/purchase_count, 2)
        products_bought = list({t['ProductName'] for t in trans})
        customer_grouped[customer_id] = {'total_spent':Total_spent,'purchase_count':purchase_count,'avg_order_value':Avg_order_value,
                                         'products_bought':products_bought}
    customer_grouped_sorted = dict(sorted(customer_grouped.items(), key=lambda x: x[1]['total_spent'],reverse= True))
    return customer_grouped_sorted

def daily_sales_trend(transactions):
    grouped = {}
    for t in transactions:
        Date = t['Date']
        if not Date:
            continue
        if Date not in grouped:
            grouped[Date] = []
        grouped[Date].append(t)
    Date_grouped = {}
    for date,trans in grouped.items():
        revenue = sum(t['Quantity']*t['UnitPrice'] for t in trans)
        transaction_count = len(trans)
        unique_customers = len({t['CustomerID'] for t in trans})
        Date_grouped[date] = {'revenue':revenue,'transaction_count':transaction_count,'unique_customers':unique_customers}
    Date_grouped_sorted = dict(sorted(Date_grouped.items(), key=lambda x: x[0]))
    return Date_grouped_sorted

def find_peak_sales_day(transactions):
    revenue = 0
    transaction_count = 0
    grouped = {}

    for d in transactions:
        Date = d['Date']
        if not Date:
            continue
        if Date not in grouped:
            grouped[Date] = []
        grouped[Date].append(d)
    date_grouped = []
    for Date,trans in grouped.items():
        revenue = sum(t['UnitPrice']*t['Quantity'] for t in trans)
        transaction_count = len(trans)
        date_grouped.append((Date,revenue,transaction_count))
    date_grouped.sort(key = lambda x: x[1], reverse = True)
    return date_grouped[0]
    
def low_performing_products(transactions, threshold=10):
    grouped = {}
    for t in transactions:
        products = t['ProductName']
        if not products:
            continue
        if products not in grouped:
            grouped[products] = []
        grouped[products].append(t)
    product_grouped = []
    for products, trans in grouped.items():
        TotalQuantity = sum(t['Quantity'] for t in trans)
        revenue = sum(t['Quantity']*t['UnitPrice'] for t in trans)
        if TotalQuantity < threshold:
            product_grouped.append((products,TotalQuantity,revenue))
    product_grouped.sort(key = lambda x: x[1], reverse = False)
    return product_grouped
