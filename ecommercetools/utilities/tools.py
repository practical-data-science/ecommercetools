import pandas as pd
import numpy as np
from datetime import timedelta, datetime


def load_transaction_items(filename,
                           date_column='order_date',
                           order_id_column='order_id',
                           customer_id_column='customer_id',
                           sku_column='sku',
                           quantity_column='quantity',
                           unit_price_column='unit_price'
                           ):
    """Load a CSV of transactional item data, sets standard column names, and calculates line price.

    Args:
        filename (str): Filename and path of CSV file containing transaction items.
        date_column (str, optional): Name of order date column, default is order_date
        order_id_column (str, optional): Name of order ID column, default is order_id
        customer_id_column (str, optional): Name of customer ID column, default is customer_id
        sku_column (str, optional): Name of SKU column, default is sku
        quantity_column (int, optional): Name of quantity column, default is quantity
        unit_price_column (float, optional): Name of unit price column, default is unit_price

    Usage:
        transaction_items = rt.load_data('data/input/transaction_items_non_standard_names.csv',
                                     date_column='InvoiceDate',
                                     order_id_column='OrderId',
                                     customer_id_column='CustomerId',
                                     sku_column='VariantId',
                                     quantity_column='Qty',
                                     unit_price_column='Price'
                                     )

    Returns:
        A Pandas dataframe containing the same data with the column names changed to the
        standardised names used throughout RetailTools, if they do not already match, and
        the order_date column correctly set as a datetime column. If the user provides a
        CSV file in which the column names are already set to these values, it it not a
        requirement to provide them.

    """

    df = pd.read_csv(filename, parse_dates=[date_column])
    df = df.rename(columns={
        date_column: 'order_date',
        order_id_column: 'order_id',
        customer_id_column: 'customer_id',
        sku_column: 'sku',
        quantity_column: 'quantity',
        unit_price_column: 'unit_price'
    })
    df['line_price'] = round(df['quantity'] * df['unit_price'], 2)
    return df


def load_sample_data():
    """Load the Online Retail dataset of transaction items and format for use within EcommerceTools functions.

    :return: Pandas dataframe.
    """

    df = pd.read_csv('https://raw.githubusercontent.com/databricks/Spark-The-Definitive-Guide/master/data'
                     '/retail-data/all/online-retail-dataset.csv',
                     names=['order_id', 'sku', 'description', 'quantity', 'order_date', 'unit_price', 'customer_id',
                            'country'],
                     skiprows=1,
                     parse_dates=['order_date']
                     )
    df['line_price'] = df['unit_price'] * df['quantity']
    return df


def get_cumulative_count(df, group_column, count_column, sort_column):
    """Get the cumulative count of a column based on a GroupBy.

    Args:
        df (object): Pandas DataFrame.
        group_column (string): Column to group by.
        count_column (string): Column to count.
        sort_column (string): Column to sort by.

    Returns:
        Cumulative count of the column.

    Usage:
        df['running_total'] = get_cumulative_count(df, 'customer_id', 'order_id', 'date_created')
    """

    df = df.sort_values(by=sort_column, ascending=True)
    return df.groupby([group_column])[count_column].cumcount()


def get_previous_value(df, group_column, value_column):
    """Group by a column and return the previous value of another column and assign value to a new column.

    Args:
        df (object): Pandas DataFrame.
        group_column (str): Column name to group by
        value_column (str): Column value to return.

    Returns:
        Original DataFrame with new column containing previous value of named column.
    """

    df = df.copy()
    df = df.sort_values(by=[value_column], ascending=False)
    return df.groupby([group_column])[value_column].shift(-1)


def get_days_since_date(df, before_datetime, after_datetime):
    """Return a new column containing the difference between two dates in days.

    Args:
        df (object): Pandas DataFrame.
        before_datetime (datetime): Earliest datetime (will convert value)
        after_datetime (datetime): Latest datetime (will convert value)

    Returns:
        New column value
    """

    df = df.copy()
    df[before_datetime] = pd.to_datetime(df[before_datetime])
    df[after_datetime] = pd.to_datetime(df[after_datetime])

    diff = df[after_datetime] - df[before_datetime]
    return round(diff / np.timedelta64(1, 'D')).fillna(0).astype(int)


def date_subtract(date, days):
    """Given a date, subtract a specified number of days, and return the date.

    Args:
        date (datetime): Original date to subtract from.
        days (int): Number of days to subtract from date.

    Return:
        subtracted_date (datetime): Original date with days subtracted.
    """

    return pd.to_datetime(date) - timedelta(days=days)


def select_last_x_days(df,
                       date_column='order_date',
                       days=365):
    """Select the last X days from a Pandas dataframe.

    Args:
        df (object): Pandas dataframe containing time series data.
        date_column (str, optional): Name of column containing date. Default is order_date.
        days (int, optional): Number of days to subtract from current date. Default is 365.

    Returns:
        df (object): Filtered dataframe containing only records from the past X days.
    """

    subtracted_date = date_subtract(datetime.today(), days)
    df = df[df[date_column] >= subtracted_date]
    return df
