import pandas as pd
from ecommercetools.products import products


def _abc_classify_product(percentage):
    """Return an ABC classification for a product based on its ranked percentage revenue contribution.

    Args:
        percentage (float): Running percentage of revenue contributed by each SKU over a time period.

    Returns:
        class (string): ABC class string
    """

    if 0 < percentage <= 80:
        return 'A'
    elif 80 < percentage <= 90:
        return 'B'
    else:
        return 'C'


def get_inventory_classification(transaction_items, days=None, verbose=False):
    """Return a Pandas DataFrame of product inventory classification from the transaction items dataframe.

    Args:
        transaction_items (object): Pandas DataFrame of transaction items.
        days (int, optional): Return data only for products sold in the past X days.
        verbose (bool, optional): Displays additional columns of workings when set to True.

    Returns:
        products (object): Pandas DataFrame.
    """

    # Filter to the last X days
    if days:
        products_data = products.get_products(transaction_items, days)
    else:
        products_data = products.get_products(transaction_items)

    # Sort the data
    products_data['revenue_total'] = products_data['revenue'].sum()
    products_data = products_data.sort_values(by='revenue', ascending=False)

    # ABC inventory classification
    products_data['revenue_cumsum'] = products_data['revenue'].cumsum()
    products_data['revenue_running_percentage'] = (products_data['revenue_cumsum'] / products_data['revenue_total']) * 100
    products_data['abc_class'] = products_data['revenue_running_percentage'].apply(_abc_classify_product)
    products_data['abc_rank'] = products_data['revenue_running_percentage'].rank().astype(int)

    if verbose:
        products_data = products_data[['sku', 'abc_class', 'abc_rank', 'revenue',
                                       'revenue_cumsum', 'revenue_total', 'revenue_running_percentage']]
    else:
        products_data = products_data[['sku', 'abc_class', 'abc_rank']]

    return products_data
