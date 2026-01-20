Sales Analytics System
A Python-based data pipeline designed to process local sales transactions, validate data integrity, and enrich records with real-time product information from an external API.

Project Overview
This system automates the workflow of a data analyst by:

Reading raw sales data: Robust support for pipe-delimited text files.

Cleaning and Validation: Ensuring data quality across all transaction records.

Data Enrichment: Integrating with the DummyJSON API to fetch extended product details like Brand and Rating.

Generating Reports: Creating an enriched_sales_data.txt file and a final analytics report.

Setup Instructions
To set up this project on your local machine, follow these steps:

Clone the repository:

git clone https://github.com/karwayunishaan/bitsom_ba_25071953-sales-analytics-system.git

cd bitsom_ba_25071953-sales-analytics-system

Install Dependencies: This project requires the requests library to handle API calls. Install it using:
python -m pip install -r requirements.txt

How to Run
Once the setup is complete, you can run the main application using:
python main.py

Project Structure
main.py: The primary entry point that coordinates the data processing workflow.

utils/api_handler.py: Contains logic for fetching and mapping API data.

utils/file_handler.py: Manages reading/writing the pipe-delimited files.

data/: Contains sales_data.txt (input) and enriched_sales_data.txt (output).

output/: Contains the final sales_report.txt.
