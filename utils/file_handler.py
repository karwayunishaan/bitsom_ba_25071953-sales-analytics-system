import os
def read_sales_data(filename):
    encodings = ['utf-8','latin-1','cp1252']
    for encoding in encodings:
        print(f"Trying to read the file with encoding: {encoding}")
        try:
            with open(filename,'r', encoding=encoding) as file:
                
                #read Lines from the file
                lines = file.readlines()
                cleaned_data = [line.strip() for line in lines[1:] if line.strip()]
                return cleaned_data
        except FileNotFoundError:
            return f"Error: The file '{filename}' was not found."
        except UnicodeDecodeError:
            # If this encoding fails, the loop continues to the next one
            continue
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return "Error: Could not decode the file using available encodings."

def parse_transactions(raw_lines):
    headers =  ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    parse_list = []
    for row in raw_lines:
        values = row.split('|')
        if len(values) != len(headers):
            continue
        try:
            prod_name = values[3].replace(",", "")
            qty = int(values[4].replace(",", ""))
            UP = float(values[5].replace(",", ""))

            entry = {'TransactionID': values[0],
                'Date': values[1],
                'ProductID': values[2],
                'ProductName': prod_name,
                'Quantity': qty,
                'UnitPrice': UP,
                'CustomerID': values[6],
                'Region': values[7]
            }
            
            parse_list.append(entry)
        except ValueError:
            # Skip the row if Quantity or Price isn't a valid number
            continue
        
    return parse_list

def validate_and_filter(transactions, region, min_amount, max_amount):
    # Initialize our counters and lists
    valid_transactions = []
    invalid_count = 0
    region_filtered_count = 0
    amount_filtered_count = 0
    
    # Pre-filter steps (Requirements: Filter Display)
    all_regions = set(t['Region'] for t in transactions if t['Region'])
    print(f"Available regions: {', '.join(all_regions)}")
    
    all_amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    print(f"Transaction amount range: Min ${min(all_amounts):.2f}, Max ${max(all_amounts):.2f}")

    for t in transactions:
        # 1. Validation Rules (The "Bouncer")
        is_valid = (
            t['Quantity'] > 0 and 
            t['UnitPrice'] > 0 and 
            t['TransactionID'].startswith('T') and 
            t['ProductID'].startswith('P') and 
            t['CustomerID'].startswith('C')
        )
        
        if not is_valid:
            invalid_count += 1
            continue  
            
        # 2. Region Filtering
        # Logic: If a region is specified AND it doesn't match, filter it out
        if region and t['Region'].strip().lower() != region:
            region_filtered_count += 1
            continue
            
        # 3. Amount Filtering
        amount = t['Quantity'] * t['UnitPrice']
        if (min_amount is not None and amount < min_amount) or \
           (max_amount is not None and amount > max_amount):
            amount_filtered_count += 1
            continue
            
        # If it survived all checks, add to final list
        valid_transactions.append(t)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': region_filtered_count,
        'filtered_by_amount': amount_filtered_count,
        'final_count': len(valid_transactions)
    }
    
    return (valid_transactions, invalid_count, summary)

