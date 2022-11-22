import pandas as pd
from ecommercetools import utilities
from ecommercetools import transactions
from ecommercetools import products
from ecommercetools import customers
from ecommercetools import operations
from ecommercetools import seo
from ecommercetools import reports

"""


# =======================================================================
# Load sample data
# =======================================================================

transaction_items = utilities.load_sample_data()
print(transaction_items.head())

# =======================================================================
# Create transactions dataframe
# =======================================================================

transactions = transactions.get_transactions(transaction_items)
print(transactions.head())

# =======================================================================
# Create products dataframe
# =======================================================================

products_df = products.get_products(transaction_items)
print(products_df.head())

# =======================================================================
# Create repurchase rates dataframe
# =======================================================================

repurchase_rates = products.get_repurchase_rates(transaction_items)
print(repurchase_rates.head(3))

# =======================================================================
# Create customers dataframe
# =======================================================================

customers_df = customers.get_customers(transaction_items)
print(customers_df.head())

# =======================================================================
# Create cohorts dataframe
# =======================================================================

cohorts_df = customers.get_cohorts(transaction_items, period='M')
print(cohorts_df.head())

# =======================================================================
# Create cohort matrix dataframe
# =======================================================================

cohort_matrix_df = customers.get_cohort_matrix(transaction_items, period='M', percentage=True)
print(cohort_matrix_df.head())

cohort_matrix_df = customers.get_cohort_matrix(transaction_items, period='M', percentage=False)
print(cohort_matrix_df.head())

# =======================================================================
# Create retention dataframe
# =======================================================================

retention_df = customers.get_retention(transactions)
print(retention_df.head())

# =======================================================================
# Create RFMH dataframe
# =======================================================================

rfm_df = customers.get_rfm_segments(customers_df)
print(rfm_df.head())

# =======================================================================
# Create latency dataframe
# =======================================================================

latency_df = customers.get_latency(transactions)
print(latency_df.head())

# =======================================================================
# Create customer ABC dataframe
# =======================================================================

abc_df = customers.get_abc_segments(customers_df, months=12, abc_class_name='abc_class_12m', abc_rank_name='abc_rank_12m')
print(abc_df.head())

# =======================================================================
# Create customer predictions dataframe
# =======================================================================

customer_predictions = customers.get_customer_predictions(transactions,
                                                          observation_period_end='2011-12-09',
                                                          days=90)
print(customer_predictions.head(10))

# =======================================================================
# Create ABC inventory classification dataframe
# =======================================================================

inventory_classification = operations.get_inventory_classification(transaction_items, verbose=True)
print(inventory_classification.head())
print(inventory_classification.abc_class.value_counts())

# =======================================================================
# Scrape a bunch of URLs
# =======================================================================

urls = ['https://practicaldatascience.co.uk/data-science/how-to-create-a-pandas-dataframe',
        'https://practicaldatascience.co.uk/data-science/how-to-query-the-google-search-console-api-with-ecommercetools',
        'https://practicaldatascience.co.uk/data-science/how-to-assign-rfm-scores-with-quantile-based-discretization',
        '404',
        'https://practicaldatascience.co.uk/data-science/how-to-engineer-customer-purchase-latency-features',
        'https://practicaldatascience.co.uk/assets/files/marketing.pdf'
        ]
df = pd.DataFrame(list(zip(urls)), columns=['loc'])

df_pages = seo.scraping.scrape_site(df)

print(df_pages)


# =======================================================================
# Get SERPs
# =======================================================================

results = seo.get_serps("bearded dragon brumation", pages=3)
print(results)


# =======================================================================
# Get indexed pages
# =======================================================================

results = seo.get_indexed_pages(["https://www.bbc.co.uk",  # Millions
                                 "https://www.practicaldatascience.co.uk",  # 1
                                 "https://www.shj989uiskjdlksjd.com"  # None
                                 ])
print(results)
exit()

# =======================================================================
# Get all Google Search Console data
# =======================================================================

key = "pds-client-secrets.json"
site_url = "sc-domain:practicaldatascience.co.uk"
payload = {
    'startDate': "2021-01-01",
    'endDate': "2021-08-31",
    'dimensions': ["query"],
    'rowLimit': 25000,
    'startRow': 0
}

df = seo.query_google_search_console(key, site_url, payload, fetch_all=True)
print(len(df))

# =======================================================================
# Compare two Google Search Console periods
# =======================================================================

payload_before = {
    'startDate': "2021-08-11",
    'endDate': "2021-08-31",
    'dimensions': ["page", "query"],
}

payload_after = {
    'startDate': "2021-07-21",
    'endDate': "2021-08-10",
    'dimensions': ["page","query"],
}

df = seo.query_google_search_console_compare(key, site_url, payload_before, payload_after, fetch_all=False)
print(df.sort_values(by='clicks_change', ascending=False).head())

# =======================================================================
# Load customers report
# =======================================================================

df_customers_report = reports.customers_report(transaction_items, frequency='M')
print(df_customers_report.head(13))

# =======================================================================
# Load transactions report
# =======================================================================

df_orders_report = reports.transactions_report(transaction_items, frequency='M')
print(df_orders_report.head(13))


# =======================================================================
# Classify Google Search Console data using ABCD
# =======================================================================

key = "pds-client-secrets.json"
site_url = "sc-domain:practicaldatascience.co.uk"
start_date = '2022-10-01'
end_date = '2022-10-31'

df_classes = seo.classify_pages(key, site_url, start_date, end_date, output='classes')
print(df_classes.head())

df_summary = seo.classify_pages(key, site_url, start_date, end_date, output='summary')
print(df_summary)


"""