# EcommerceTools

![EcommerceTools](https://github.com/practical-data-science/ecommercetools/blob/master/banner.png?raw=true)

EcommerceTools is a data science toolkit for those working in technical ecommerce, marketing science, and technical seo and includes a wide range of features to aid analysis and model building. The package is written in Python and is designed to be used with Pandas and works within a Jupyter notebook environment or in standalone Python projects. 

#### Installation

You can install EcommerceTools and its dependencies via PyPi by entering `pip3 install ecommercetools` in your terminal, or `!pip3 install ecommercetools` within a Jupyter notebook cell. 

---

### Modules

- [Transactions](#Transactions)
- [Products](#Products)
- [Customers](#Customers)
- [Advertising](#Advertising)
- [Operations](#Operations)
- [Marketing](#Marketing)
- [NLP](#NLP)
- [SEO](#SEO)
- [Reports](#Reports)
---

### Transactions

1. #### Load sample transaction items data

If you want to get started with the transactions, products, and customers features, you can use the `load_sample_data()` function to load a set of real world data. This imports the transaction items from widely-used Online Retail dataset and reformats it ready for use by EcommerceTools. 

```python
from ecommercetools import utilities

transaction_items = utilities.load_sample_data()
transaction_items.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>order_id</th>
      <th>sku</th>
      <th>description</th>
      <th>quantity</th>
      <th>order_date</th>
      <th>unit_price</th>
      <th>customer_id</th>
      <th>country</th>
      <th>line_price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>536365</td>
      <td>85123A</td>
      <td>WHITE HANGING HEART T-LIGHT HOLDER</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>2.55</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>15.30</td>
    </tr>
    <tr>
      <th>1</th>
      <td>536365</td>
      <td>71053</td>
      <td>WHITE METAL LANTERN</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>3.39</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>20.34</td>
    </tr>
    <tr>
      <th>2</th>
      <td>536365</td>
      <td>84406B</td>
      <td>CREAM CUPID HEARTS COAT HANGER</td>
      <td>8</td>
      <td>2010-12-01 08:26:00</td>
      <td>2.75</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>22.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>536365</td>
      <td>84029G</td>
      <td>KNITTED UNION FLAG HOT WATER BOTTLE</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>3.39</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>20.34</td>
    </tr>
    <tr>
      <th>4</th>
      <td>536365</td>
      <td>84029E</td>
      <td>RED WOOLLY HOTTIE WHITE HEART.</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>3.39</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>20.34</td>
    </tr>
  </tbody>
</table>

2. #### Create a transaction items dataframe

The `utilities` module includes a range of tools that allow you to format data, so it can be used within other EcommerceTools functions. The `load_data()` function is used to create a Pandas dataframe of formatted transactional item data. When loading your transaction items data, all you need to do is define the column mappings, and the function will reformat the dataframe accordingly. 

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

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>order_id</th>
      <th>sku</th>
      <th>description</th>
      <th>quantity</th>
      <th>order_date</th>
      <th>unit_price</th>
      <th>customer_id</th>
      <th>country</th>
      <th>line_price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>536365</td>
      <td>85123A</td>
      <td>WHITE HANGING HEART T-LIGHT HOLDER</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>2.55</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>15.30</td>
    </tr>
    <tr>
      <th>1</th>
      <td>536365</td>
      <td>71053</td>
      <td>WHITE METAL LANTERN</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>3.39</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>20.34</td>
    </tr>
    <tr>
      <th>2</th>
      <td>536365</td>
      <td>84406B</td>
      <td>CREAM CUPID HEARTS COAT HANGER</td>
      <td>8</td>
      <td>2010-12-01 08:26:00</td>
      <td>2.75</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>22.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>536365</td>
      <td>84029G</td>
      <td>KNITTED UNION FLAG HOT WATER BOTTLE</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>3.39</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>20.34</td>
    </tr>
    <tr>
      <th>4</th>
      <td>536365</td>
      <td>84029E</td>
      <td>RED WOOLLY HOTTIE WHITE HEART.</td>
      <td>6</td>
      <td>2010-12-01 08:26:00</td>
      <td>3.39</td>
      <td>17850.0</td>
      <td>United Kingdom</td>
      <td>20.34</td>
    </tr>
  </tbody>
</table>

3. #### Create a transactions dataframe

The `get_transactions()` function takes the formatted Pandas dataframe of transaction items and returns a Pandas dataframe of aggregated transaction data, which includes features identifying the order number. 

```python
import pandas as pd
from ecommercetools import customers

transaction_items = pd.read_csv('transaction_items.csv')
transactions = transactions.get_transactions(transaction_items)
transactions.to_csv('transactions.csv', index=False)
print(transactions.head())
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>order_id</th>
      <th>order_date</th>
      <th>customer_id</th>
      <th>skus</th>
      <th>items</th>
      <th>revenue</th>
      <th>replacement</th>
      <th>order_number</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>536365</td>
      <td>2010-12-01 08:26:00</td>
      <td>17850.0</td>
      <td>7</td>
      <td>40</td>
      <td>139.12</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>536366</td>
      <td>2010-12-01 08:28:00</td>
      <td>17850.0</td>
      <td>2</td>
      <td>12</td>
      <td>22.20</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>536367</td>
      <td>2010-12-01 08:34:00</td>
      <td>13047.0</td>
      <td>12</td>
      <td>83</td>
      <td>278.73</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>536368</td>
      <td>2010-12-01 08:34:00</td>
      <td>13047.0</td>
      <td>4</td>
      <td>15</td>
      <td>70.05</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>536369</td>
      <td>2010-12-01 08:35:00</td>
      <td>13047.0</td>
      <td>1</td>
      <td>3</td>
      <td>17.85</td>
      <td>0</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

---

### Products

#### 1. Get product data from transaction items

```python
products_df = products.get_products(transaction_items)
products_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sku</th>
      <th>first_order_date</th>
      <th>last_order_date</th>
      <th>customers</th>
      <th>orders</th>
      <th>items</th>
      <th>revenue</th>
      <th>avg_unit_price</th>
      <th>avg_quantity</th>
      <th>avg_revenue</th>
      <th>avg_orders</th>
      <th>product_tenure</th>
      <th>product_recency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10002</td>
      <td>2010-12-01 08:45:00</td>
      <td>2011-04-28 15:05:00</td>
      <td>40</td>
      <td>73</td>
      <td>1037</td>
      <td>759.89</td>
      <td>1.056849</td>
      <td>14.205479</td>
      <td>10.409452</td>
      <td>1.82</td>
      <td>3749</td>
      <td>3600</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10080</td>
      <td>2011-02-27 13:47:00</td>
      <td>2011-11-21 17:04:00</td>
      <td>19</td>
      <td>24</td>
      <td>495</td>
      <td>119.09</td>
      <td>0.376667</td>
      <td>20.625000</td>
      <td>4.962083</td>
      <td>1.26</td>
      <td>3660</td>
      <td>3393</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10120</td>
      <td>2010-12-03 11:19:00</td>
      <td>2011-12-04 13:15:00</td>
      <td>25</td>
      <td>29</td>
      <td>193</td>
      <td>40.53</td>
      <td>0.210000</td>
      <td>6.433333</td>
      <td>1.351000</td>
      <td>1.16</td>
      <td>3746</td>
      <td>3380</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10123C</td>
      <td>2010-12-03 11:19:00</td>
      <td>2011-07-15 15:05:00</td>
      <td>3</td>
      <td>4</td>
      <td>-13</td>
      <td>3.25</td>
      <td>0.487500</td>
      <td>-3.250000</td>
      <td>0.812500</td>
      <td>1.33</td>
      <td>3746</td>
      <td>3522</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10123G</td>
      <td>2011-04-08 11:13:00</td>
      <td>2011-04-08 11:13:00</td>
      <td>0</td>
      <td>1</td>
      <td>-38</td>
      <td>0.00</td>
      <td>0.000000</td>
      <td>-38.000000</td>
      <td>0.000000</td>
      <td>inf</td>
      <td>3620</td>
      <td>3620</td>
    </tr>
  </tbody>
</table>

#### 2. Calculate product consumption and repurchase rate


```python
repurchase_rates = products.get_repurchase_rates(transaction_items)
repurchase_rates.head(3).T
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>sku</th>
      <td>10002</td>
      <td>10080</td>
      <td>10120</td>
    </tr>
    <tr>
      <th>revenue</th>
      <td>759.89</td>
      <td>119.09</td>
      <td>40.53</td>
    </tr>
    <tr>
      <th>items</th>
      <td>1037</td>
      <td>495</td>
      <td>193</td>
    </tr>
    <tr>
      <th>orders</th>
      <td>73</td>
      <td>24</td>
      <td>29</td>
    </tr>
    <tr>
      <th>customers</th>
      <td>40</td>
      <td>19</td>
      <td>25</td>
    </tr>
    <tr>
      <th>avg_unit_price</th>
      <td>1.05685</td>
      <td>0.376667</td>
      <td>0.21</td>
    </tr>
    <tr>
      <th>avg_line_price</th>
      <td>10.4095</td>
      <td>4.96208</td>
      <td>1.351</td>
    </tr>
    <tr>
      <th>avg_items_per_order</th>
      <td>14.2055</td>
      <td>20.625</td>
      <td>6.65517</td>
    </tr>
    <tr>
      <th>avg_items_per_customer</th>
      <td>25.925</td>
      <td>26.0526</td>
      <td>7.72</td>
    </tr>
    <tr>
      <th>purchased_individually</th>
      <td>0</td>
      <td>0</td>
      <td>9</td>
    </tr>
    <tr>
      <th>purchased_once</th>
      <td>34</td>
      <td>17</td>
      <td>22</td>
    </tr>
    <tr>
      <th>bulk_purchases</th>
      <td>73</td>
      <td>24</td>
      <td>20</td>
    </tr>
    <tr>
      <th>bulk_purchase_rate</th>
      <td>1</td>
      <td>1</td>
      <td>0.689655</td>
    </tr>
    <tr>
      <th>repurchases</th>
      <td>39</td>
      <td>7</td>
      <td>7</td>
    </tr>
    <tr>
      <th>repurchase_rate</th>
      <td>0.534247</td>
      <td>0.291667</td>
      <td>0.241379</td>
    </tr>
    <tr>
      <th>repurchase_rate_label</th>
      <td>Moderate repurchase</td>
      <td>Low repurchase</td>
      <td>Low repurchase</td>
    </tr>
    <tr>
      <th>bulk_purchase_rate_label</th>
      <td>Very high bulk</td>
      <td>Very high bulk</td>
      <td>High bulk</td>
    </tr>
    <tr>
      <th>bulk_and_repurchase_label</th>
      <td>Moderate repurchase_Very high bulk</td>
      <td>Low repurchase_Very high bulk</td>
      <td>Low repurchase_High bulk</td>
    </tr>
  </tbody>
</table>

---

### Customers

#### 1. Create a customers dataset

```python
from ecommercetools import customers

customers_df = customers.get_customers(transaction_items)
customers_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>revenue</th>
      <th>orders</th>
      <th>skus</th>
      <th>items</th>
      <th>first_order_date</th>
      <th>last_order_date</th>
      <th>avg_items</th>
      <th>avg_order_value</th>
      <th>tenure</th>
      <th>recency</th>
      <th>cohort</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12346.0</td>
      <td>0.00</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>2011-01-18 10:01:00</td>
      <td>2011-01-18 10:17:00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>3701</td>
      <td>3700</td>
      <td>20111</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12347.0</td>
      <td>4310.00</td>
      <td>7</td>
      <td>7</td>
      <td>2458</td>
      <td>2010-12-07 14:57:00</td>
      <td>2011-12-07 15:52:00</td>
      <td>351.14</td>
      <td>615.71</td>
      <td>3742</td>
      <td>3377</td>
      <td>20104</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12348.0</td>
      <td>1797.24</td>
      <td>4</td>
      <td>4</td>
      <td>2341</td>
      <td>2010-12-16 19:09:00</td>
      <td>2011-09-25 13:13:00</td>
      <td>585.25</td>
      <td>449.31</td>
      <td>3733</td>
      <td>3450</td>
      <td>20104</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12349.0</td>
      <td>1757.55</td>
      <td>1</td>
      <td>1</td>
      <td>631</td>
      <td>2011-11-21 09:51:00</td>
      <td>2011-11-21 09:51:00</td>
      <td>631.00</td>
      <td>1757.55</td>
      <td>3394</td>
      <td>3394</td>
      <td>20114</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12350.0</td>
      <td>334.40</td>
      <td>1</td>
      <td>1</td>
      <td>197</td>
      <td>2011-02-02 16:01:00</td>
      <td>2011-02-02 16:01:00</td>
      <td>197.00</td>
      <td>334.40</td>
      <td>3685</td>
      <td>3685</td>
      <td>20111</td>
    </tr>
  </tbody>
</table>

#### 2. Create a customer cohort analysis dataset


```python
from ecommercetools import customers

cohorts_df = customers.get_cohorts(transaction_items, period='M')
cohorts_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>order_id</th>
      <th>order_date</th>
      <th>acquisition_cohort</th>
      <th>order_cohort</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>17850.0</td>
      <td>536365</td>
      <td>2010-12-01 08:26:00</td>
      <td>2010-12</td>
      <td>2010-12</td>
    </tr>
    <tr>
      <th>7</th>
      <td>17850.0</td>
      <td>536366</td>
      <td>2010-12-01 08:28:00</td>
      <td>2010-12</td>
      <td>2010-12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>13047.0</td>
      <td>536367</td>
      <td>2010-12-01 08:34:00</td>
      <td>2010-12</td>
      <td>2010-12</td>
    </tr>
    <tr>
      <th>21</th>
      <td>13047.0</td>
      <td>536368</td>
      <td>2010-12-01 08:34:00</td>
      <td>2010-12</td>
      <td>2010-12</td>
    </tr>
    <tr>
      <th>25</th>
      <td>13047.0</td>
      <td>536369</td>
      <td>2010-12-01 08:35:00</td>
      <td>2010-12</td>
      <td>2010-12</td>
    </tr>
  </tbody>
</table>


#### 3. Create a customer cohort analysis matrix

```python
from ecommercetools import customers

cohort_matrix_df = customers.get_cohort_matrix(transaction_items, period='M', percentage=True)
cohort_matrix_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th>periods</th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
    </tr>
    <tr>
      <th>acquisition_cohort</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-12</th>
      <td>1.0</td>
      <td>0.381857</td>
      <td>0.334388</td>
      <td>0.387131</td>
      <td>0.359705</td>
      <td>0.396624</td>
      <td>0.379747</td>
      <td>0.354430</td>
      <td>0.354430</td>
      <td>0.394515</td>
      <td>0.373418</td>
      <td>0.500000</td>
      <td>0.274262</td>
    </tr>
    <tr>
      <th>2011-01</th>
      <td>1.0</td>
      <td>0.239905</td>
      <td>0.282660</td>
      <td>0.242280</td>
      <td>0.327791</td>
      <td>0.299287</td>
      <td>0.261283</td>
      <td>0.256532</td>
      <td>0.311164</td>
      <td>0.346793</td>
      <td>0.368171</td>
      <td>0.149644</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-02</th>
      <td>1.0</td>
      <td>0.247368</td>
      <td>0.192105</td>
      <td>0.278947</td>
      <td>0.268421</td>
      <td>0.247368</td>
      <td>0.255263</td>
      <td>0.281579</td>
      <td>0.257895</td>
      <td>0.313158</td>
      <td>0.092105</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-03</th>
      <td>1.0</td>
      <td>0.190909</td>
      <td>0.254545</td>
      <td>0.218182</td>
      <td>0.231818</td>
      <td>0.177273</td>
      <td>0.263636</td>
      <td>0.238636</td>
      <td>0.288636</td>
      <td>0.088636</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-04</th>
      <td>1.0</td>
      <td>0.227425</td>
      <td>0.220736</td>
      <td>0.210702</td>
      <td>0.207358</td>
      <td>0.237458</td>
      <td>0.230769</td>
      <td>0.260870</td>
      <td>0.083612</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>


```python
from ecommercetools import customers

cohort_matrix_df = customers.get_cohort_matrix(transaction_items, period='M', percentage=False)
cohort_matrix_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th>periods</th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
    </tr>
    <tr>
      <th>acquisition_cohort</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-12</th>
      <td>948.0</td>
      <td>362.0</td>
      <td>317.0</td>
      <td>367.0</td>
      <td>341.0</td>
      <td>376.0</td>
      <td>360.0</td>
      <td>336.0</td>
      <td>336.0</td>
      <td>374.0</td>
      <td>354.0</td>
      <td>474.0</td>
      <td>260.0</td>
    </tr>
    <tr>
      <th>2011-01</th>
      <td>421.0</td>
      <td>101.0</td>
      <td>119.0</td>
      <td>102.0</td>
      <td>138.0</td>
      <td>126.0</td>
      <td>110.0</td>
      <td>108.0</td>
      <td>131.0</td>
      <td>146.0</td>
      <td>155.0</td>
      <td>63.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-02</th>
      <td>380.0</td>
      <td>94.0</td>
      <td>73.0</td>
      <td>106.0</td>
      <td>102.0</td>
      <td>94.0</td>
      <td>97.0</td>
      <td>107.0</td>
      <td>98.0</td>
      <td>119.0</td>
      <td>35.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-03</th>
      <td>440.0</td>
      <td>84.0</td>
      <td>112.0</td>
      <td>96.0</td>
      <td>102.0</td>
      <td>78.0</td>
      <td>116.0</td>
      <td>105.0</td>
      <td>127.0</td>
      <td>39.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-04</th>
      <td>299.0</td>
      <td>68.0</td>
      <td>66.0</td>
      <td>63.0</td>
      <td>62.0</td>
      <td>71.0</td>
      <td>69.0</td>
      <td>78.0</td>
      <td>25.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>



#### 4. Create a customer "retention" dataset


```python
from ecommercetools import customers

retention_df = customers.get_retention(transactions_df)
retention_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acquisition_cohort</th>
      <th>order_cohort</th>
      <th>customers</th>
      <th>periods</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2010-12</td>
      <td>2010-12</td>
      <td>948</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2010-12</td>
      <td>2011-01</td>
      <td>362</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2010-12</td>
      <td>2011-02</td>
      <td>317</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2010-12</td>
      <td>2011-03</td>
      <td>367</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2010-12</td>
      <td>2011-04</td>
      <td>341</td>
      <td>4</td>
    </tr>
  </tbody>
</table>

#### 5. Create an RFM (H) dataset

This is an extension of the regular Recency, Frequency, Monetary value (RFM) model that includes an additional parameter "H" for heterogeneity. This shows the number of unique SKUs purchased by each customer. While typically unassociated with targeting, this value can be very useful in identifying which customers should probably be buying a broader mix of products than they currently are, as well as spotting those who may have stopped buying certain items. 


```python
from ecommercetools import customers

rfm_df = customers.get_rfm_segments(customers_df)
rfm_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>acquisition_date</th>
      <th>recency_date</th>
      <th>recency</th>
      <th>frequency</th>
      <th>monetary</th>
      <th>heterogeneity</th>
      <th>tenure</th>
      <th>r</th>
      <th>f</th>
      <th>m</th>
      <th>h</th>
      <th>rfm</th>
      <th>rfm_score</th>
      <th>rfm_segment_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12346.0</td>
      <td>2011-01-18 10:01:00</td>
      <td>2011-01-18 10:17:00</td>
      <td>3700</td>
      <td>2</td>
      <td>0.00</td>
      <td>1</td>
      <td>3701</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>111</td>
      <td>3</td>
      <td>Risky</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12350.0</td>
      <td>2011-02-02 16:01:00</td>
      <td>2011-02-02 16:01:00</td>
      <td>3685</td>
      <td>1</td>
      <td>334.40</td>
      <td>1</td>
      <td>3685</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>111</td>
      <td>3</td>
      <td>Risky</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12365.0</td>
      <td>2011-02-21 13:51:00</td>
      <td>2011-02-21 14:04:00</td>
      <td>3666</td>
      <td>3</td>
      <td>320.69</td>
      <td>2</td>
      <td>3666</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>111</td>
      <td>3</td>
      <td>Risky</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12373.0</td>
      <td>2011-02-01 13:10:00</td>
      <td>2011-02-01 13:10:00</td>
      <td>3686</td>
      <td>1</td>
      <td>364.60</td>
      <td>1</td>
      <td>3686</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>111</td>
      <td>3</td>
      <td>Risky</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12377.0</td>
      <td>2010-12-20 09:37:00</td>
      <td>2011-01-28 15:45:00</td>
      <td>3690</td>
      <td>2</td>
      <td>1628.12</td>
      <td>2</td>
      <td>3730</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>111</td>
      <td>3</td>
      <td>Risky</td>
    </tr>
  </tbody>
</table>


#### 6. Create a purchase latency dataset


```python
from ecommercetools import customers 

latency_df = customers.get_latency(transactions_df)
latency_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>frequency</th>
      <th>recency_date</th>
      <th>recency</th>
      <th>avg_latency</th>
      <th>min_latency</th>
      <th>max_latency</th>
      <th>std_latency</th>
      <th>cv</th>
      <th>days_to_next_order</th>
      <th>label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12680.0</td>
      <td>4</td>
      <td>2011-12-09 12:50:00</td>
      <td>3388</td>
      <td>28</td>
      <td>16</td>
      <td>73</td>
      <td>30.859898</td>
      <td>1.102139</td>
      <td>-3329.0</td>
      <td>Order overdue</td>
    </tr>
    <tr>
      <th>1</th>
      <td>13113.0</td>
      <td>24</td>
      <td>2011-12-09 12:49:00</td>
      <td>3388</td>
      <td>15</td>
      <td>0</td>
      <td>52</td>
      <td>12.060126</td>
      <td>0.804008</td>
      <td>-3361.0</td>
      <td>Order overdue</td>
    </tr>
    <tr>
      <th>2</th>
      <td>15804.0</td>
      <td>13</td>
      <td>2011-12-09 12:31:00</td>
      <td>3388</td>
      <td>15</td>
      <td>1</td>
      <td>39</td>
      <td>11.008261</td>
      <td>0.733884</td>
      <td>-3362.0</td>
      <td>Order overdue</td>
    </tr>
    <tr>
      <th>3</th>
      <td>13777.0</td>
      <td>33</td>
      <td>2011-12-09 12:25:00</td>
      <td>3388</td>
      <td>11</td>
      <td>0</td>
      <td>48</td>
      <td>12.055274</td>
      <td>1.095934</td>
      <td>-3365.0</td>
      <td>Order overdue</td>
    </tr>
    <tr>
      <th>4</th>
      <td>17581.0</td>
      <td>25</td>
      <td>2011-12-09 12:21:00</td>
      <td>3388</td>
      <td>14</td>
      <td>0</td>
      <td>67</td>
      <td>21.974293</td>
      <td>1.569592</td>
      <td>-3352.0</td>
      <td>Order overdue</td>
    </tr>
  </tbody>
</table>



#### 7. Customer ABC segmentation

```python
from ecommercetools import customers

abc_df = customers.get_abc_segments(customers_df, months=12, abc_class_name='abc_class_12m', abc_rank_name='abc_rank_12m')
abc_df.head()
```


<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>abc_class_12m</th>
      <th>abc_rank_12m</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12346.0</td>
      <td>D</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12347.0</td>
      <td>D</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12348.0</td>
      <td>D</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12349.0</td>
      <td>D</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12350.0</td>
      <td>D</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>

#### 8. Predict customer AOV, CLV, and orders

EcommerceTools allows you to predict the AOV, Customer Lifetime Value (CLV) and expected number of orders via the Gamma-Gamma and BG/NBD models from the excellent Lifetimes package. By passing the dataframe of transactions from `get_transactions()` to the `get_customer_predictions()` function, EcommerceTools will fit the BG/NBD and Gamma-Gamma models and predict the AOV, order quantity, and CLV for each customer in the defined number of future days after the end of the observation period.

```python
customer_predictions = customers.get_customer_predictions(transactions_df, 
                                                          observation_period_end='2011-12-09', 
                                                          days=90)
customer_predictions.head(10)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>customer_id</th>
      <th>predicted_purchases</th>
      <th>aov</th>
      <th>clv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12346.0</td>
      <td>0.188830</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12347.0</td>
      <td>1.408736</td>
      <td>569.978836</td>
      <td>836.846896</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12348.0</td>
      <td>0.805907</td>
      <td>333.784235</td>
      <td>308.247354</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12349.0</td>
      <td>0.855607</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12350.0</td>
      <td>0.196304</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>12352.0</td>
      <td>1.682277</td>
      <td>376.175359</td>
      <td>647.826169</td>
    </tr>
    <tr>
      <th>6</th>
      <td>12353.0</td>
      <td>0.272541</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>12354.0</td>
      <td>0.247183</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>12355.0</td>
      <td>0.262909</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>12356.0</td>
      <td>0.645368</td>
      <td>324.039419</td>
      <td>256.855226</td>
    </tr>
  </tbody>
</table>
---

### Advertising

#### 1. Create paid search keywords


```python
from ecommercetools import advertising

product_names = ['fly rods', 'fly reels']
keywords_prepend = ['buy', 'best', 'cheap', 'reduced']
keywords_append = ['for sale', 'price', 'promotion', 'promo', 'coupon', 'voucher', 'shop', 'suppliers']
campaign_name = 'fly_fishing'

keywords = advertising.generate_ad_keywords(product_names, keywords_prepend, keywords_append, campaign_name)
keywords.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>product</th>
      <th>keywords</th>
      <th>match_type</th>
      <th>campaign_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>fly rods</td>
      <td>[fly rods]</td>
      <td>Exact</td>
      <td>fly_fishing</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fly rods</td>
      <td>[buy fly rods]</td>
      <td>Exact</td>
      <td>fly_fishing</td>
    </tr>
    <tr>
      <th>2</th>
      <td>fly rods</td>
      <td>[best fly rods]</td>
      <td>Exact</td>
      <td>fly_fishing</td>
    </tr>
    <tr>
      <th>3</th>
      <td>fly rods</td>
      <td>[cheap fly rods]</td>
      <td>Exact</td>
      <td>fly_fishing</td>
    </tr>
    <tr>
      <th>4</th>
      <td>fly rods</td>
      <td>[reduced fly rods]</td>
      <td>Exact</td>
      <td>fly_fishing</td>
    </tr>
  </tbody>
</table>


#### 2. Create paid search ad copy using Spintax

```python
from ecommercetools import advertising

text = "Fly Reels from {Orvis|Loop|Sage|Airflo|Nautilus} for {trout|salmon|grayling|pike}"
spin = advertising.generate_spintax(text, single=False)

spin
```


    ['Fly Reels from Orvis for trout',
     'Fly Reels from Orvis for salmon',
     'Fly Reels from Orvis for grayling',
     'Fly Reels from Orvis for pike',
     'Fly Reels from Loop for trout',
     'Fly Reels from Loop for salmon',
     'Fly Reels from Loop for grayling',
     'Fly Reels from Loop for pike',
     'Fly Reels from Sage for trout',
     'Fly Reels from Sage for salmon',
     'Fly Reels from Sage for grayling',
     'Fly Reels from Sage for pike',
     'Fly Reels from Airflo for trout',
     'Fly Reels from Airflo for salmon',
     'Fly Reels from Airflo for grayling',
     'Fly Reels from Airflo for pike',
     'Fly Reels from Nautilus for trout',
     'Fly Reels from Nautilus for salmon',
     'Fly Reels from Nautilus for grayling',
     'Fly Reels from Nautilus for pike']

---

### Operations

#### 1. Create an ABC inventory classification

```python
inventory_classification = operations.get_inventory_classification(transaction_items)
inventory_classification.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sku</th>
      <th>abc_class</th>
      <th>abc_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10002</td>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10080</td>
      <td>A</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10120</td>
      <td>A</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10123C</td>
      <td>A</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10123G</td>
      <td>A</td>
      <td>4</td>
    </tr>
  </tbody>
</table>


---
### Marketing

#### 1. Get ecommerce trading calendar

```python
from ecommercetools import marketing

trading_calendar_df = marketing.get_trading_calendar('2021-01-01', days=365)
trading_calendar_df.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>event</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-01-01</td>
      <td>January sale</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021-01-02</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021-01-03</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>2021-01-04</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>2021-01-05</td>
      <td></td>
    </tr>
  </tbody>
</table>


#### 2. Get ecommerce trading events


```python
from ecommercetools import marketing

trading_events_df = marketing.get_trading_events('2021-01-01', days=365)
trading_events_df.head()
```


<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>event</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-01-01</td>
      <td>January sale</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021-01-29</td>
      <td>January Pay Day</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021-02-11</td>
      <td>Valentine's Day [last order date]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2021-02-14</td>
      <td>Valentine's Day</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2021-02-26</td>
      <td>February Pay Day</td>
    </tr>
  </tbody>
</table>



---

### NLP

#### 1. Generate text summaries
The `get_summaries()` function of the `nlp` module takes a Pandas dataframe containing text and returns a machine-generated summary of the content using a Huggingface Transformers pipeline via PyTorch. To use this feature, first load your Pandas dataframe and import the `nlp` module from `ecommercetools`.

```python
import pandas as pd
from ecommercetools import nlp 

pd.set_option('max_colwidth', 1000)
df = pd.read_csv('text.csv')
df.head()
```

Specify the name of the Pandas dataframe, the column containing the text you wish to summarise (i.e. `product_description`), and specify a column name in which to store the machine-generated summary. The `min_length` and `max_length` arguments control the number of words generated, while the `do_sample` argument controls whether the generated text is completely unique (`do_sample=False`) or extracted from the text (`do_sample=True`).

```python
df = nlp.get_summaries(df, 'product_description', 'sampled_summary', min_length=50, max_length=100, do_sample=True)
df = nlp.get_summaries(df, 'product_description', 'unsampled_summary', min_length=50, max_length=100, do_sample=False)
df = nlp.get_summaries(df, 'product_description', 'unsampled_summary_20_to_30', min_length=20, max_length=30, do_sample=False)
```

Since the model used for text summarisation is very large (1.2 GB plus), this function will take some time to complete. Once loaded, summaries are generated within a second or two per piece of text, so it is advisable to try smaller volumes of data initially.


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


<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>loc</th>
      <th>changefreq</th>
      <th>priority</th>
      <th>domain</th>
      <th>sitemap_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>http://flyandlure.org/</td>
      <td>hourly</td>
      <td>1.0</td>
      <td>flyandlure.org</td>
      <td>http://www.flyandlure.org/sitemap.xml</td>
    </tr>
    <tr>
      <th>1</th>
      <td>http://flyandlure.org/about</td>
      <td>monthly</td>
      <td>1.0</td>
      <td>flyandlure.org</td>
      <td>http://www.flyandlure.org/sitemap.xml</td>
    </tr>
    <tr>
      <th>2</th>
      <td>http://flyandlure.org/terms</td>
      <td>monthly</td>
      <td>1.0</td>
      <td>flyandlure.org</td>
      <td>http://www.flyandlure.org/sitemap.xml</td>
    </tr>
    <tr>
      <th>3</th>
      <td>http://flyandlure.org/privacy</td>
      <td>monthly</td>
      <td>1.0</td>
      <td>flyandlure.org</td>
      <td>http://www.flyandlure.org/sitemap.xml</td>
    </tr>
    <tr>
      <th>4</th>
      <td>http://flyandlure.org/copyright</td>
      <td>monthly</td>
      <td>1.0</td>
      <td>flyandlure.org</td>
      <td>http://www.flyandlure.org/sitemap.xml</td>
    </tr>
  </tbody>
</table>


#### 3. Get Core Web Vitals from PageSpeed Insights
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


<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>page</th>
      <th>device</th>
      <th>query</th>
      <th>clicks</th>
      <th>impressions</th>
      <th>ctr</th>
      <th>position</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>http://flyandlure.org/articles/fly_fishing_gea...</td>
      <td>MOBILE</td>
      <td>simms freestone waders review</td>
      <td>56</td>
      <td>217</td>
      <td>25.81</td>
      <td>3.12</td>
    </tr>
    <tr>
      <th>1</th>
      <td>http://flyandlure.org/</td>
      <td>MOBILE</td>
      <td>fly and lure</td>
      <td>37</td>
      <td>159</td>
      <td>23.27</td>
      <td>3.81</td>
    </tr>
    <tr>
      <th>2</th>
      <td>http://flyandlure.org/articles/fly_fishing_gea...</td>
      <td>DESKTOP</td>
      <td>orvis encounter waders review</td>
      <td>35</td>
      <td>134</td>
      <td>26.12</td>
      <td>4.04</td>
    </tr>
    <tr>
      <th>3</th>
      <td>http://flyandlure.org/articles/fly_fishing_gea...</td>
      <td>DESKTOP</td>
      <td>simms freestone waders review</td>
      <td>35</td>
      <td>200</td>
      <td>17.50</td>
      <td>3.50</td>
    </tr>
    <tr>
      <th>4</th>
      <td>http://flyandlure.org/</td>
      <td>DESKTOP</td>
      <td>fly and lure</td>
      <td>32</td>
      <td>170</td>
      <td>18.82</td>
      <td>3.09</td>
    </tr>
  </tbody>
</table>

##### Fetching all results from Google Search Console

To fetch all results, set `fetch_all` to `True`. This will automatically paginate through your Google Search Console data and return all results. Be aware that if you do this you may hit Google's quota limit if you run a query over an extended period, or have a busy site with lots of `page` or `query` dimensions. 

```python
from ecommercetools import seo

key = "google-search-console.json"
site_url = "http://flyandlure.org"
payload = {
    'startDate': "2019-01-01",
    'endDate': "2019-12-31",
    'dimensions': ["page", "device", "query"],
    'rowLimit': 25000,
    'startRow': 0
}

df = seo.query_google_search_console(key, site_url, payload, fetch_all=True)
print(df.head())

```

##### Comparing two time periods in Google Search Console

```python
payload_before = {
    'startDate': "2021-08-11",
    'endDate': "2021-08-31",
    'dimensions': ["page","query"],    
}

payload_after = {
    'startDate': "2021-07-21",
    'endDate': "2021-08-10",
    'dimensions': ["page","query"],    
}

df = seo.query_google_search_console_compare(key, site_url, payload_before, payload_after, fetch_all=False)
df.sort_values(by='clicks_change', ascending=False).head()
```


#### 6. Get the number of "indexed" pages
The `get_indexed_pages()` function uses the "site:" prefix to search Google for the number of pages "indexed". This is very approximate and may not be a perfect representation, but it's usually a good guide of site "size" in the absence of other data. 

```python
from ecommercetools import seo

urls = ['https://www.bbc.co.uk', 'https://www.bbc.co.uk/iplayer', 'http://flyandlure.org']
df = seo.get_indexed_pages(urls)
print(df.head())
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>url</th>
      <th>indexed_pages</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>http://flyandlure.org</td>
      <td>2090</td>
    </tr>
    <tr>
      <th>1</th>
      <td>https://www.bbc.co.uk/iplayer</td>
      <td>215000</td>
    </tr>
    <tr>
      <th>0</th>
      <td>https://www.bbc.co.uk</td>
      <td>12700000</td>
    </tr>
  </tbody>
</table>


#### 7. Get keyword suggestions from Google Autocomplete
The `google_autocomplete()` function returns a set of keyword suggestions from Google Autocomplete. The `include_expanded=True` argument allows you to expand the number of suggestions shown by appending prefixes and suffixes to the search terms. 

```python
from ecommercetools import seo

suggestions = seo.google_autocomplete("data science", include_expanded=False)
print(suggestions)

suggestions = seo.google_autocomplete("data science", include_expanded=True)
print(suggestions)
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>term</th>
      <th>relevance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>data science jobs</td>
      <td>650</td>
    </tr>
    <tr>
      <th>1</th>
      <td>data science jobs chester</td>
      <td>601</td>
    </tr>
    <tr>
      <th>2</th>
      <td>data science course</td>
      <td>600</td>
    </tr>
    <tr>
      <th>3</th>
      <td>data science masters</td>
      <td>554</td>
    </tr>
    <tr>
      <th>4</th>
      <td>data science salary</td>
      <td>553</td>
    </tr>
    <tr>
      <th>5</th>
      <td>data science internship</td>
      <td>552</td>
    </tr>
    <tr>
      <th>6</th>
      <td>data science jobs london</td>
      <td>551</td>
    </tr>
    <tr>
      <th>7</th>
      <td>data science graduate scheme</td>
      <td>550</td>
    </tr>
  </tbody>
</table>

#### 8. Retrieve robots.txt content
The `get_robots()` function returns the contents of a robots.txt file in a Pandas dataframe so it can be parsed and analysed. 

```python
from ecommercetools import seo

robots = seo.get_robots("http://www.flyandlure.org/robots.txt")
print(robots)
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>directive</th>
      <th>parameter</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>User-agent</td>
      <td>*</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Disallow</td>
      <td>/signin</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Disallow</td>
      <td>/signup</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Disallow</td>
      <td>/users</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Disallow</td>
      <td>/contact</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Disallow</td>
      <td>/activate</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Disallow</td>
      <td>/*/page</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Disallow</td>
      <td>/articles/search</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Disallow</td>
      <td>/search.php</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Disallow</td>
      <td>*q=*</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Disallow</td>
      <td>*category_slug=*</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Disallow</td>
      <td>*country_slug=*</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Disallow</td>
      <td>*county_slug=*</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Disallow</td>
      <td>*features=*</td>
    </tr>
  </tbody>
</table>

#### 9. Get Google SERPs
The `get_serps()` function returns a Pandas dataframe containing the Google search engine results for a given search term. Note that this function is not suitable for large-scale scraping and currently includes no features to prevent it from being blocked.

```python
from ecommercetools import seo

serps = seo.get_serps("data science blog")
print(serps)
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>link</th>
      <th>text</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10 of the best data science blogs to follow - ...</td>
      <td>https://www.tableau.com/learn/articles/data-sc...</td>
      <td>10 of the best data science blogs to follow. T...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Best Data Science Blogs to Follow in 2020 | by...</td>
      <td>https://towardsdatascience.com/best-data-scien...</td>
      <td>14 Jul 2020 — 1. Towards Data Science · Joined...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Top 20 Data Science Blogs And Websites For Dat...</td>
      <td>https://medium.com/@exastax/top-20-data-scienc...</td>
      <td>Top 20 Data Science Blogs And Websites For Dat...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Data Science Blog – Dataquest</td>
      <td>https://www.dataquest.io/blog/</td>
      <td>Browse our data science blog to get helpful ti...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>51 Awesome Data Science Blogs You Need To Chec...</td>
      <td>https://365datascience.com/trending/51-data-sc...</td>
      <td>Blog name: DataKind · datakind data science bl...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Blogs on AI, Analytics, Data Science, Machine ...</td>
      <td>https://www.kdnuggets.com/websites/blogs.html</td>
      <td>Individual/small group blogs · Ai4 blog, featu...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Data Science Blog – Applied Data Science</td>
      <td>https://data-science-blog.com/</td>
      <td>... an Bedeutung – DevOps for Data Science. De...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Top 10 Data Science and AI Blogs in 2020 - Liv...</td>
      <td>https://livecodestream.dev/post/top-data-scien...</td>
      <td>Some of the best data science and AI blogs for...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Data Science Blogs: 17 Must-Read Blogs for Dat...</td>
      <td>https://www.thinkful.com/blog/data-science-blogs/</td>
      <td>Data scientists could be considered the magici...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>rushter/data-science-blogs: A curated list of ...</td>
      <td>https://github.com/rushter/data-science-blogs</td>
      <td>A curated list of data science blogs. Contribu...</td>
    </tr>
  </tbody>
</table>


---

### Reports
The Reports module creates weekly, monthly, quarterly, or yearly reports for customers and orders and calculates a range of common ecommerce metrics to show business performance.

#### 1. Customers report
The `customers_report()` function takes a formatted dataframe of transaction items (see above) and a desired frequency (D for daily, W for weekly, M for monthly, Q for quarterly) and calculates aggregate metrics for each period. 

The function returns the number of orders, the number of customers, the number of new customers, the number of returning customers, and the acquisition rate (or proportion of new customers). For monthly reporting, I would recommend a 13-month period so you can compare the last month with the same month the previous year. 

```python
from ecommercetools import reports

df_customers_report = reports.customers_report(transaction_items, frequency='M')
print(df_customers_report.head(13))
```

#### 2. Transactions report
The `transactions_report()` function takes a formatted dataframe of transaction items (see above) and a desired frequency (D for daily, W for weekly, M for monthly, Q for quarterly) and calculates aggregate metrics for each period. 

The metrics returned are: customers, orders, revenue, SKUs, units, average order value, average SKUs per order, average units per order, and average revenue per customer. 

```python
from ecommercetools import reports

df_orders_report = reports.transactions_report(transaction_items, frequency='M')
print(df_orders_report.head(13))
```

