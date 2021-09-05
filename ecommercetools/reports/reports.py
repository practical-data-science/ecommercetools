import pandas as pd
import numpy as np
from ecommercetools import transactions


def report_period_overview(df, period_type='M'):
    """Return an overview of customers, orders, units, and revenue with averages per order and customer.

    Args:
        df (dataframe): Pandas dataframe containing formatted transaction items data.
        period_type (string, optional): Period type, i.e. M for month, W for week, or Y for Year.

    Returns:
        df (dataframe): Pandas dataframe containing aggregate data for each period.
    """

    df = df.assign(period=df.groupby('customer_id')['order_date'].transform('min').dt.to_period(period_type))

    df = df.groupby('period').agg(
        customers=('customer_id', 'nunique'),
        orders=('order_id', 'nunique'),
        units=('quantity', 'sum'),
        revenue=('line_price', 'sum')
    )

    df['avg_order_value'] = round(df['revenue'] / df['orders'], 2)
    df['avg_units_per_order'] = round(df['units'] / df['orders'], 2)
    df['avg_orders_per_customer'] = round(df['orders'] / df['customers'], 2)
    df['avg_revenue_per_customer'] = round(df['revenue'] / df['customers'], 2)
    df = df.sort_values(by='period', ascending=False).reset_index()

    return df


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
        skus=('sku', 'nunique'),
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
