import datetime
from utils.file_handler import read_sales_data,parse_transactions, validate_and_filter
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
from utils.data_process import (calculate_total_revenue, region_wise_sales,top_selling_products,
                                 customer_analysis, daily_sales_trend,find_peak_sales_day,
                                 low_performing_products)

def generate_sales_report(transactions, enriched_transaction,output_file = 'output/sales_report.txt'):
    #overall summary
    Total_revenue = calculate_total_revenue(transactions)
    Total_transactions = len(transactions)
    Avg_order_value = Total_revenue/Total_transactions
    dates = []
    for t in transactions:
        if t['Date']:
            dates.append(t['Date'])
    date1 = min(dates)
    date2 = max(dates)
    date_r = f"{date1} to {date2}"
        

    #region
    Region_data = region_wise_sales(transactions)
    sorted_reg = sorted(Region_data.items(),key=lambda x:x[1]['total_sales'],reverse = True)

    #top 5
    prod = top_selling_products(transactions, n=5)
    cust = customer_analysis(transactions)
    sorted_cust = sorted(cust.items(),key = lambda x:x[1]['total_spent'],reverse = True)
    #daily
    daily = daily_sales_trend(transactions)
    #product performance analysis
    peak_sale = find_peak_sales_day(transactions)
    low_prod = low_performing_products(transactions)

    ## API ENRICHMENT
    success = []
    failure = []
    total_records = len(enriched_transaction)

    for t in enriched_transaction:
        if t['API_match'] == True:
            success.append(t)
        else:
            failure.append(t)
    success_count = len(success)
    failure_count = len(failure)
    percentage = (success_count/total_records)*100
    failed_products = set()
    for t in failure:
        if t['ProductName']:
            failed_products.add(t['ProductName'])
        else:
            pass
    failed_products = sorted(failed_products)
    #report
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, "w", encoding="utf-8") as f:

        f.write("=" * 44 + "\n")
        f.write("          SALES ANALYTICS REPORT\n")
        f.write(f"        Generated: {now}\n")
        f.write(f"        Records Processed: {Total_transactions}\n")
        f.write("=" * 44 + "\n\n")
        f.write(f"Overall Summary\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue     Rs.:{Total_revenue:,.2f}\n")
        f.write(f"Total transactions   :{Total_transactions:,.2f}\n")
        f.write(f"Average order value  :{Avg_order_value:,.2f}\n")
        f.write(f"Date range           :{date_r}\n")


        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<15}{'Transactions'}\n")
        for region,trans in sorted_reg:
            total_sales = trans['total_sales']
            pct = trans['percentage']
            count = trans['transaction_count']
            f.write(
                f"{region:<10}"
                f"₹{total_sales:14,.2f}     "
                f"{pct:>10.2f}%        "
                f"{count:>10}\n"
            )
        f.write("\nTop 5 Products\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Product_name':<15}{'Quantity sold':>12}{'Revenue':>10}\n")
        for rank,(product,qty,revenue) in enumerate(prod, start = 1):
            f.write(
                f"{rank:<6}"
                f"{product:<25}"
                f"{qty:<8}"
                f"₹{revenue:>14,.2f}\n")
        f.write("\n")
        f.write(f"{'Rank':<10}{'customer_id':<15}{'Total spent':>12}{'Order count':>10}\n")
        for rank,(cid,trans) in enumerate(sorted_cust,start = 1):
            total_spent = trans['total_spent']
            order_count = trans['purchase_count']
            f.write(
                f"{rank:<6}"
                f"{cid:<15}"
                f"{total_spent:<12,.2f}"
                f"{order_count:>10}\n")
        f.write("\n")
        f.write("DAILY SALES TREND")
        f.write("-" * 44 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>12}{'transactions':>8}{'Unique customers':>10}\n")
        for date,trans in daily.items():
            revenue = trans['revenue']
            transaction = trans['transaction_count']
            unique_cust = trans['unique_customers']
            f.write(
                f"{date:<12}"
                f"₹{revenue:>11,.2f}     "
                f"{transaction:>8}        "
                f"{unique_cust:>10}\n")
        f.write("\n")
        f.write("Product Performance Analysis\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best selling day: {peak_sale[0]}\n")
        f.write("Lowest performing products\n")
        f.write(f"{'Product_name':<10}{'Quantity':<15}{'revenue'}\n")
        for products,totalquantity,revenue in low_prod:
            f.write(
                f"{products:<10}"
                f"{totalquantity:>8}"
                f"{revenue:>11,.2f}\n")
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Successfully Enriched:  {success_count}\n")
        f.write(f"Success Rate:           {percentage:.2f}%\n")
        f.write("Products Not Enriched:\n")

        for product in failed_products:
            f.write(f" - {product}\n")

        f.write("\n")
    return output_file
                        
            
        
        
      
            
              
            
            
            
            
    
    
    