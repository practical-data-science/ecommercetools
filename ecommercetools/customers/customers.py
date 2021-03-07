import pandas as pd
import numpy as np
import operator as op
from ecommercetools.transactions import transactions
from ecommercetools.utilities import tools
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def get_customers(transaction_items):
    """Return a Pandas DataFrame of customers from a Pandas DataFrame of transaction items.

    Args:
        transaction_items (object): DataFrame containing order_id, sku, quantity, unit_price, customer_id, order_date

    Returns:
        customers: Pandas DataFrame containing customers
    """

    transactions_df = transactions.get_transactions(transaction_items)
    customers = transactions_df.groupby('customer_id').agg(
        revenue=('revenue', 'sum'),
        orders=('order_id', 'nunique'),
        skus=('skus', 'nunique'),
        items=('items', 'sum'),
        first_order_date=('order_date', 'min'),
        last_order_date=('order_date', 'max')
    ).reset_index()
    customers['avg_items'] = round((customers['items'] / customers['orders']), 2)
    customers['avg_order_value'] = round((customers['revenue'] / customers['orders']), 2)
    customers['tenure'] = (pd.to_datetime('today') - customers['first_order_date']).dt.days
    customers['recency'] = (pd.to_datetime('today') - customers['last_order_date']).dt.days
    customers['cohort'] = customers['first_order_date'].dt.year.astype(str) + \
                          customers['first_order_date'].dt.quarter.astype(str)
    return customers


def _sorted_kmeans(df,
                   metric_column,
                   cluster_name,
                   ascending=True):
    """Runs a K-means clustering algorithm on a specific metric column in a Pandas dataframe.

    Sorts the data in a specified direction; and reassigns cluster numbers to match the data distribution,
    so they are appropriate for RFM segmentation. You may need to log transform heavily skewed data.

    Args:
        df (object): Pandas dataframe
        metric_column (str): Name of metric column
        ascending (bool, optional): Set to False to sort in descending order
        cluster_name (str): Name of cluster

    Returns:
        Original Pandas DataFrame with additional column
    """

    # Fit the model
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(df[[metric_column]])

    # Assign the initial unsorted cluster
    initial_cluster = 'unsorted_' + cluster_name
    df[initial_cluster] = kmeans.predict(df[[metric_column]]) + 1
    df[cluster_name] = df[initial_cluster]

    # Group the clusters and re-rank to determine the correct order
    df_sorted = df.groupby(initial_cluster)[metric_column].mean().round(2).reset_index()
    df_sorted = df_sorted.sort_values(by=metric_column, ascending=ascending).reset_index(drop=True)
    df_sorted[cluster_name] = df_sorted[metric_column].rank(method='max', ascending=ascending).astype(int)

    # Merge data and drop redundant columns
    df = df.merge(df_sorted[[cluster_name, initial_cluster]], on=[initial_cluster])
    df = df.drop(initial_cluster, axis=1)
    df = df.drop(cluster_name + '_x', axis=1)
    df = df.rename(columns={cluster_name + '_y': cluster_name})

    return df


def _label_rfm_segments(rfm):
    """Return a label for a customer based on their RFM score

    Args:
        rfm (int): Full three-digit RFM score, i.e. 555 or 111

    Returns:
        label (str): Descriptive RFM score label, i.e. Risky
    """

    rfm = int(rfm)

    if (rfm >= 111) & (rfm <= 155):
        return 'Risky'

    elif (rfm >= 211) & (rfm <= 255):
        return 'Hold and improve'

    elif (rfm >= 311) & (rfm <= 353):
        return 'Potential loyal'

    elif ((rfm >= 354) & (rfm <= 454)) or ((rfm >= 511) & (rfm <= 535)) or (rfm == 541):
        return 'Loyal'

    elif (rfm == 455) or (rfm >= 542) & (rfm <= 555):
        return 'Star'

    else:
        return 'Other'


def get_rfm_segments(customers):
    """Return a Pandas DataFrame of customer RFM segments from a Pandas DataFrame of customers.

    The DataFrame returned by get_customers() already contains the raw data required, but
    this function will rename it accordingly and use it to assign the customer to a range
    of different segments that can be used for marketing and analysis.

    Args:
        customers: Pandas DataFrame from get_customers()

    Returns:
        segments: Pandas DataFrame

    """

    # Rename the raw data columns
    segments = customers[['customer_id']]
    segments = segments.assign(acquisition_date=customers['first_order_date'])
    segments = segments.assign(recency_date=customers['last_order_date'])
    segments = segments.assign(recency=customers['recency'])
    segments = segments.assign(frequency=customers['orders'])
    segments = segments.assign(monetary=customers['revenue'])
    segments = segments.assign(heterogeneity=customers['skus'])
    segments = segments.assign(tenure=customers['tenure'])

    # Use K-means to create RFMH scores
    segments = _sorted_kmeans(segments, 'recency', 'r', ascending=False)
    segments = _sorted_kmeans(segments, 'frequency', 'f', ascending=True)
    segments = _sorted_kmeans(segments, 'monetary', 'm', ascending=True)
    segments = _sorted_kmeans(segments, 'heterogeneity', 'h', ascending=True)

    # Create scores
    segments = segments.assign(rfm=segments['r'].astype(str) + \
                                   segments['f'].astype(str) + \
                                   segments['m'].astype(str))

    segments = segments.assign(rfm_score=segments['r'].astype(int) + \
                                         segments['f'].astype(int) + \
                                         segments['m'].astype(int))

    # Create labels
    segments['rfm_segment_name'] = segments.apply(lambda x: _label_rfm_segments(x.rfm), axis=1)

    return segments


