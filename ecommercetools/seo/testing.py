"""
Functions for running simple before and after tests using Causal Impact.
"""

from datetime import timedelta
import pandas as pd
from causalimpact import CausalImpact
from ecommercetools import seo
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def _subtract_days_from_date(date, days):
    """Subtract days from a date and return the date.

    Args:
        date (string): Date string in YYYY-MM-DD format.
        days (int): Number of days to subtract from date

    Returns:
        date (date): Date in YYYY-MM-DD with X days subtracted.
    """

    subtracted_date = pd.to_datetime(date) - timedelta(days=days)
    subtracted_date = subtracted_date.strftime("%Y-%m-%d")

    return subtracted_date


def _add_days_to_date(date, days):
    """Add days to a date and return the date.

    Args:
        date (string): Date string in YYYY-MM-DD format.
        days (int): Number of days to add to date

    Returns:
        date (date): Date in YYYY-MM-DD with X days added.
    """

    added_date = pd.to_datetime(date) + timedelta(days=days)
    added_date = added_date.strftime("%Y-%m-%d")

    return added_date


def _get_pre_and_post_periods(post_period_start_date, days):
    """Return the pre- and post-period dates for use in CausalImpact.

    If you provide the start date for the test period, i.e. 2021-07-18, and
    the test duration in days, i.e. 14, this function will return the start
    and end date for the test period, and the start and end date for the
    pre-intervention period that ran immediately before. Data are returned
    in the right format for use by the CausalImpact model.

    Args:
        post_period_start_date (string): The date at which the test was started in YYYY-MM-DD format.
        days (int): The number of days to use for the test period.

    Returns:
        pre_period (list): The start and end date for the period before the test.
        post_period (list): The start and end date for the test period.

    Example:
        pre_period, post_period = get_pre_and_post_periods('2021-07-18', 14)

        pre_period
            ['2021-07-04', '2021-07-17']

        post_period
            ['2021-07-18', '2021-07-31']
    """

    pre_period_start_date = _subtract_days_from_date(post_period_start_date, 14)
    pre_period_end_date = _subtract_days_from_date(post_period_start_date, 1)
    post_period_end_date = _add_days_to_date(post_period_start_date, 13)

    pre_period = [pre_period_start_date, pre_period_end_date]
    post_period = [post_period_start_date, post_period_end_date]

    return pre_period, post_period


def _get_seo_test_data(key, site_url, post_period_start_date, days, filters=None):
    """Return Google Search Console data for use within a Causal Impact SEO test.

    Args:
        key (string): Filepath of Google Search Console API client secrets JSON keyfile
        site_url (string): Google Search Console property URL to query
        post_period_start_date (string): Start date for test in YYYY-MM-DD format
        days (int): Number of days to include in test period
        filters (optional, list): Optional list of GSC formatted query filters.

    Returns:
        df (dataframe): Date indexed dataframe containing clicks, impressions, ctr, and position

    Usage:
        # Site level test
        df = _get_seo_test_data('client_secrets.json',
                                    'https://example.com',
                                    '2021-07-17',
                                    14)

        # Page level test
        filters = [{
            'filters':[{
                'dimension':'page',
                'expression': 'https://example.com/hello'
            }]
        }]

        df = _get_seo_test_data('client_secrets.json',
                                    'https://example.com',
                                    '2021-07-17',
                                    14,
                                    filters)

        # Query level test
        filters = [{
            'filters':[{
                'dimension':'query',
                'expression': 'marketing'
            }]
        }]

        df = _get_seo_test_data('client_secrets.json',
                                    'https://example.com',
                                    '2021-07-17',
                                    14,
                                    filters)
    """

    # Get the dates of the pre- and post-periods
    pre_period, post_period = _get_pre_and_post_periods(post_period_start_date, days)

    # Create basic payload
    payload = {
        'startDate': pre_period[0],
        'endDate': post_period[1],
        'dimensions': ['date'],
        'rowLimit': 10000,
        'startRow': 0,
    }

    # Add filters to the payload if provided
    if filters:
        payload['dimensionFilterGroups'] = filters

    # Run Google Search Console query using payload
    df = seo.query_google_search_console(key, site_url, payload)
    df.sort_values(by='date', ascending=True).head()
    df = df.set_index('date')

    print(df.head())

    return df


def seo_test(key,
             site_url,
             post_period_start_date,
             days,
             filters=None,
             metric='clicks'):
    """Run a simple marketing or SEO test using CausalImpact.

    Args:
        key (string): Filepath of Google Search Console API client secrets JSON keyfile
        site_url (string): Google Search Console property URL to query
        post_period_start_date (string): Start date for test in YYYY-MM-DD format
        days (int): Number of days to include in test period
        filters (optional, list): Optional list of GSC formatted query filters.
        metric (optional): Select a specific metric to examine. Default is clicks.

    Returns:
        model (object): Returns a Causal Impact model object.

    """

    # Get the SEO test data
    df = _get_seo_test_data(key, site_url, post_period_start_date, days, filters)

    # Get the dates of the pre- and post-periods
    pre_period, post_period = _get_pre_and_post_periods(post_period_start_date, days)

    print(pre_period)
    print(post_period)

    # Fit the test model
    model = CausalImpact(df[metric], pre_period, post_period)

    return model

