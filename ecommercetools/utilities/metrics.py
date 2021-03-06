"""Common retail metrics."""

import math
from datetime import datetime

"""====================================================================================================================
SALES AND FINANCIAL METRICS
===================================================================================================================="""


def tax(gross_revenue, tax_rate=0.2):
    """Returns total tax based on gross revenue and tax rate.

    Args:
        gross_revenue (float): Gross revenue.
        tax_rate (float, optional): Product tax as decimal, i.e. 0.2 for 20% tax. Default is 0.2.

    Returns:
        total_tax (float): Total tax based on gross revenue and tax rate.

    Example:
        total_tax = tax(1000, 0.2)
        200.0
    """

    return gross_revenue * tax_rate


def net_revenue(gross_revenue, tax_rate=0.2):
    """Returns total net revenue based on gross revenue and tax rate.

    Args:
        gross_revenue (float): Gross revenue.
        tax_rate (float, optional): Product tax as decimal, i.e. 0.2 for 20% tax. Default is 0.2.

    Returns:
        net_revenue (float): Total net revenue based on gross revenue and tax rate.

    Example:
        net_revenue = net_revenue(1000, 0.2)
        800.0
    """

    total_tax = tax(gross_revenue, tax_rate)
    return gross_revenue - total_tax


def aov(total_revenue, total_orders):
    """Return the AOV (Average Order Value).

    Args:
        total_revenue (float): Total revenue.
        total_orders (int): Total number of orders.

    Returns:
        aov (float) as average order value
    """

    return total_revenue / total_orders


def product_cost(gross_revenue, margin, tax_rate=0.2):
    """Return the product cost from the gross revenue, product margin, and tax rate.

    Args:
        gross_revenue (float): Gross product revenue
        margin (float): Product margin as a decimal, i.e. 0.3 for 30% margin.
        tax_rate (float, optional): Optional tax rate, i.e. 0.2 for 20% tax.

    Returns:
        Product cost based on margin and tax rate.
    """

    revenue_net = net_revenue(gross_revenue, tax_rate)
    return revenue_net * margin


def gross_profit(gross_revenue, margin, tax_rate=0.2):
    """Return the gross profit from the gross revenue, product margin, and tax rate.

    Args:
        gross_revenue (float): Gross product revenue
        margin (float): Product margin as a decimal, i.e. 0.3 for 30% margin.
        tax_rate (float, optional): Optional tax rate, i.e. 0.2 for 20% tax.

    Returns:
        Gross profit based on margin and tax rate.
    """

    cost_product = product_cost(gross_revenue, margin, tax_rate)
    cost_tax = tax(gross_revenue, tax_rate)
    return gross_revenue - (cost_product + cost_tax)


def net_profit(gross_revenue, other_costs, margin, tax_rate=0.2):
    """Return the gross profit from the gross revenue, product margin, and tax rate.

    Args:
        gross_revenue (float): Gross product revenue
        other_costs (float): Other costs, i.e. advertising, cross-charges, shipping
        margin (float): Product margin as a decimal, i.e. 0.3 for 30% margin.
        tax_rate (float, optional): Optional tax rate, i.e. 0.2 for 20% tax.

    Returns:
        Gross profit based on margin and tax rate.
    """

    cost_product = product_cost(gross_revenue, margin, tax_rate)
    cost_tax = tax(gross_revenue, tax_rate)
    return gross_revenue - (cost_product + cost_tax + other_costs)


def sales_growth_rate(sales_period_1, sales_period_2):
    """Return the sales growth rate for the current period versus the previous period.

    Args:
        sales_period_1 (float): Total company sales for previous the period.
        sales_period_2 (float): Total company sales for the current period.

    Returns:
        Sales growth based on sales in period 2 versus period 1.
    """

    return ((sales_period_2 - sales_period_1) / sales_period_1) * 100


def revenue_per_unit(total_revenue, total_units):
    """Return the total revenue per unit for the period.

    Args:
        total_revenue (float): Total revenue generated during the period.
        total_units (int): Total units sold during the period.

    Returns:
        Total revenue per unit during the period.
    """

    return total_revenue / total_units


"""====================================================================================================================
MARKET STRATEGY METRICS
===================================================================================================================="""


def market_share(company_sales, market_sales):
    """Return the percentage market share for a company based on its revenue versus total market revenue.

    Args:
        company_sales (float): Total company sales for the period.
        market_sales (float): Total market sales for the period.

    Returns:
        market_share (float): Percentage of sales generated by the company within the market.
    """

    return (company_sales / market_sales) * 100


"""====================================================================================================================
CUSTOMER METRICS
===================================================================================================================="""


