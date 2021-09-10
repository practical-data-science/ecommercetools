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

    Args:
        response: HTML response from Requests-HTML
    Returns:
        HTML element
    """

    try:
        return response.html.find('title', first=True).text
    except Exception as e:
        return


def _get_description(response):
    """Parse HTML and extract the meta description

    Args:
        response: HTML response from Requests-HTML
    Returns:
        HTML element
    """

    try:
        return response.html.xpath('//meta[@name="description"]/@content')[0]
    except Exception as e:
        return


def _get_canonical(response):
    """Parse HTML and extract the canonical
    :param response: HTML response from Requests-HTML
    :return: HTML element
    """

    try:
        return response.html.xpath("//link[@rel='canonical']/@href")
    except Exception as e:
        return


def _get_robots(response):
    """Parse HTML and extract the meta robots
    :param response: HTML response from Requests-HTML
    :return: HTML element
    """

    try:
        return response.html.xpath("//meta[@name='robots']/@content")
    except Exception as e:
        return


def _get_generator(response):
    """Parse HTML and extract the generator
    :param response: HTML response from Requests-HTML
    :return: HTML element
    """

    try:
        return response.html.xpath("//meta[@name='generator']/@content")
    except Exception as e:
        return


def _get_hreflang(response):
    """Parse HTML and extract the hreflang
    :param response: HTML response from Requests-HTML
    :return: HTML element
    """

    try:
        return response.html.xpath("//link[@rel='alternate']/@hreflang")
    except Exception as e:
        return


def _get_absolute_links(response):
    """Parse HTML and extract the absolute URLs
    :param response: HTML response from Requests-HTML
    :return: HTML element as text
    """

    try:
        return response.html.absolute_links
    except Exception as e:
        return


def _get_paragraphs(response):
    """Parse HTML and extract paragraphs

    Args:
        response: HTML response from Requests-HTML
    Returns:
        HTML element
    """

    try:
        paragraphs = []
        for paragraph in response.html.find('p'):
            paragraphs.append(paragraph.text)
        return paragraphs
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

    df_pages = pd.DataFrame(columns=['url', 'title', 'description', 'canonical', 'robots', 'hreflang', 'generator',
                                     'absolute_links', 'paragraphs'])

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
                    'canonical': _get_canonical(r),
                    'robots': _get_robots(r),
                    'hreflang': _get_hreflang(r),
                    'generator': _get_generator(r),
                    'absolute_links': _get_absolute_links(r),
                    'paragraphs': _get_paragraphs(r),
                }

                df_pages = df_pages.append(row, ignore_index=True)

    return df_pages

