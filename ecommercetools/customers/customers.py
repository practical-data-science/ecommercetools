import pandas as pd
import numpy as np
import operator as op
from ecommercetools.transactions import transactions
from ecommercetools import utilities
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from lifetimes import GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes import BetaGeoFitter


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


def _days_to_next_order(avg_latency, std_latency, recency):
    """Estimate the number of days to a customer's next order using latency.

    Args:
        avg_latency (float): Average latency in days
        std_latency (float): Standard deviation of latency in days
        recency (float): Recency in days
    Returns:
        Approximate number of days until the next order.
    """

    return avg_latency - (recency - std_latency)


def _latency_label_customers(avg_latency, std_latency, recency):
    """Add a label to describe a customer's latency metric.

    Args:
        avg_latency (float): Average latency in days
        std_latency (float): Standard deviation of latency in days
        recency (float): Recency in days
    Returns:
           Label describing the latency metric in relation to the customer.
    """

    days_to_next_order_upper = avg_latency - (recency - std_latency)
    days_to_next_order_lower = avg_latency - (recency + std_latency)

    if recency < days_to_next_order_lower:
        return 'Order not due'

    elif (recency <= days_to_next_order_lower) or (recency <= days_to_next_order_upper):
        return 'Order due soon'

    elif recency > days_to_next_order_upper:
        return 'Order overdue'

    else:
        return 'Not sure'


def get_latency(df_transactions):
    """Return a Pandas dataframe containing latency metrics for each customer.

    Args:
        df_transactions: Pandas dataframe from get_transactions().

    Returns:
        Pandas dataframe of customer purchase latency metrics.
    """

    # Create latency dataframe and calculate granular metrics
    df_latency = df_transactions[['order_id', 'customer_id', 'order_date', 'revenue']]
    df_latency = df_latency[df_latency['revenue'] > 0]
    df_latency = df_latency.sort_values(by=['order_date'], ascending=False)
    df_latency['prev_order_date'] = utilities.get_previous_value(df_latency, 'customer_id', 'order_date')
    df_latency['days_since_prev_order'] = utilities.get_days_since_date(df_latency, 'prev_order_date', 'order_date')
    df_latency['order_number'] = utilities.get_cumulative_count(df_latency, 'customer_id', 'order_id', 'order_date')

    # Create customer dataframe and calculate aggregate metrics
    df_customers = pd.DataFrame(df_latency['customer_id'].unique())
    df_customers.columns = ['customer_id']

    # Calculate frequency
    df_frequency = df_latency.groupby('customer_id')['order_id'].nunique().reset_index()
    df_frequency.columns = ['customer_id', 'frequency']
    df_customers = df_customers.merge(df_frequency, on='customer_id')

    # Calculate recency
    df_recency = df_latency.groupby('customer_id')['order_date'].max().reset_index()
    df_recency.columns = ['customer_id', 'recency_date']
    df_customers = df_customers.merge(df_recency, on='customer_id')
    df_customers['recency'] = round((pd.to_datetime('today') - df_customers['recency_date']) \
                                    / np.timedelta64(1, 'D')).astype(int)

    # Calculate average latency
    df_avg_latency = df_latency.groupby('customer_id')['days_since_prev_order'].mean().astype(int).reset_index()
    df_avg_latency.columns = ['customer_id', 'avg_latency']
    df_customers = df_customers.merge(df_avg_latency, on='customer_id')

    # Calculate standard deviation of latency for returning customers
    df_latency_returning = df_latency[df_latency['order_number'] > 0]

    # Min latency
    df_min = df_latency_returning.groupby('customer_id')['days_since_prev_order'].min().astype(int).reset_index()
    df_min.columns = ['customer_id', 'min_latency']
    df_customers = df_customers.merge(df_min, on='customer_id')

    # Max latency
    df_max = df_latency_returning.groupby('customer_id')['days_since_prev_order'].max().astype(int).reset_index()
    df_max.columns = ['customer_id', 'max_latency']
    df_customers = df_customers.merge(df_max, on='customer_id')

    # STD latency
    df_std = df_latency_returning.groupby('customer_id')['days_since_prev_order'].std().reset_index()
    df_std.columns = ['customer_id', 'std_latency']
    df_customers = df_customers.merge(df_std, on='customer_id')

    # Coefficient of Variation of latency
    df_customers['cv'] = df_customers['std_latency'] / df_customers['avg_latency']

    # Calculate approximate days to next order
    df_customers['days_to_next_order'] = df_customers.apply(
        lambda x: _days_to_next_order(x['avg_latency'], x['std_latency'], x['recency']), axis=1).round()

    # Label latency
    df_customers['label'] = df_customers.apply(
        lambda x: _latency_label_customers(x['avg_latency'], x['std_latency'], x['recency']), axis=1)

    return df_customers


def _get_lifetimes_rfmt(df_transactions, observation_period_end):
    """Return the RFMT data from the Lifetimes model.

    Args:
        df_transactions (df): Pandas dataframe of transactions from get_transactions()
        observation_period_end (string): Date string in YYYY-MM-DD format representing end of observation period.

    Returns:
        df: Pandas dataframe containing frequency, recency, T, monetary_value per customer.
    """

    df_transactions = df_transactions[df_transactions['replacement'] == 0]

    df = summary_data_from_transaction_data(df_transactions,
                                            'customer_id',
                                            'order_date',
                                            'revenue',
                                            observation_period_end=observation_period_end)
    return df