def retention_rate(customers_repurchasing_current_period,
                   customers_purchasing_previous_period):
    """Return the retention rate of customers acquired in one period who repurchased in another.

    Args:
        customers_repurchasing_current_period (int): The number of customers acquired in p1, who reordered in p2.
        customers_purchasing_previous_period (int): The number of customers who placed their first order in p1.

    Returns:
        retention_rate (float): Percentage of customers acquired in p1 who repurchased in p2.
    """

    return (customers_repurchasing_current_period / customers_purchasing_previous_period) * 100


"""====================================================================================================================
PRODUCT AND CATEGORY MANAGEMENT METRICS
===================================================================================================================="""


def share_of_shelf_index(products_of_brand_x, total_products):
    """Return share of shelf index showing the percentage of total products made up by brand X.

    Args:
        products_of_brand_x (int): Number of products of brand X in portfolio, category, or on shelf.
        total_products (int): Total number of products of all brands in portfolio, category, or on shelf.

    Returns:
        Percentage of shelf, category, or portfolio made up by brand X
    """

    return (products_of_brand_x / total_products) * 100


def product_turnover(units_sold_in_period, average_items_stocked_in_period):
    """Return the product turnover (or sell through rate) for a product based on units sold versus items stocked.

    Args:
        units_sold_in_period (int): Number of units of product X sold in the period.
        average_items_stocked_in_period (int): Average stock holding for product X in the period.

    Returns:
        product_turnover (float): Percentage of average stock holding sold during the period.
    """

    return (units_sold_in_period / average_items_stocked_in_period) * 100


def price_index(price_of_product_x, price_of_product_y):
    """Return the price index of product X over product Y.

    Args:
        price_of_product_x (float): Price of product X.
        price_of_product_y (float): Price of product Y.

    Returns:
        price_index (float): Price of X / Price of Y
    """

    return (price_of_product_x / price_of_product_y) * 100


def purchase_intention(people_who_declared_interest, total_people):
    """Returns the purchase intention rate for a product.

    This can be used for cart-to-detail, buy-to-detail, and similar calculations.

    Args:
        people_who_declared_interest (int): Number of people who declared interest in a product.
        total_people (int): Total number of people.

    Returns:
        Percentage of people who were interested in a product.
    """

    return (people_who_declared_interest / total_people) * 100


def product_trial_rate(number_of_first_time_purchases, total_purchasers):
    """Returns the percentage of customers who trialled a product for the first time during a period.

    Args:
        number_of_first_time_purchases (int): Total number of unique first-time purchasers during a period.
        total_purchasers (int): Total number of unique purchasers during a period.

    Returns:
        Percentage of customers who purchased product for the first time during a period.
    """

    return (number_of_first_time_purchases / total_purchasers) * 100


def product_repurchase_rate(number_of_repeat_purchasers, total_purchasers):
    """Returns the percentage of customers who purchased a product for the second time or more.

    Args:
        number_of_repeat_purchasers (int): Total number of unique repeat purchasers during a period.
        total_purchasers (int): Total number of unique purchasers during a period.

    Returns:
        Percentage of customers who purchased product for the second time or more during a period.
    """

    return (number_of_repeat_purchasers / total_purchasers) * 100


def product_consumption_rate(total_items, total_orders):
    """Returns the average number of units per order.

    Args:
        total_items (int): Total number of items of a SKU sold during a period.
        total_orders (int): Total number of orders during a period.

    Returns:
        Average number of units per order.
    """

    return (total_items / total_orders) * 100


def brand_usage(number_of_brand_purchasers, total_purchasers):
    """Returns the percentage of brand usage for a period.

    Args:
        number_of_brand_purchasers (int): Total number of unique purchasers of a brand in a period.
        total_purchasers (int): Total unique purchasers in a period.

    Returns:
        Percentage of purchasers who used brand X in the period.
    """

    return (number_of_brand_purchasers / total_purchasers) * 100


def brand_penetration_rate(number_of_brand_purchasers, total_purchasers):
    """Returns the percentage of penetration rate for a brand.

    Args:
        number_of_brand_purchasers (int): Total number of unique purchasers of a brand.
        total_purchasers (int): Total unique purchasers.

    Returns:
        Percentage of purchasers who have purchased the brand.
    """

    return (number_of_brand_purchasers / total_purchasers) * 100


def product_satisfaction(total_reviews, positive_reviews):
    """Return the product satisfaction score for a period.

    Args:
        total_reviews (int): Total number of reviews received within the period.
        positive_reviews (int): Total number of positive reviews received within the period.

    Returns:
        Percentage (float) of positive reviews received.
    """

    return (positive_reviews / total_reviews) * 100


