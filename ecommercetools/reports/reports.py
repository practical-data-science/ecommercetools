import pandas as pd
import numpy as np
from ecommercetools import transactions


def transactions_report(df, frequency='M'):
    """Create an transactions report based on a specified reporting frequency.

    Args:
        df (dataframe): Pandas dataframe of transaction items.
        frequency (optional, string, default 'M'): Optional frequency indicator (Y, Q, M, W, D)

    Returns:
        df (dataframe): Pandas dataframe of aggregated data for the specified frequency.
    """

    df['year'] = df['order_date'].dt.year
    df['quarter'] = df['order_date'].dt.quarter
    df['year_quarter'] = df['year'].astype(str) + '-' + df['quarter'].astype(str)
    df['month'] = df['order_date'].dt.month
    df['year_month'] = df['order_date'].dt.strftime('%Y-%m')
    df['week'] = df['order_date'].dt.strftime('%W')
    df['year_week'] = df['order_date'].dt.strftime('%Y-%W')
    df['day'] = df['order_date'].dt.strftime('%j')
    df['year_day'] = df['order_date'].dt.strftime('%Y-%j')

    if frequency == 'Y':
        group = 'year'
    elif frequency == 'Q':
        group = 'year_quarter'
    elif frequency == 'W':
        group = 'year_week'
    elif frequency == 'D':
        group = 'year_day'
    else:
        group = 'year_month'

    df_agg = df.groupby(group).agg(
        customers=('customer_id', 'nunique'),
        orders=('order_id', 'nunique'),
        revenue=('line_price', 'sum'),
        skus=('sku', 'count'),
        units=('quantity', 'sum')
    ).reset_index()

    df_agg['avg_order_value'] = round(df_agg['revenue'] / df_agg['orders'], 2)
    df_agg['avg_skus_per_order'] = round(df_agg['skus'] / df_agg['orders'], 2)
    df_agg['avg_units_per_order'] = round(df_agg['units'] / df_agg['orders'], 2)
    df_agg['avg_revenue_per_customer'] = round(df_agg['revenue'] / df_agg['customers'], 2)

    return df_agg


def customers_report(transaction_items_df, frequency='M'):
    """Create a customers report based on a specified reporting frequency.

    Args:
        df (dataframe): Pandas dataframe of transaction items.
        frequency (optional, string, default 'M'): Optional frequency indicator (Y, Q, M, W, D)

    Returns:
        df (dataframe): Pandas dataframe of aggregated data for the specified frequency.
    """

    df = transactions.get_transactions(transaction_items_df)

    df['period'] = df['order_date'].dt.strftime('%B, Y')
    df['year'] = df['order_date'].dt.year
    df['quarter'] = df['order_date'].dt.quarter
    df['year_quarter'] = df['year'].astype(str) + '-' + df['quarter'].astype(str)
    df['month'] = df['order_date'].dt.month
    df['year_month'] = df['order_date'].dt.strftime('%Y-%m')
    df['week'] = df['order_date'].dt.strftime('%W')
    df['year_week'] = df['order_date'].dt.strftime('%Y-%W')
    df['day'] = df['order_date'].dt.strftime('%j')
    df['year_day'] = df['order_date'].dt.strftime('%Y-%j')

    if frequency == 'Y':
        group = 'year'
    elif frequency == 'Q':
        group = 'year_quarter'
    elif frequency == 'W':
        group = 'year_week'
    elif frequency == 'D':
        group = 'year_day'
    else:
        group = 'year_month'

    df['new_customers'] = np.where(df['order_number'] == 1, 1, 0)

    df_agg = df.groupby(group).agg(
        orders=('order_id', 'nunique'),
        customers=('customer_id', 'nunique'),
        new_customers=('new_customers', 'sum'),
    ).reset_index()

    df_agg['returning_customers'] = df_agg['customers'] - df_agg['new_customers']
    df_agg['acquisition_rate'] = round((df_agg['new_customers'] / df_agg['customers']) * 100, 2)

    return df_agg
