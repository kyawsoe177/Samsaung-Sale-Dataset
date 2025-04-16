# Data Exploration
Let's have a look at the dataset using head() and tail() functions.

**sale_df.head()**

<img src="https://github.com/user-attachments/assets/ee2cbdf9-9ff0-4a56-a957-6f1b0ddd0fe7" alt="Top five rows" width="1000" height="150">

**sale_df.tail()**

<img src="https://github.com/user-attachments/assets/c227b70e-2d9e-41fc-beb8-0239e3cd0ce2" alt="Bottom five rows" width="1000" height="150">

You can easily tell that there are mix of categorical and numerical variables. Each row represents sales data and 5G specifications of a Samsung phone for each quarter of the year across different regions.

Next, we will use df.shape and df.info() to gather more details about the dataset.

**sale_df.shape**

<img src="https://github.com/user-attachments/assets/9d4533df-ffbc-4c66-a999-2957016fcbbe" alt="Rows and columns" width="90" height="25">

**sale_df.info()**

<img src="https://github.com/user-attachments/assets/b9d2fe55-effe-453f-bab2-ac26444d8df0" alt="Information" width="400" height="300">

There are 1,000 rows and 12 columns. The data type is accurate and corresponds appropriately to the given values.

# Data Cleaning

Prior to the analysis, we need to clean the data. In this process, we will focus on common issues like missing values and duplicate entries.

**sale_df.isnull().sum()**

<img src="https://github.com/user-attachments/assets/db59af2b-04bc-4981-b767-7efb18590a64" alt="Null values" width="200" height="300">

The results show that the dataset contains no null values.

**sale_df.duplicated().sum()**

<img src="https://github.com/user-attachments/assets/72c5ddc8-4daa-4d6c-8bf1-e3cb8f1c1f92" alt="Duplicated values" width="50" height="20">

Unexpectedly, there are 640 duplicates in the dataset. We are going to remove those for better result during the analysis.

**sale_df.drop_duplicates()** <br/>
**sale_df.shape**

<img src="https://github.com/user-attachments/assets/67dd401d-f5df-404c-b2e6-93ddedaa60d9" alt="New rows and cloumns" width="50" height="20">

After removing duplicates, the dataset now contains 360 rows.

# Descriptive Analysis

We use df.describe(include='all') to ensure that both numerical and categorical features are included in the output.

**sale_df.describe(include = "all")**

<img src="https://github.com/user-attachments/assets/f9696000-d3f5-40c8-9f02-6d1db2a8d32d" alt="Descriptive analysis" width="1000" height="180">

Surprisingly, we discovered negative values in 'Market Share' and '5G Subscribers,' which are not valid. Additionally, 'Regional 5G Coverage' exceeds 100%, which is unrealistic. We will remove these anomalies from the dataset.

**sale_df = sale_df[sale_df['Market Share (%)'] >= 0]** \
**sale_df = sale_df[sale_df['5G Subscribers (millions)'] >= 0]** \
**sale_df = sale_df[sale_df['Regional 5G Coverage (%)'] <= 100]**

<img src="https://github.com/user-attachments/assets/599bd94d-7f8a-4a03-8061-ec01db0a6716" alt="Drop negative values" width="1000" height="180">

'nan' values come from calculations of categorical values. Since they are not intended for calculations, we can ignore them for now.

With the insights provided from numerical values
- Q4 is the most active sales period.
- Galaxy A32 5G is the top-selling product.
- 5G adoption is strong but varies regionally.
- Revenue and sales fluctuate significantly, suggesting product-specific demand.

# Exploratory Data Analysis
## Which product model generates the highest revenue and sales volume overall?

```
highest_sales = pd.DataFrame(sale_df.groupby('Product Model')[['Units Sold', 'Revenue ($)']].sum())
highest_sales = highest_sales.sort_values(by='Units Sold', ascending=False)
```

 <img src="https://github.com/user-attachments/assets/f9668cdd-8418-450f-aa40-79ee2d4f60ef" alt="Hightest sale" width="300" height="350"> 

```
fig, ax1 = plt.subplots(figsize=(14, 6))
plot_df = highest_sales.reset_index()
x = np.arange(len(plot_df['Product Model']))

color = 'tab:blue'
ax1.set_ylabel('Units Sold', color=color)
ax1.bar(x - 0.2, plot_df['Units Sold'], width=0.4, label='Units Sold', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(x)
ax1.set_xticklabels(plot_df['Product Model'], rotation=45, ha='right')

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Revenue ($)', color=color)
ax2.bar(x + 0.2, plot_df['Revenue ($)'], width=0.4, label='Revenue ($)', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))

plt.title('Comparison of Units Sold and Revenue per Product Model')
plt.tight_layout()
plt.show()
```