"""====================================================================================================================
SALES TEAM METRICS
===================================================================================================================="""


def market_coverage_index(unique_customers_contacted, unique_customers):
    """Returns the market coverage index showing the percentage of customers contacted or visited by a sales force.

    Args:
        unique_customers_contacted (int): Unique customers contacted/visited during the period.
        unique_customers (int): Unique customers who purchased during the period, or who are managed by the sales force.

    Returns:
        Market coverage representing the percentage of customers contacted or visited during a period.
    """

    return (unique_customers_contacted / unique_customers) * 100


def sales_force_efficiency(number_of_orders_from_visits, number_of_visits):
    """Returns the percentage of visits by the sales force that resulted in orders from customers.

    Args:
        number_of_orders_from_visits (int): Number of orders generated by sales force visits during the period.
        number_of_visits (int): Number of sales force visits during the period.

    Returns:
        Percentage of visits by the sales force that led to orders.
    """

    return (number_of_orders_from_visits / number_of_visits) * 100


"""====================================================================================================================
MARKETING METRICS
===================================================================================================================="""


def cpm(total_cost, total_recipients):
    """Return the CPM (or Cost per Mille) based on the marketing cost per 1000 customers.

    Args:
        total_cost (float): Total cost of marketing.
        total_recipients (int): Total number of marketing recipients.

    Returns:
        cpm (float) as total cost of marketing per 1000 customers.
    """

    return (total_cost / total_recipients) * 1000


def cpo(total_cost, total_transactions):
    """Return the CPT (Cost per Order).

    Args:
        total_cost (float): Total cost of marketing.
        total_transactions (int): Total number of transactions.

    Returns:
        cpt (float) as total cost per order
    """

    return total_cost / total_transactions


def cpa(total_cost, total_acquisitions):
    """Return the CPA (Cost per Acquisition).

    Args:
        total_cost (float): Total cost of marketing.
        total_acquisitions (int): Total number of acquisitions.

    Returns:
        cpt (float) as total cost per acquisition
    """

    return total_cost / total_acquisitions


def cpc(total_cost, total_clicks):
    """Return the CPC (Cost per Click).

    Args:
        total_cost (float): Total cost of marketing.
        total_clicks (int): Total number of clicks.

    Returns:
        cpt (float) as total cost per click
    """

    return total_cost / total_clicks


def conversion_rate(total_conversions, total_actions):
    """Return the conversion rate (CR) for an action.

    Args:
        total_conversions (int): Total number of conversions.
        total_actions (int): Total number of actions.

    Returns:
        conversion rate (float) percentage
    """

    return (total_conversions / total_actions) * 100


def lin_rodnitsky_ratio(avg_cost_per_conversion_all_queries,
                        avg_cost_per_conversion_queries_with_one_conversion_or_more):
    """Return the Lin-Rodnitsky Ratio describing the quality of paid search account managemnent.

    Args:
        avg_cost_per_conversion_all_queries (float): Average cost per conversion on the whole PPC account.
        avg_cost_per_conversion_queries_with_one_conversion_or_more (float): Average cost per conversion for only
        conversions where there was one or more conversions.

    Returns:
        Lin-Rodnitsky Ratio (float).

        1.0 to 1.5 - Account is too conservatively managed.
        1.5 to 2.0 - Account is well-managed.
        2.0 to 2.5 - Account is too aggressively managed.
        2.5 or more - Account is being mismanaged.
    """

    return avg_cost_per_conversion_all_queries / avg_cost_per_conversion_queries_with_one_conversion_or_more


def romi(total_revenue, total_marketing_costs):
    """Return the Return on Marketing Investment (ROMI).

    Args:
        total_revenue (float): Total revenue generated.
        total_marketing_costs (float): Total marketing costs

    Returns:
        Return on Marketing Investment (float) or (ROMI).
    """

    return ((total_revenue - total_marketing_costs) / total_marketing_costs) * 100


def roi(total_revenue, total_marketing_costs, total_other_costs):
    """Return the Return on Investment (ROI).

    Args:
        total_revenue (float): Total revenue generated.
        total_marketing_costs (float): Total marketing costs
        total_other_costs (float): Total other costs

    Returns:
        Return on Marketing Investment (float) or (ROMI).
    """

    total_costs = total_marketing_costs + total_other_costs
    return ((total_revenue - total_costs) / total_costs) * 100


def roas(total_revenue, total_marketing_costs):
    """Return the Return on Advertising Spend or ROAS.

    Args:
        total_revenue (float): Total revenue generated.
        total_marketing_costs (float): Total marketing costs

    Returns:
        Return on Advertising Spend or ROAS (float).
    """

    return total_revenue / total_marketing_costs


