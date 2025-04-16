import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


pd.options.display.width = 0
pd.options.display.float_format = '{:.2f}'.format

sale_df = pd.read_csv('samsung_sale_dataset.csv')

# print(sale_df.head())
# print(sale_df.tail())
# print(sale_df.shape)
# print(sale_df.info())

# print(sale_df.isnull().sum())
# print(sale_df.duplicated().sum())
# sale_df = sale_df.drop_duplicates()
# print(sale_df.shape())

# print(sale_df.describe(include="all").map(lambda x: f"{x:.6f}" if isinstance(x, (int, float)) else x))
# sale_df = sale_df[sale_df['Market Share (%)'] >= 0]
# sale_df = sale_df[sale_df['5G Subscribers (millions)'] >= 0]
# sale_df = sale_df[sale_df['Regional 5G Coverage (%)'] <= 100]


# Which product model generates the highest revenue and sales volume overall?
highest_sales = pd.DataFrame(sale_df.groupby('Product Model')[['Units Sold', 'Revenue ($)']].sum())
highest_sales = highest_sales.sort_values(by='Units Sold', ascending=False)

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

# How have total revenue and units sold evolved year over year?
yearly_revenue = pd.DataFrame(sale_df.groupby('Year')[['Units Sold', 'Revenue ($)']].sum())

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

# How does product model performance vary across different regions?
regional_sales = sale_df.pivot_table(index='Region', columns='Product Model', values='Units Sold', aggfunc='sum', fill_value=0)

plt.figure(figsize=(10, 6))
sns.heatmap(regional_sales, annot=True, fmt=',.0f', cmap='YlGnBu', cbar_kws={'label': 'Units Sold'})
plt.title('Units Sold for Each Product by Region')
plt.xlabel('')
plt.ylabel('Region')
plt.tight_layout()
plt.show()

# What is the impact of 5G capability on product sales and revenue trends?
revenue_5G = pd.DataFrame(sale_df.groupby(['Year', '5G Capability'])['Revenue ($)'].sum())
ax = revenue_5G.unstack().plot(kind='line', marker='o', figsize=(10, 6))
plt.title('Revenue Trends by 5G Capability')
plt.xlabel('')
plt.ylabel('Revenue ($)')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.grid(True)
plt.legend(title='5G Capability')
plt.show()
