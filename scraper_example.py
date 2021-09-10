import pandas as pd
from ecommercetools import seo

# Fetch the sitemap to obtain a URL list to scrape
df_sitemap = seo.get_sitemap("https://www.practicaldatascience.co.uk/sitemap.xml")

# Scrape the list of URLs
df_pages = seo.scrape_site(df_sitemap.head(), url='loc', verbose=True)

print(df_pages)