"""====================================================================================================================
CONTENT METRICS
===================================================================================================================="""


def focus_index(average_pages_visited_in_section, total_pages_in_section):
    """Return the focus index for a section of a website.

    Args:
        average_pages_visited_in_section (float): Average number of pages visited in this section of the website.
        total_pages_in_section (int): Total number of pages in this section of the website.

    Returns:
        Focus index as average_pages_visited_in_section / total_pages_in_section
    """

    return (average_pages_visited_in_section / total_pages_in_section) * 100


def stickiness(total_visits, total_visit_duration, total_users):
    """Return the stickiness score for a website or part of a website.

    Args:
        total_visits (int): Total number of visits to a website or a section of a website.
        total_visit_duration (int): Total number of minutes spent viewing the website or a section of a website.
        total_users (int): Total unique users who visited a website or section of a website.

    Returns:
        Stickiness score for website or part of website
    """

    frequency_of_visits = total_visits / total_users
    average_visit_duration = total_visit_duration / total_visits
    total_reach = total_users / total_visits

    return frequency_of_visits * average_visit_duration * total_reach


def sessions_with_product_views(total_sessions, sessions_with_product_views):
    """Return the percentage of sessions with product views during the period.

    Args:
        total_sessions (int): Total number of sessions within the period.
        sessions_with_product_views (int): Total number of sessions with product views within the period.

    Returns:
        Percentage (float) of positive reviews received.
    """

    return (sessions_with_product_views / total_sessions) * 100


"""====================================================================================================================
SOCIAL MEDIA METRICS
===================================================================================================================="""


def engagement_rate(followers_who_engaged, total_followers):
    """Return the engagement rate for a social media account.

    Args:
        followers_who_engaged (int): Total unique followers who engaged.
        total_followers (int): Total number of followers.

    Returns:
        Engagement rate (float) as followers_who_engaged / total_followers
    """

    return (followers_who_engaged / total_followers) * 100


"""====================================================================================================================
INVENTORY MANAGEMENT METRICS
===================================================================================================================="""


def dio(average_inventory_cost, cost_of_goods_sold):
    """Return the DIO or Days of Inventory Outstanding over the previous 365 days.

    Args:
        average_inventory_cost (float): Average cost of inventory.
        cost_of_goods_sold (float): Cost of goods sold.

    Returns:
        Days of Inventory Outstanding (float).
    """

    return (average_inventory_cost / cost_of_goods_sold) * 365


def safety_stock(max_units_sold_daily, avg_units_sold_daily, max_lead_time, avg_lead_time):
    """Returns the safety stock level for a given product based on sales and lead time.

    Args:
        max_units_sold_daily (int): Maximum number of units sold daily in previous period.
        avg_units_sold_daily (float): Average number of units sold daily in previous period.
        max_lead_time (int): Maximum number of days required to obtain stock.
        avg_lead_time (int): Average number of days required to obtain stock.

    Returns:
        Safety stock level for the product based on sales and lead time.
    """

    return (max_units_sold_daily * max_lead_time) - (avg_units_sold_daily * avg_lead_time)


def reorder_point(max_units_sold_daily, avg_units_sold_daily, max_lead_time, avg_lead_time, lead_time):
    """Returns the reorder point for a given product based on sales and lead time.

    The reorder point is the stock level at which a new order should be placed in order to avoid stock outs.

    Args:
        max_units_sold_daily (int): Maximum number of units sold daily in previous period.
        avg_units_sold_daily (float): Average number of units sold daily in previous period.
        max_lead_time (int): Maximum number of days required to obtain stock.
        avg_lead_time (int): Average number of days required to obtain stock.
        lead_time (int): Number of days required to obtain stock.

    Returns:
        Safety stock level for the product based on sales and lead time.
    """

    safety = safety_stock(max_units_sold_daily, avg_units_sold_daily, max_lead_time, avg_lead_time)
    return (lead_time * avg_units_sold_daily) + safety


def back_order_rate(total_back_orders, total_orders):
    """Return the back order rate for a period. Back orders are those that could not be shipped due to lack of stock.

    Args:
        total_back_orders (int): Total number of back orders.
        total_orders (int): Total number of orders.

    Returns:
        Back order rate (float).
    """

    return (total_back_orders / total_orders) * 100


