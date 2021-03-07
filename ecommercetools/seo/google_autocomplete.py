"""
Get keyword suggestions for a term using Google Autocomplete or Google Suggest.
"""

import requests
import urllib.parse
import json
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


def _get_results(query: str):
    """Get the JSON data from a Google Autocomplete query.

    Args:
        query (string): Query term, i.e. data science

    Returns:
        results (dict): JSON results.
    """

    query = urllib.parse.quote_plus(query)
    response = _get_source("https://suggestqueries.google.com/complete/search?output=chrome&hl=en&q=" + query)
    results = json.loads(response.text)
    return results


def _format_results(results: dict):
    """Return formatted dictionary containing term and relevance.

    Args:
        results (dict): JSON dictionary of Google Autocomplete results.

    Returns:
        suggestions (dict): Formatted dictionary containing term and relevance.
    """

    if results:
        suggestions = []
        for index, value in enumerate(results[1]):
            suggestion = {'term': value, 'relevance': results[4]['google:suggestrelevance'][index]}
            suggestions.append(suggestion)
        return suggestions


def _get_suggestions(query: str):
    """Return results sorted by relevance.

    Args:
        query (string): Search term, i.e. data science

    Returns:
        results (dict): Sorted dictionary containing term and relevance.
    """

    results = _get_results(query)
    results = _format_results(results)
    results = sorted(results, key=lambda k: k['relevance'], reverse=True)
    return results


def _get_expanded_term_suffixes():
    """Return a list of query suffixes to extend Google Autocomplete results.

    Returns:
        expanded_term_suffixes (list)
    """

    expanded_term_suffixes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    return expanded_term_suffixes


def _get_expanded_term_prefixes():
    """Return a list of query prefixes to extend Google Autocomplete results.

    Returns:
        expanded_term_prefixes (list)
    """

    expanded_term_prefixes = ['who is *', 'what is *', 'where is *', 'when can *', 'why is *',
                              'how to *', 'best', 'cheap', 'worst', 'is', 'what', 'when', 'why',
                              'how', 'who']
    return expanded_term_prefixes


def _get_expanded_terms(query: str):
    """Return a list of expanded terms, comprising the original query, and the prefixed and suffixed queries.

    Args:
        query (string): Query term, i.e. data science

    Returns:
        terms (list): List of query terms with suffixes and prefixes.
    """

    expanded_term_prefixes = _get_expanded_term_prefixes()
    expanded_term_suffixes = _get_expanded_term_suffixes()

    terms = [query]

    for term in expanded_term_prefixes:
        terms.append(term + ' ' + query)

    for term in expanded_term_suffixes:
        terms.append(query + ' ' + term)

    return terms


def _get_expanded_suggestions(query: str):
    """Return the Google Autocomplete suggestions for a query and its prefixed and suffixed versions.

    Args:
        query (string): Query term, i.e. data science

    Returns:
        all_results (dict): Sorted formatted dictionary of results for each search term.
    """

    all_results = []

    expanded_terms = _get_expanded_terms(query)
    for term in expanded_terms:
        results = _get_results(term)
        results = _format_results(results)
        all_results = all_results + results
        all_results = sorted(all_results, key=lambda k: k['relevance'], reverse=True)
    return all_results


def google_autocomplete(query: str, include_expanded=True):
    """Run a Google Autocomplete / Google Suggest search with optional query expansion.

    Args:
        query (string): Query term, i.e. data science
        include_expanded (bool, optional): Optional boolean flag. Set to true to add prefixes/suffixes.

    Returns:
        df (dataframe): Pandas dataframe containing results.
    """

    if include_expanded:
        results = _get_expanded_suggestions(query)

    else:
        results = _get_suggestions(query)

    df = pd.DataFrame.from_records(results)
    return df

