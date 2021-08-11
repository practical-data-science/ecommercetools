import pandas as pd


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