def sales_velocity(units_sold_last_12m, number_of_days_in_stock, velocity_days=30):
    """Return the sales velocity of a product for a given number of days.

    Args:
        units_sold_last_12m (int): Total number of units sold in the past 12 months.
        number_of_days_in_stock (int): Total number of days in the past 12 months when product was in stock.
        velocity_days (int, optional): Number of days over which to measure sales velocity. Default 30.

    Returns:
        Sales velocity of product
    """

    return (units_sold_last_12m / number_of_days_in_stock) * velocity_days


def accuracy_of_forecast_demand(actual_demand, forecast_demand):
    """Return the accuracy of forecast demand.

    Args:
        actual_demand (int): Actual number of units of product sold within the period.
        forecast_demand (int): Number of units forecast to be demanded within the period.

    Returns:
        Accuracy of forecast demand.
    """

    return ((actual_demand - forecast_demand) / actual_demand) * 100


def eoq(demand_in_units, cost_of_ordering, cost_of_carrying):
    """Return the Economic Order Quantity (EOQ) for a product.

    Args:
        demand_in_units (int):
        cost_of_ordering (float):
        cost_of_carrying (float):

    Returns:
        Economic Order Quantity or EOQ (float).
    """

    return math.sqrt(((demand_in_units * cost_of_ordering) * 2) / cost_of_carrying)


"""====================================================================================================================
CUSTOMER SERVICE METRICS
===================================================================================================================="""


def csat(total_responses, positive_responses):
    """Return the Customer Satisfaction or CSAT score for a period.

    Args:
        total_responses (int): Total number of responses received within the period.
        positive_responses (int): Total number of positive responses received within the period.

    Returns:
        Percentage (float) of positive responses received.
    """

    return (positive_responses / total_responses) * 100


def nps(total_promoters, total_detractors, total_respondents):
    """Return the Net Promoter Score (NPS) for a period.

    Args:
        total_promoters (int): Total number of promoters (9 or 10 out of 10) within the period.
        total_detractors (int): Total number of detractors responses (1 to 6 out of 10) within the period.
        total_respondents (int): Total number of responses within the period.

    Returns:
        NPS score (float) based on the percentage of promoters - percentage detractors.
    """

    return ((total_promoters * 100) / total_respondents) - ((total_detractors * 100) / total_respondents)


def ticket_to_order_ratio(total_tickets, total_orders):
    """Returns the ratio of tickets to orders.

    Args:
        total_tickets (int): Total chats, emails, or tickets in the period.
        total_orders (int): Total orders in the period.

    Returns:
        Ratio of tickets to orders
    """

    return (total_tickets / total_orders) * 100


def average_tickets_to_resolve(total_tickets, total_resolutions):
    """Returns the average number of tickets required to resolve an issue.

    Args:
        total_tickets (int): Total chats, emails, or tickets in the period.
        total_resolutions (int): Total chats, emails, or tickets resolved in the period.

    Returns:
        Average number of tickets it takes to resolve an issue.
    """

    return total_tickets / total_resolutions


def time_to_resolve(time_received, time_resolved):
    """Returns the time taken to resolve an issue.

    Args:
        time_received (datetime): Datetime showing when ticket was received.
        time_resolved (datetime): Datetime showing when ticket was received.

    Returns:
        Time taken to resolve issue in hours.
    """

    time_received = datetime.strptime(time_received, "%Y-%m-%d %H:%M:%S")
    time_resolved = datetime.strptime(time_resolved, "%Y-%m-%d %H:%M:%S")
    time_to_resolve = ((time_resolved - time_received).seconds / 60) / 60

    return time_to_resolve



"""====================================================================================================================
OPERATIONS METRICS
===================================================================================================================="""


def service_level(orders_received, orders_delivered):
    """Return the inventory management service level metric, based on the percentage of received orders delivered.

    Args:
        orders_received (int): Orders received within the period.
        orders_delivered (int): Orders successfully delivered within the period.

    Returns:
        Percentage (float) of orders received that were delivered within th period.
    """

    return (orders_delivered / orders_received) * 100


def available_inventory_accuracy(counted_items, counted_items_that_match_record):
    """Return the Available Inventory Accuracy.

    Args:
        counted_items (int): Total items supposedly in the inventory according to the WMS.
        counted_items_that_match_record (int): Number of items were the WMS count matches the actual count.

    Returns:
        Percentage of available inventory that was correctly counted in the WMS.
    """

    return (counted_items_that_match_record / counted_items) * 100


def lost_sales_ratio(days_out_of_stock, days_in_period):
    """Returns the lost sales ratio for a product, representing the percentage of days in a period when it was OOS.

    Args:
        days_out_of_stock (int): Total days the product was out of stock.
        days_in_period (int): Total days in the period.

    Returns:
        Percentage of days in the period when the product was out of stock.
    """

    return (days_out_of_stock / days_in_period) * 100


