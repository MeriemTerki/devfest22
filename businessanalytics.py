# -*- coding: utf-8 -*-
"""BusinessAnalytics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LJhA8NHfjsGC_1Frz9gg6V4m4TUi7Clx

### Objective:
There is an abundance of customer information and tools available to businesses in order to make informed business decision. In this project we followed a method to use customer data to grow a business using a combination of programming, data analysis, and machine learning.
"""

!pip install  plotly==5.11.0

"""### Data
This is a transactional data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based online retail. The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.

The dataset is available on Kaggle: [E-Commerce Data](https://https://www.kaggle.com/datasets/carrie1/ecommerce-data?resource=download)

## Step 1 - Key Performance Indicators
The first step is to understand the main metrics the business wants to track, depending on the company’s product, position, targets & more.

#### 1. Import Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np # linear algebra
import pandas as pd # data processing
import os # manipulate paths
from datetime import date # supplies classes for manipulating dates
from time import strftime # convert time to a string as specified by the format argument

import seaborn as sns # to create visualisations
import matplotlib.pyplot as plt
# %matplotlib inline
import plotly
import plotly.graph_objs as go
import cufflinks as cf

from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()
cf.go_offline()

import warnings # remove warning messages
warnings.filterwarnings('ignore')

"""## 2. Load and Read the Data"""

