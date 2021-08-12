"""
A very primitive and slow web scraper for SEO tasks on small websites
"""

import requests
import urllib.parse
import pandas as pd
from requests_html import HTMLSession


def _get_source(url: str):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def _get_title(response):
    """Parse HTML and extract the title

    :param response: HTML response from Requests-HTML
    :return: HTML element as text
    """

    try:
        return response.html.find('title', first=True).text
    except Exception as e:
        return


def _get_description(response):
    """Parse HTML and extract the title

    :param response: HTML response from Requests-HTML
    :return: HTML element as text
    """

    try:
        return response.html.xpath('//meta[@name="description"]/@content')[0]
    except Exception as e:
        return


def scrape_site(df, url='loc', verbose=False):
    """Scrapes every page in a Pandas dataframe column.

    Args:
        df: Pandas dataframe containing the URL list.
        url (optional, string): Optional name of URL column, if not 'url'
        verbose (optional, boolean, default = False): Set to False to hide progress updates

    Returns:
        df: Pandas dataframe containing all scraped content.

    """

    if verbose:
        pages = len(df)
        minutes = pages / 60

        print('Preparing to scrape ' + str(pages) + ' pages. This will take approximately ' + str(round(minutes)) + ' minutes')

    df_pages = pd.DataFrame(columns=['url', 'title', 'description'])

    for index, row in df.iterrows():

        if verbose:
            print('Scraping: ' + row[url])

        response = _get_source(row[url])

        if response:
            with response as r:
                row = {
                    'url': row[url],
                    'title': _get_title(r),
                    'description': _get_description(r),
                }

                df_pages = df_pages.append(row, ignore_index=True)

    return df_pages