def _get_predicted_purchases(df_transactions,
                             observation_period_end,
                             days=90):
    """Return the number of predicted purchases per customer from the Lifetimes BG/NBD model.

    Args:
        df_transactions (df): Pandas dataframe of transactions from get_transactions()
        observation_period_end (string): Date string in YYYY-MM-DD format representing end of observation period.

    Returns:
        df: Pandas dataframe containing frequency, recency, T, monetary_value per customer, and predicted purchases.
    """

    df = _get_lifetimes_rfmt(df_transactions, observation_period_end)
    bgf = BetaGeoFitter(penalizer_coef=0)
    bgf.fit(df['frequency'], df['recency'], df['T'])
    df['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(days,
                                                                                        df['frequency'],
                                                                                        df['recency'],
                                                                                        df['T'])
    return df


def _get_predicted_aov(df_transactions,
                       observation_period_end,
                       ggf_penalizer_coef=0):
    """Returns the predicted AOV for each customer via the Gamma-Gamma model.
    This function uses models from the Lifetimes package.

    Args:
        df_transactions (df): Pandas dataframe of transactions from get_transactions()
        observation_period_end (string): Date string in YYYY-MM-DD format for end of observation period.
        ggf_penalizer_coef (float, optional): Penalizer coefficient for Gamma-Gamma model. See Lifetimes.

    Returns:
        Predicted AOV for each customer.
    """

    df_rfmt = _get_lifetimes_rfmt(df_transactions, observation_period_end)

    df_returning = df_rfmt[df_rfmt['frequency'] > 0]
    df_returning = df_rfmt[df_rfmt['monetary_value'] > 0]

    ggf = GammaGammaFitter(penalizer_coef=ggf_penalizer_coef)
    ggf.fit(df_returning['frequency'],
            df_returning['monetary_value'])

    predicted_monetary = ggf.conditional_expected_average_profit(
        df_returning['frequency'],
        df_returning['monetary_value']
    )

    aov_df = pd.DataFrame(predicted_monetary, columns=['aov'])

    return aov_df


def _get_predicted_clv(df_transactions,
                       observation_period_end,
                       months=12,
                       discount_rate=0.01,
                       ggf_penalizer_coef=0,
                       bgf_penalizer_coef=0):
    """Return the predicted CLV for each customer using the Gamma-Gamma and BG/NBD models.
    This function uses models from the Lifetimes package.

    Args:
        df_transactions (df): Pandas dataframe of transactions from get_transactions()
        observation_period_end (string): Date string in YYYY-MM-DD format for end of observation period.
        months (int, optional): Optional number of months in CLV prediction window.
        discount_rate (float, optional): Discount rate. See Lifetimes.
        ggf_penalizer_coef (float, optional): Penalizer coefficient for Gamma-Gamma model. See Lifetimes.
        bgf_penalizer_coef (float, optional): Penalizer coefficient for BG/NBD model. See Lifetimes.

    Returns:
        Predicted CLV for each customer.
    """

    df_rfmt = _get_lifetimes_rfmt(df_transactions, observation_period_end)
    df_returning = df_rfmt[df_rfmt['frequency'] > 0]
    df_returning = df_rfmt[df_rfmt['monetary_value'] > 0]

    ggf = GammaGammaFitter(penalizer_coef=ggf_penalizer_coef)
    ggf.fit(df_returning['frequency'],
            df_returning['monetary_value'])

    bgf = BetaGeoFitter(penalizer_coef=bgf_penalizer_coef)
    bgf.fit(df_returning['frequency'],
            df_returning['recency'],
            df_returning['T'])

    preds = ggf.customer_lifetime_value(
        bgf,
        df_returning['frequency'],
        df_returning['recency'],
        df_returning['T'],
        df_returning['monetary_value'],
        time=months,
        discount_rate=discount_rate
    ).to_frame().reset_index()

    return preds


def get_customer_predictions(df_transactions,
                             observation_period_end,
                             days=90,
                             months=3,
                             discount_rate=0.01,
                             ggf_penalizer_coef=0,
                             bgf_penalizer_coef=0):
    """Get predicted customer purchased, AOV, and CLV for the defined period.

    This uses the Lifetimes package to run the Gamma-Gamma, and BG/NBD models
    and predict the AOV, CLV, and number of purchases each customer will make.
    These models use a different approach to measuring RFMT than the other
    functions in EcommerceTools, so are not directly comparable, so the results
    have been removed from the output.

    Args:
        df_transactions (df): Pandas dataframe of transactions from get_transactions()
        observation_period_end (string): Date string in YYYY-MM-DD format for end of observation period.
        days (int, optional): Optional number of days in purchase prediction window.
        months (int, optional): Optional number of months in CLV prediction window.
        discount_rate (float, optional): Discount rate. See Lifetimes.
        ggf_penalizer_coef (float, optional): Penalizer coefficient for Gamma-Gamma model. See Lifetimes.
        bgf_penalizer_coef (float, optional): Penalizer coefficient for BG/NBD model. See Lifetimes.

    Returns:
        df_predictions: Pandas dataframe containing predictions from Gamma-Gamma and BG/NBD models.
    """

    df_predicted_purchases = _get_predicted_purchases(df_transactions,
                                                      observation_period_end,
                                                      days=days)
    df_aov = _get_predicted_aov(df_transactions,
                                observation_period_end)

    df_clv = _get_predicted_clv(df_transactions,
                                observation_period_end,
                                months=months,
                                discount_rate=discount_rate,
                                bgf_penalizer_coef=bgf_penalizer_coef,
                                ggf_penalizer_coef=ggf_penalizer_coef
                                )

    df_predictions = df_predicted_purchases.merge(df_aov, on='customer_id', how='left')
    df_predictions = df_predictions.merge(df_clv, on='customer_id', how='left')

    return df_predictions[['customer_id', 'predicted_purchases', 'aov', 'clv']]