<img src="https://github.com/user-attachments/assets/18422efb-77f5-4235-8096-38e82eba8170" alt="Hightest sale" width="700" height="400"> 

<p align="justify">Galaxy S22 5G has the highest revenue per unit ($1,176.89). Higher sales generally mean higher revenue, but pricing significantly influences total revenue. For example, Galaxy S23 5G generates more revenue than models with higher sales, showing the power of premium pricing.</p>

## How have total revenue and units sold evolved year over year?

```
yearly_revenue = pd.DataFrame(sale_df.groupby('Year')[['Units Sold', 'Revenue ($)']].sum())
```

<img src="https://github.com/user-attachments/assets/68a820d9-7ff5-485b-b2e1-4d040cf684b9" alt="Yearly Revenue" width="200" height="150"> 

```
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.set_ylabel('Units Sold', color='tab:blue')
ax1.plot(yearly_revenue.index, yearly_revenue['Units Sold'], marker='o', linestyle='-', color='tab:blue', label='Units Sold')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))

ax2 = ax1.twinx()
ax2.set_ylabel('Revenue ($)', color='tab:red')
ax2.plot(yearly_revenue.index, yearly_revenue['Revenue ($)'], marker='s', linestyle='--', color='tab:red', label='Revenue ($)')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
fig.tight_layout()
plt.title('Total Units Sold and Revenue Over Years')
plt.show()
```

<img src="https://github.com/user-attachments/assets/20a6947e-55f8-4430-b035-ca58b1eb4528" alt="Yearly Revenue" width="700" height="400"> 

<p align="justify"> 2023 may reflect a failed strategy (high volume, low margins). Revenue rebounded to the highest level despite lower units sold than 2020-2023. <br/>
Investigate 2022–2023: Why did high sales volume not translate to revenue? (e.g., over-discounting, operational costs?)
Leverage 2024’s Success: Identify what drove higher revenue/unit (e.g., premium offerings, efficiency gains).</p>

## How does product model performance vary across different regions?

```
regional_sales = sale_df.pivot_table(index='Region', columns='Product Model', values='Units Sold', aggfunc='sum', fill_value=0)
```

<img src="https://github.com/user-attachments/assets/96ed1a9b-852a-4d51-893a-cceb0c633b85" alt="Regional sale" width="1000" height="130">

```
plt.figure(figsize=(10, 6))
sns.heatmap(regional_sales, annot=True, fmt=',.0f', cmap='YlGnBu', cbar_kws={'label': 'Units Sold'})
plt.title('Units Sold for Each Product by Region')
plt.xlabel('')
plt.ylabel('Region')
plt.tight_layout()
plt.show()
```

<img src="https://github.com/user-attachments/assets/05062242-a29d-416c-a189-f1f7a463de39" alt="Regional Sale" width="700" height="400"> 

<p align="justify">North America and Latin America seem to have the highest sales volumes overall, as indicated by the darkest blue shades.
The Galaxy Note series has lower sales compared to other flagship models. Premium models (S series, Z series) are more successful in North America and Latin America. Mid-range models (A series) perform well across all regions, making them a key segment to focus on.</p>

## What is the impact of 5G capability on product sales and revenue trends?

```
revenue_5G = pd.DataFrame(sale_df.groupby(['Year', '5G Capability'])['Revenue ($)'].sum())
```

<img src="https://github.com/user-attachments/assets/05ab1c84-e4a8-434c-8cff-5e341e9a0ea5" alt="Revenue 5G" width="280" height="250">

```
ax = revenue_5G.unstack().plot(kind='line', marker='o', figsize=(10, 6))
plt.title('Revenue Trends by 5G Capability')
plt.xlabel('')
plt.ylabel('Revenue ($)')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.grid(True)
plt.legend(title='5G Capability')
plt.show()
```

<img src="https://github.com/user-attachments/assets/055145fd-497a-4ac8-ac0b-ec74d27ac7b8" alt="Revenue 5G" width="700" height="400">

<p align="justify">
Investing in 5G-capable products continues to be a high-revenue strategy. Non-5G demand still exists, possibly in emerging markets or lower-income segments—worth supporting as a secondary revenue stream.
</p>
