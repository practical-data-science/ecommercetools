import re
import random
import itertools
import pandas as pd


def _match_type_exact(keywords):
    exact = []
    for keyword in keywords:
        exact.append([keyword[0], '[' + keyword[1] + ']'])

    df = pd.DataFrame.from_records(exact, columns=['product', 'keywords'])
    df['match_type'] = 'Exact'

    return df


def _match_type_phrase(keywords):
    phrase = []
    for keyword in keywords:
        phrase.append([keyword[0], '"' + keyword[1] + '"'])

    df = pd.DataFrame.from_records(phrase, columns=['product', 'keywords'])
    df['match_type'] = 'Phrase'

    return df


def _match_type_broad(keywords):
    broad = []
    for keyword in keywords:
        broad.append([keyword[0], keyword[1]])

    df = pd.DataFrame.from_records(broad, columns=['product', 'keywords'])
    df['match_type'] = 'Broad'

    return df


def _match_type_broad_modified(keywords):
    broad_modified = []
    for keyword in keywords:
        bmm = ['+' + keyword[1].replace(' ', ' +')]
        broad_modified.append([keyword[0], bmm])

    df = pd.DataFrame.from_records(broad_modified, columns=['product', 'keywords'])
    df['match_type'] = 'Modified'

    return df


def _generate_combinations(products,
                           keywords_prepend,
                           keywords_append):
    """Return a list of all prepended and appended keywords combinations.

    Args:
        products (list): List of product names.
        keywords_prepend (list): List of keywords to prepend to product names.
        keywords_append (list): List of keywords to append to product names.

    Returns:
        keywords (list): List of lists containing the product name and keyword combination.

    Example:
        [['fly rods', 'fly rods'],
        ['fly rods', 'buy fly rods'],
        ['fly rods', 'best fly rods']]
    """

    keywords = []

    for product in products:
        keywords.append([product, product])

        for keyword_prepend in keywords_prepend:
            keywords.append([product, keyword_prepend + ' ' + product])

        for keyword_append in keywords_append:
            keywords.append([product, product + ' ' + keyword_append])

    return keywords


def generate_ad_keywords(products,
                         keywords_prepend,
                         keywords_append,
                         campaign_name):
    """Return a Pandas dataframe of keywords data for use in Google Adwords.

    Args:
        products (list): List of product names.
        keywords_prepend (list): List of keywords to prepend to product names.
        keywords_append (list): List of keywords to append to product names.
        campaign_name (str): Name of paid search campaign.

    Returns:
        df (object): Pandas dataframe containing generated data.
    """

    keywords = _generate_combinations(products, keywords_prepend, keywords_append)

    exact = _match_type_exact(keywords)
    phrase = _match_type_phrase(keywords)
    broad = _match_type_broad(keywords)
    broad_modified = _match_type_broad_modified(keywords)

    df = pd.concat([exact, phrase, broad, broad_modified])
    df['campaign_name'] = campaign_name
    return df


def generate_spintax(text, single=True):
    """Return a list of unique spins of a Spintax text string.

    Args:
        text (string): Spintax text (i.e. I am the {President|King|Ambassador} of Nigeria.)
        single (bool, optional): Optional boolean to return a list or a single spin.

    Returns:
        spins (string, list): Single spin or list of spins depending on single.
    """

    pattern = re.compile('({[^}]+}|[^{}]*)')
    chunks = pattern.split(text)

    def options(s):
        if len(s) > 0 and s[0] == '{':
            return [opt for opt in s[1:-1].split('|')]
        return [s]

    parts_list = [options(chunk) for chunk in chunks]

    spins = []

    for spin in itertools.product(*parts_list):
        spins.append(''.join(spin))

    if single:
        return spins[random.randint(0, len(spins) - 1)]
    else:
        return spins

