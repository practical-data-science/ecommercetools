import pandas as pd
from ecommercetools.utilities import tools


def get_products(transaction_items, days=None):
    """Return a Pandas DataFrame of products from a Pandas DataFrame of transaction items.

    Args:
        transaction_items (object): Pandas DataFrame.
        days (int, optional): Select only product sold in the last X days.

    Returns:
        customers (object): Pandas DataFrame
    """

    if days:
        transaction_items = tools.select_last_x_days(transaction_items, 'order_date', days)

    transaction_items = transaction_items.assign(line_price=transaction_items['quantity'] * transaction_items['unit_price'])

    products = transaction_items.groupby('sku').agg(
        first_order_date=('order_date', 'min'),
        last_order_date=('order_date', 'max'),
        customers=('customer_id', 'nunique'),
        orders=('order_id', 'nunique'),
        items=('quantity', 'sum'),
        revenue=('line_price', 'sum'),
        avg_unit_price=('unit_price', 'mean'),
        avg_quantity=('quantity', 'mean'),
        avg_revenue=('line_price', 'mean')
    ).reset_index()

    products['avg_orders'] = round(products['orders'] / products['customers'], 2)
    products['product_tenure'] = (pd.to_datetime('today') - products['first_order_date']).dt.days
    products['product_recency'] = (pd.to_datetime('today') - products['last_order_date']).dt.days
    return products


def get_repurchase_rate_label(df):
    """Add a label describing the repurchase rate bin.

    Args:
        df (object): Pandas DataFrame containing repurchase_rate.

    Returns:
    -------
        df (object): Pandas DataFrame with repurchase_rate_label added.
    """

    labels = ['Very low repurchase',
              'Low repurchase',
              'Moderate repurchase',
              'High repurchase',
              'Very high repurchase']
    df['repurchase_rate_label'] = pd.cut(df['repurchase_rate'],
                                         bins=5,
                                         labels=labels)
    return df


def get_bulk_purchase_rate_label(df):
    """Add a label describing the bulk purchase rate bin.

    Args:
        df (object): Pandas DataFrame containing bulk_purchase_rate.

    Returns:
    -------
        df (object): Pandas DataFrame with bulk_purchase_rate_label added.
    """

    labels = ['Very low bulk',
              'Low bulk',
              'Moderate bulk',
              'High bulk',
              'Very high bulk']
    df['bulk_purchase_rate_label'] = pd.cut(df['bulk_purchase_rate'],
                                            bins=5,
                                            labels=labels)
    return df


def get_repurchase_rates(df):
    """Return repurchase rates and purchase behaviour for each SKU from transaction items data.

    Given a Pandas DataFrame of transactional items, this function returns a Pandas DataFrame
    containing the purchase behaviour and repurchase behaviour for each SKU.

    Args:
        df (object): Pandas DataFrame. Required columns: sku, order_id, customer_id, quantity, unit_price.

    Returns:
    -------
        df (object): Pandas DataFrame.
    """

    # Count the number of times each customer purchased each SKU
    df['times_purchased'] = df.groupby(['sku', 'customer_id'])['order_id'].transform('count')

    # Count the number of times the SKU was purchased individually within orders
    df['purchased_individually'] = df[df['quantity'] == 1]. \
        groupby('sku')['order_id'].transform('count')
    df['purchased_individually'] = df['purchased_individually'].fillna(0)

    # Count the number of times the SKU was purchased once only by customers
    df['purchased_once'] = df[df['times_purchased'] == 1]. \
        groupby('sku')['order_id'].transform('count')
    df['purchased_once'] = df['purchased_once'].fillna(0)

    # Calculate line price
    df['line_price'] = df['unit_price'] * df['quantity']

    # Get unique SKUs and count total items, orders, and customers
    df_skus = df.groupby('sku').agg(
        revenue=('line_price', 'sum'),
        items=('quantity', 'sum'),
        orders=('order_id', 'nunique'),
        customers=('customer_id', 'nunique'),
        avg_unit_price=('unit_price', 'mean'),
        avg_line_price=('line_price', 'mean')
    )

    # Calculate the average number of units per order
    df_skus = df_skus.assign(avg_items_per_order=(df_skus['items'] / df_skus['orders']))

    # Calculate the average number of items per customer
    df_skus = df_skus.assign(avg_items_per_customer=(df_skus['items'] / df_skus['customers']))

    # Merge the dataframes
    df_subset = df[['sku', 'purchased_individually', 'purchased_once']].fillna(0)
    df_subset.drop_duplicates('sku', keep='first', inplace=True)
    df_skus = df_skus.merge(df_subset, on='sku', how='left')

    # Calculate bulk purchase rates
    df_skus = df_skus.assign(bulk_purchases=(df_skus['orders'] - df_skus['purchased_individually']))
    df_skus = df_skus.assign(bulk_purchase_rate=(df_skus['bulk_purchases'] / df_skus['orders']))

    # Calculate repurchase rates
    df_skus = df_skus.assign(repurchases=(df_skus['orders'] - df_skus['purchased_once']))
    df_skus = df_skus.assign(repurchase_rate=(df_skus['repurchases'] / df_skus['orders']))

    # Add labels
    df_skus = get_repurchase_rate_label(df_skus)
    df_skus = get_bulk_purchase_rate_label(df_skus)

    df_skus['bulk_and_repurchase_label'] = df_skus['repurchase_rate_label'].astype(str) + \
                                           '_' + df_skus['bulk_purchase_rate_label'].astype(str)

    return df_skus
