# EcommerceTools

![EcommerceTools](https://github.com/practical-data-science/ecommercetools/blob/master/banner.png?raw=true)

EcommerceTools is a data science toolkit for those working in technical ecommerce, marketing science, and technical seo and includes a wide range of features to aid analysis and model building. 

The package is written in Python and is designed to be used with Pandas and works within a Jupyter notebook environment or in standalone Python projects. 

#### Installation

You can install EcommerceTools and its dependencies via PyPi by entering `pip3 install ecommercetools` in your terminal. 

---

### SEO

#### 1. Discover XML sitemap locations
The `get_sitemaps()` function takes the location of a `robots.txt` file (always stored at the root of a domain), and returns the URLs of any XML sitemaps listed within. 

```python
from ecommercetools import seo

sitemaps = seo.get_sitemaps("http://www.flyandlure.org/robots.txt")
print(sitemaps)

```

#### 2. Get an XML sitemap
The `get_dataframe()` function allows you to download the URLs in an XML sitemap to a Pandas dataframe. If the sitemap contains child sitemaps, each of these will be retrieved. You can save the Pandas dataframe to CSV in the usual way. 

```python
from ecommercetools import seo

df = seo.get_sitemap("http://flyandlure.org/sitemap.xml")
print(df.head())
```

##### 3. Get Core Web Vitals from PageSpeed Insights
The `get_core_web_vitals()` function retrieves the Core Web Vitals metrics for a list of sites from the Google PageSpeed Insights API and returns results in a Pandas dataframe. The function requires a a Google PageSpeed Insights API key. 

```python
from ecommercetools import seo

pagespeed_insights_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
urls = ['https://www.bbc.co.uk', 'https://www.bbc.co.uk/iplayer']
df = seo.get_core_web_vitals(pagespeed_insights_key, urls)
print(df.head())
```

#### 4. Get Google Knowledge Graph data
The `get_knowledge_graph()` function returns the Google Knowledge Graph data for a given search term. This requires the use of a Google Knowledge Graph API key. By default, the function returns output in a Pandas dataframe, but you can pass the `output="json"` argument if you wish to receive the JSON data back. 

```python
from ecommercetools import seo

knowledge_graph_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
knowledge_graph = seo.get_knowledge_graph(knowledge_graph_key, "tesla", output="dataframe")
print(knowledge_graph)
```

#### 5. Get Google Search Console API data
The `query_google_search_console()` function runs a search query on the Google Search Console API and returns data in a Pandas dataframe. This function requires a JSON client secrets key with access to the Google Search Console API. 

```python
from ecommercetools import seo

key = "google-search-console.json"
site_url = "http://flyandlure.org"
payload = {
    'startDate': "2019-01-01",
    'endDate': "2019-12-31",
    'dimensions': ["page", "device", "query"],
    'rowLimit': 100,
    'startRow': 0
}

df = seo.query_google_search_console(key, site_url, payload)
print(df.head())

```

#### 6. Get the number of "indexed" pages
The `get_indexed_pages()` function uses the "site:" prefix to search Google for the number of pages "indexed". This is very approximate and may not be a perfect representation, but it's usually a good guide of site "size" in the absence of other data. 

```python
from ecommercetools import seo

urls = ['https://www.bbc.co.uk', 'https://www.bbc.co.uk/iplayer', 'http://flyandlure.org']
df = seo.get_indexed_pages(urls)
print(df.head())
```

##### 7. Get keyword suggestions from Google Autocomplete
The `google_autocomplete()` function returns a set of keyword suggestions from Google Autocomplete. The `include_expanded=True` argument allows you to expand the number of suggestions shown by appending prefixes and suffixes to the search terms. 

```python
from ecommercetools import seo

suggestions = seo.google_autocomplete("data science", include_expanded=False)
print(suggestions)

suggestions = seo.google_autocomplete("data science", include_expanded=True)
print(suggestions)
```

#### 8. Retrieve robots.txt content
The `get_robots()` function returns the contents of a robots.txt file in a Pandas dataframe so it can be parsed and analysed. 

```python
from ecommercetools import seo

robots = seo.get_robots("http://www.flyandlure.org/robots.txt")
print(robots)
```

#### 9. Get Google SERPs
The `get_serps()` function returns a Pandas dataframe containing the Google search engine results for a given search term. Note that this function is not suitable for large-scale scraping and currently includes no features to prevent it from being blocked.

```python
from ecommercetools import seo

serps = seo.get_serps("fly fishing blog")
print(serps)
```

---

### Ecommerce

#### Create a transaction items dataframe

The `utilities` module includes a range of tools that allow you to format data so it can be used within other EcommerceTools functions. The `load_data()` function is used to create a Pandas dataframe of formatted transactional item data. 

```python
import pandas as pd
from ecommercetools import utilities

transaction_items = utilities.load_data('transaction_items_non_standard_names.csv',
                                 date_column='InvoiceDate',
                                 order_id_column='InvoiceNo',
                                 customer_id_column='CustomerID',
                                 sku_column='StockCode',
                                 quantity_column='Quantity',
                                 unit_price_column='UnitPrice'
                                 )
transaction_items.to_csv('transaction_items.csv', index=False)
print(transaction_items.head())
```

#### Create a transactions dataframe

The `get_transactions()` function takes the formatted Pandas dataframe of transaction items and returns a Pandas dataframe of aggregated transaction data, which includes features identifying the order number. 

```python
import pandas as pd
from ecommercetools import customers

transaction_items = pd.read_csv('transaction_items.csv')
transactions = customers.get_transactions(transaction_items)
transactions.to_csv('transactions.csv', index=False)
print(transactions.head())
```

#### Create a customers dataframe