# input data file is available in the "../input/" directory.
for dirname, _, filenames in os.walk('/content/data.csv'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# read the data
df = pd.read_csv('/content/data.csv', encoding = "ISO-8859-1")
df

# print the columns names for each dataset
print("df columns:",list(df))

"""##### Data Dictionary
* InvoiceNo: the invoice number
* StockCode: the stock code of the product
* Description: the description of the product
* Quantity: the number of items purchased
* InvoiceDate: the date the order has been invoiced
* UnitPrice: the price per item
* CustomerID: the unique customer ID
* Country: the country from which the order has been placed

## 3. Basic Date Information
"""

# print the number of rows and columns
print("df shape:",df.shape)

# print the basic information: missing values and data types
df.info()

# print a summary of the data in df
df.describe()

"""##### Note:
It seems that we msising customers numbers, this may be because of guest checkout or error in the datas collection. There are also negative values in the Quantity and UnitPrice which suggests that the dataset includes refunds.
"""

# print the number of unique values in df objects
print('Number of unique values in InvoiceNo:',df.InvoiceNo.nunique())
print('Number of unique values in StockCode:',df.StockCode.nunique())
print('Number of unique values in Description:',df.Description.nunique())
print('Number of unique values in CustomerID:',df.CustomerID.nunique())
print('Number of unique values in Country:',df.Country.nunique())

# print the first 5 rows
df.head()

"""### 4. Data Cleaning"""

# converting the type of InvoiceDate feature from string to datetime.
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# creating YearMonth feature to simplify reporting and visualization
df['InvoiceYearMonth'] = df['InvoiceDate'].map(lambda date: 100*date.year + date.month).astype('category')

df.head()

"""### 5. Key Performance Indicators (KPIs)"""

import seaborn as sns
import matplotlib.pyplot as plt

# calculate Revenue for each row
df['Revenue'] = df['UnitPrice'] * df['Quantity']

# we look at the revenue by country
revenue_country = pd.DataFrame(df.groupby('Country')['Revenue'].agg(sum).sort_values(ascending=False)).reset_index()
x=revenue_country['Country']
y=revenue_country['Revenue']


fig, ax = plt.subplots(figsize=(40,40))
# x and y are lists
sns.barplot(x=x, y=y, color='goldenrod', ax=ax, label="Some Label")
ax.set_xlabel("Revenue")
ax.set_ylabel("Country")
ax.legend()
plt.show()

"""##### Note:
United Kingdom is the region that generates most of the company's revenue. For the purpose of this analysis, we will focus on UK customers.
"""

# creating a new dataframe with UK customers only
df_uk = df.query("Country=='United Kingdom'").reset_index(drop=True)
df_uk.shape

"""#### Monthly Revenue"""

# create a new dataframe with YearMonth and Revenue columns
revenue = df_uk.groupby(['InvoiceYearMonth'])['Revenue'].sum().reset_index()
revenue.head()

import seaborn as sns
sns.lineplot(data=revenue, x='InvoiceYearMonth', y='Revenue')

"""#### Note:

The chart above shows upward trend for the revenue generated up to the November 2011 (as the December data is incomplete). Up to August 2011, the business had a monthly revenue between 400K and 600K, since then, the business has seen its revenue dramatically increase reaching 1.2M in November 2011.
"""

# calculate the monthly growth
revenue['MonthlyGrowth'] = revenue['Revenue'].pct_change()

revenue.head()

# bar chart showing the monthly growth rate

fig, ax = plt.subplots(figsize=(10,10))
revenue['positive'] = revenue['MonthlyGrowth'] > 0

sns.barplot(x=revenue.query("InvoiceYearMonth < 201112")['InvoiceYearMonth'],
            y=round(revenue.query("InvoiceYearMonth < 201112")['MonthlyGrowth']*100,2), color='goldenrod', ax=ax, label="Some Label")
ax.set_xlabel("InvoiceYearMonth")
ax.set_ylabel("MonthlyGrowth")
ax.legend()
plt.show()

"""#### Note
* September was an outstanding months with almost 60% growth compared with the previous month. 
* November was also very good month with 46.2% growth. 
* March and May are both up by more than 30% but this may be explain by the poor performance of the previous months.

* January and April 2011 are poor performance months.
*  We will have to investigate the data to understand why.

### Monthly Active Customers
"""

# creating monthly active customers dataframe by counting unique Customer IDs
monthly_active = df_uk.groupby('InvoiceYearMonth')['CustomerID'].nunique().reset_index()
monthly_active.columns = ['InvoiceYearMonth','ActiveCustomers']

# print the dataframe
monthly_active

fig, ax = plt.subplots(figsize=(10,10))
# x and y are lists
sns.barplot(x=monthly_active.query("InvoiceYearMonth < 201112")['InvoiceYearMonth'], y=monthly_active.query("InvoiceYearMonth < 201112")['ActiveCustomers'], color='goldenrod', ax=ax, label="Some Label")
ax.set_xlabel("Active Customers")
ax.set_ylabel("InvoiceYearMonth")
ax.legend()
plt.show()

# calculate the monthly active customers rate: ACR
monthly_active['ActiveCustomersRate'] = monthly_active['ActiveCustomers'].pct_change()

# bar chart showing the monthly active customers rate
monthly_active['positive'] = monthly_active['ActiveCustomersRate'] > 0

fig, ax = plt.subplots(figsize=(10,10))
# x and y are lists
sns.barplot(x=monthly_active.query("InvoiceYearMonth < 201112")['InvoiceYearMonth'], y=round(monthly_active.query("InvoiceYearMonth < 201112")['ActiveCustomersRate']*100,2), color='goldenrod', ax=ax, label="Some Label")
ax.set_xlabel("monthly active customers rate")
ax.set_ylabel("InvoiceYearMonth")
ax.legend()
plt.show()

"""#### Note:
* In January the company lost almost 200 customers, going from 871 
* In December to 684 in January which represents -21.47% decrease. 
* Similarly, in April the business went from 923 customer to 817 which represents a decrease of 11.48%.

### Monthly Order Count
"""

# create a new dataframe for number of orders by using InvoiceNo feature
monthly_orders = df_uk.groupby('InvoiceYearMonth')['InvoiceNo'].nunique().reset_index()
monthly_orders.columns = ['InvoiceYearMonth','Orders']

# print the dataframe
monthly_orders

# plot showing monthly orders
import seaborn as sns
x_orders=monthly_orders.query("InvoiceYearMonth < 201112")['InvoiceYearMonth']
y_orders=monthly_orders.query("InvoiceYearMonth < 201112")['Orders']
sns.lineplot(data=monthly_orders, x=x_orders, y=y_orders)

# calculate the monthly orders rate
monthly_orders['OrdersRate'] = monthly_orders['Orders'].pct_change()

# bar chart showing the monthly orders rate
monthly_orders['positive'] = monthly_orders['OrdersRate'] > 0

fig, ax = plt.subplots(figsize=(10,10))
x=monthly_orders.query("InvoiceYearMonth < 201112")['InvoiceYearMonth']
y=round(monthly_orders.query("InvoiceYearMonth < 201112")['OrdersRate']*100,2)

sns.barplot(x=x, y=y, color='goldenrod', ax=ax, label="Some Label")
ax.set_xlabel("InvoiceYearMonth")
ax.set_ylabel("Monthly Orders Rate")
ax.legend()
plt.show()

"""#### Note:
The number of orders has been decreasing between December and February going from 1,885 to 1,259 orders representing -33.21% decrease. The orders went up until May growing by 56.71%. The orders dropped again until August by -27.72% and finally took up to November by 50.34%.

### Average Order Value
"""

# create a new dataframe for average average order value
monthly_aov = df_uk.groupby(['InvoiceYearMonth','InvoiceNo'])['Revenue'].sum().reset_index() # group revenue by invoice to get the order value 
monthly_aov = monthly_aov.groupby('InvoiceYearMonth')['Revenue'].mean().reset_index() # calculate the average order value
monthly_aov.columns = ['InvoiceYearMonth','AOV']

#print the dataframe
monthly_aov

# plot showing monthly orders
import seaborn as sns
x_order_value=monthly_aov.query("InvoiceYearMonth < 201112")['InvoiceYearMonth']
y_order_value=round(monthly_aov.query("InvoiceYearMonth < 201112")['AOV'],2)
sns.scatterplot(data=monthly_aov, x=x_order_value, y=y_order_value)

"""### Note:
Between December and April the company's AVG lost 24.05%, it went back up until September going from £272.66 in April to £412.45 in September which represents an increase of 51.27%. the month of October registered a decrease (-9.89) to go back to almost the AVG as September's one in November (£412.08 which represents 10.88% increase compared with October's AVG.

### New Customer Ratio

A new customer is a customers that purchased for the first time within a period of time defined by the business. For the purpose of this analysis, a new customer is the first time a customerID appears in the dataset, this means that all the customers for December 2010 will be classed as new customers.
"""

# create a dataframe contaning CustomerID and first purchase date
first_order = df_uk.groupby('CustomerID').InvoiceDate.min().reset_index()
first_order.columns = ['CustomerID','FirstOrder']
first_order['FirstOrder'] = first_order['FirstOrder'].map(lambda date: 100*date.year + date.month)

# merge first purchase date column to our main dataframe (df_uk)
df_uk = pd.merge(df_uk, first_order, on='CustomerID')

#create a column called UserType
df_uk['UserType'] = 'New'
df_uk.loc[df_uk.InvoiceYearMonth != df_uk.FirstOrder,"UserType"] = 'Existing'

df_uk.head()

# create a dataframe to show the new customer ratio
new_customer_ratio = df_uk.query("UserType == 'New'").groupby(['InvoiceYearMonth'])['CustomerID'].nunique()/df_uk.query("UserType == 'Existing' or UserType == 'New'").groupby(['InvoiceYearMonth'])['CustomerID'].nunique()
new_customer_ratio = new_customer_ratio.reset_index()
new_customer_ratio = new_customer_ratio.dropna()

new_customer_ratio.columns = ['InvoiceYearMonth','NewCustomerRatio']
# print the dafaframe
new_customer_ratio

# plot showing monthly new customer ratio
fig, ax = plt.subplots(figsize=(10,10))
### New Customer Ratio
x_customer_ratio=new_customer_ratio.query("InvoiceYearMonth != 201112 and InvoiceYearMonth != 201012")['InvoiceYearMonth']
y_customer_ratio=round(new_customer_ratio.query("InvoiceYearMonth != 201112 and InvoiceYearMonth != 201012")['NewCustomerRatio'],2)

sns.barplot(x=x, y=y, color='goldenrod', ax=ax, label="Some Label")
ax.set_xlabel("X-Label")
ax.set_ylabel("Y-Label")
ax.legend()
plt.show()

"""### Note:
As expected the new customer ratio declines over the year as we assumed that all the customers in December 2010 were new ones. (we assumed on Feb, all customers were New). For the last six months of the year, the new customer ratio is of about 20%.

### Retention Rate
Retention rate the percentage of customers a business has retained over a given time period. It is a very important KPI and should be monitored very closely because it indicates how good of a job the marketing and sales teams are doing. It is also cost effective to focus on keeping the retention rate up because it requires more time, money and effort to convince and convert someone new to make a purchase or sign up for a services rather than keeping your existing customers that already know the business.

Fot the purpose of this analysis, we are going to calculate the monthly retention rate
"""

# identify which customers are active by looking at their revenue per month
customer_purchase = df_uk.groupby(['CustomerID','InvoiceYearMonth'])['Revenue'].sum().dropna().reset_index()
customer_purchase['CustomerID'] = customer_purchase['CustomerID'].astype(int).astype('category')
customer_purchase

# change customer_purchase from long to wide dataframe
df_retention = pd.crosstab(customer_purchase['CustomerID'], customer_purchase['InvoiceYearMonth'].astype(str), dropna=False).reset_index()
df_retention.head()

# count of total customers each months
total_customers = {}

for column in df_retention.loc[:, df_retention.columns != 'CustomerID'].columns:
    # count the total number of customers for each months
    TotalCustomers = df_retention[column].sum()
    # store the results
    total_customers[column] = (TotalCustomers)

# create a data frame
total_customers = pd.DataFrame(total_customers.items(), columns=['InvoiceYearMonth', 'TotalCustomers'])
total_customers

# count of total returning customers each months
returning_customers = {}

for i in range(0,12,1):
    # count the total number of returning customers for each months
    columns_selection = df_retention.iloc[:, (1+i):(3+i)]
    ReturningCustomers = np.where((columns_selection.iloc[:, 0] == 1) & (columns_selection.iloc[:, 1] == 1), 1, 0)
    # store the results
    returning_customers[i] = (ReturningCustomers.sum())
    
    
# create a data frame
returning_customers = pd.DataFrame(returning_customers.items(), columns=['index', 'ReturningCustomers']).drop(['index'], axis=1)
# create a row to account for the month of December 2010
new_row = pd.DataFrame({'ReturningCustomers': [np.nan]})
# add the new row to retention dataframe 
returning_customers = pd.concat([new_row, returning_customers]).reset_index(drop = True) 
returning_customers

# add the total number of customers ech month to the retention dataframe
retention = pd.merge(total_customers, returning_customers, left_index=True, right_index=True)

# calculate the retention rate
retention['RetentionRate'] = retention['ReturningCustomers']/retention['TotalCustomers']

retention

# plot showing monthly retention rate
x_retention=retention.query("InvoiceYearMonth != '201112' and InvoiceYearMonth != '201012'")['InvoiceYearMonth']
y_retention=round(retention.query("InvoiceYearMonth != '201112' and InvoiceYearMonth != '201012'")['RetentionRate'],2)
line = sns.lineplot(x=x_retention, 
                    y= y_retention, 
                    data=retention)

"""### Note:
maybe it doesn't effect the growth

### Retentention by Cohort
"""

# define the cohort_period function
def cohort_period(df):
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the cutsomer's first order.
    
    Example
    -------
    Get the 3rd month for every customer:
        df.sort(['CustomerID', 'InvoiceNo', inplace=True)
        df = df.groupby('CustomerID').apply(cohort_period)
        df[df.CohortPeriod == 3]
    """
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

# creating a new dataframe grouped by FirstOrder and InvoiceYearMonth 
df_cohort = df_uk.groupby(['FirstOrder','InvoiceYearMonth'])

# count the unique customerID
df_cohort = df_cohort.agg({'CustomerID': pd.Series.nunique})

# make the column name more meaningful
df_cohort.rename(columns={'CustomerID': 'Nb_Customers'}, inplace=True)

# apply the cohort_period() function to df_cohort
df_cohort = df_cohort.groupby(level=0).apply(cohort_period)
df_cohort.head()

# create cohort based retention table
cohorts = df_cohort['Nb_Customers'].unstack(0)

# create a serie holding the total number of customers for each CohortGroup
cohort_group_size = df_cohort['Nb_Customers'].groupby(level=0).first()

# create a new dataframe containing the percentage of customers from the cohort purchasing within the given period
cohort_retention = df_cohort['Nb_Customers'].unstack(0).divide(cohort_group_size, axis=1)

# plot showing cohort retention rate
sns.set(style='white')
plt.figure(figsize=(12, 8))
plt.title('Customers Cohorts Retention')
sns.heatmap(cohort_retention.T, mask=cohort_retention.T.isnull(), annot=True, fmt='.0%')

"""### Note:
Ove the year the company retained 27% of its customers.
"""