def _abc_classify_customer(percentage):
    """Apply an ABC classification to each customer based on its ranked percentage revenue contribution.

    Args:
        percentage (float): Cumulative percentage of ranked revenue

    Returns:
        segments: Pandas DataFrame
    """

    if 0 < percentage <= 80:
        return 'A'
    elif 80 < percentage <= 90:
        return 'B'
    else:
        return 'C'


def get_abc_segments(customers,
                     months=12,
                     abc_class_name='abc_class_12m',
                     abc_rank_name='abc_rank_12m'):
    """Return a dataframe containing the ABC class and rank for each customer.

    Apply an ABC classification to each customer based on its ranked percentage revenue contribution.
    This automatically uses a 12 month period by default, but can be modified for other periods to suit.

    Args:

        customers (object): Pandas DataFrame from get_customers()
        months (int, optional): Number of months to use for ABC analysis (12 by default)
        abc_class_name (str, optional): Name to assign to ABC class string (abc_class_12m by default)
        abc_rank_name (str, optional): Name to assign to ABC rank string (abc_rank_12m by default)

    Returns:
        abc: Pandas DataFrame
    """

    # Calculate data for customers who purchased within the specified period
    purchased = customers[customers['recency'] <= (months * 30)]
    purchased = purchased.sort_values(by='revenue', ascending=False)
    purchased['revenue_cumsum'] = purchased['revenue'].cumsum()
    purchased['revenue_total'] = purchased['revenue'].sum()
    purchased['revenue_running_percentage'] = (purchased['revenue_cumsum'] / purchased['revenue_total']) * 100
    purchased[abc_class_name] = purchased['revenue_running_percentage'].apply(_abc_classify_customer)
    purchased[abc_rank_name] = purchased['revenue_running_percentage'].rank().astype(int)
    purchased.drop(['revenue_cumsum', 'revenue_total', 'revenue_running_percentage'], axis=1, inplace=True)

    # Assign lapsed customers to class D
    lapsed = customers[customers['recency'] > (months * 30)]

    # Return ABC segments
    abc = purchased.append(lapsed)
    abc[abc_class_name].fillna('D', inplace=True)
    abc[abc_rank_name].fillna(len(purchased) + 1, inplace=True)
    abc = abc[['customer_id', abc_class_name, abc_rank_name]]
    return abc


def get_cohorts(df, period='M'):
    """Return a customer cohort matrix from a dataframe of transactional items.

    Given a Pandas DataFrame of transactional items, this function returns
    a Pandas DataFrame containing the acquisition cohort and order cohort which
    can be used for customer analysis or the creation of a cohort analysis matrix.

    Args:
        df (object): Pandas DataFrame. Required columns: order_id, customer_id, order_date.
        period (str, optional): Period value - M, Q, or Y. Create cohorts using month, quarter, or year of acquisition.

    Returns:
        df (object): Pandas DataFrame
    """

    df = df[['customer_id', 'order_id', 'order_date']].drop_duplicates()
    df = df.assign(acquisition_cohort=df.groupby('customer_id') \
        ['order_date'].transform('min').dt.to_period(period))
    df = df.assign(order_cohort=df['order_date'].dt.to_period(period))
    return df


def get_retention(df, period='M'):
    """Calculate the retention of customers in each month after their acquisition.

    Args:
        df (object): Pandas DataFrame. Required columns: order_id, customer_id, order_date.
        period (str, optional): Period value - M, Q, or Y. Create cohorts using month, quarter, or year of acquisition.

    Returns:
    -------
        df (object): Pandas DataFrame
    """

    df = get_cohorts(df, period).groupby(['acquisition_cohort', 'order_cohort']) \
        .agg(customers=('customer_id', 'nunique')) \
        .reset_index(drop=False)
    df['periods'] = (df.order_cohort - df.acquisition_cohort) \
        .apply(op.attrgetter('n'))

    return df


def get_cohort_matrix(df, period='M', percentage=False):
    """Return a cohort matrix showing the number of customers who purchased in each period after their acquisition.

    Args:
        df (object): Pandas DataFrame. Required columns: order_id, customer_id, order_date.
        period (str, optional): Period value - M, Q, or Y. Create cohorts using month, quarter, or year of acquisition.
        percentage (bool, optional): True or False. Return raw numbers or a percentage retention.

    Returns:
        df (object): Pandas DataFrame
    """

    df = get_retention(df, period).pivot_table(index='acquisition_cohort',
                                               columns='periods',
                                               values='customers')

    if percentage:
        df = df.divide(df.iloc[:, 0], axis=0)

    return df
