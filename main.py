from output.output import generate_sales_report
from utils.data_process import calculate_total_revenue, region_wise_sales,top_selling_products, customer_analysis, daily_sales_trend,find_peak_sales_day, low_performing_products
from utils.file_handler import read_sales_data,parse_transactions, validate_and_filter

def main():
    
    print("="*40)
    print("Sales Analytics System - Started")
    print("="*40)
    # Step 1: Read and parse sales data
    try:
        raw_lines = read_sales_data('data/sales_data.txt')
        if isinstance(raw_lines, str):
            print(raw_lines)
            return
        print("\n[2/7] Parsing data and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"parsed transactions : {len(parsed_transactions)}")
        print("\n[3/7] validation and filtering")
        print("enter your choice on filtering [y/n]")
        region = None
        min_amount = None
        max_amount = None
        choice = input("enter your choice on filtering [y/n]")
        try:
           if choice == "y":
                region = input("Enter the region\n").strip().lower()
                region = region if region else None
                min_amount = input("Enter the min amount\n").strip()
                min_amount = float(min_amount) if min_amount else None
                max_amount = input("Enter the max amount\n").strip()
                max_amount = float(max_amount) if max_amount else None
        except Exception as e:
            print("Invalid input for filtering. Proceeding without filters.")
        print("\n[4/7] Validating transactions...")

        valid_transactions,invalid_count,summary = validate_and_filter(parsed_transactions,region,min_amount,max_amount)

        print("Validating transactions and printing summary\n")
        print(f"Total Input: {summary['total_input']}")
        print(f"Invalid: {summary['invalid']}")
        print(f"Filtered by Region: {summary['filtered_by_region']}")
        print(f"Filtered by Amount: {summary['filtered_by_amount']}")
        print(f"Final Valid Transactions: {summary['final_count']}")

        print("="*44)
        print("[5/] Data processing")
        total_revenue = calculate_total_revenue(valid_transactions)
        print(f"Total Revenue: {(total_revenue)}")
        print("[6/] Region Wise Summary/n")
        region_summary = region_wise_sales(valid_transactions)
        print(f" Region wise sales summary {(region_summary)}")
        top_products = top_selling_products(valid_transactions,n=5)
        print(f" Top 5 selling products {(top_products)}")
        customer_analysis_data = customer_analysis(valid_transactions)
        print(f" Customer analysis data {(customer_analysis_data)}")
        daily_trend = daily_sales_trend(valid_transactions)
        print(f" Daily sales trend {(daily_trend)}")
        peak_sales = find_peak_sales_day(valid_transactions)
        print(f" Peak sales day {(peak_sales)}")
        low_performing = low_performing_products(valid_transactions)
        print(f" Low performing products {(low_performing)}")
        print("="*44)
        print("Api Enrichment\n")
        from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
        print("[7/7] Fetching product data from API...")
        products = 'https://dummyjson.com/products?limit=100'
        api_products = fetch_all_products(products)
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        print("Enrichment completed.\n")
        print("Generating sales report...")
        generate_sales_report(valid_transactions, enriched_transactions, output_file='output/sales_report.txt')



    except Exception as e:
        print(" Error encountered:", e)

if __name__ == "__main__":
    main()
