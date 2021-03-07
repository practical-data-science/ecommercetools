import pandas as pd
import numpy as np
from ecommercetools.utilities import tools


def get_transactions(transaction_items):
    """Return a Pandas DataFrame of transactions from a Pandas DataFrame of transaction items.

    Args:
        transaction_items (object): DataFrame containing order_id, sku, quantity, unit_price, customer_id, order_date

    Returns:
        transactions: Pandas DataFrame containing transactions
    """

    transaction_items = transaction_items.sort_values(by=['order_date'], ascending=True)
    transactions = transaction_items.groupby('order_id').agg(
        order_date=('order_date', 'max'),
        customer_id=('customer_id', 'max'),
        skus=('sku', 'nunique'),
        items=('quantity', 'sum'),
        revenue=('line_price', 'sum'),
    ).reset_index()
    transactions['replacement'] = np.where(transactions['revenue'] > 0, 0, 1)
    transactions['order_number'] = tools.get_cumulative_count(transactions,
                                                              'customer_id',
                                                              'order_id',
                                                              'order_date') + 1
    return transactions


