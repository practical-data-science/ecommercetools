import pandas as pd
from ecommercetools import utilities
from ecommercetools import transactions
from ecommercetools import products
from ecommercetools import customers
from ecommercetools import operations

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
