import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("--- Cafe Sales Analysis ---")

try:
    df = pd.read_csv('cafe_sales.csv')
except FileNotFoundError:
    print("Error: 'cafe_sales.csv' not found. Make sure it's in the same directory.")
    exit()

print("\n[1] Initial Data (First 5 Rows):")
print(df.head())
print("\n[2] Initial Data Info:")
df.info()


print("\n[3] Cleaning Data...")

df['ItemName'] = df['ItemName'].str.strip().str.lower()
df['Category'] = df['Category'].str.strip().str.lower()


df['QuantitySold'] = pd.to_numeric(df['QuantitySold'], errors='coerce')


print("\nMissing values before cleaning:")
print(df.isnull().sum())


median_quantity = np.nanmedian(df['QuantitySold'])
df['QuantitySold'].fillna(median_quantity, inplace=True)


df['QuantitySold'] = df['QuantitySold'].astype(int)


df['CalculatedSale'] = df['UnitPrice'] * df['QuantitySold']


discrepancies = df[np.abs(df['TotalSale'] - df['CalculatedSale']) > 0.01]
if not discrepancies.empty:
    print("\nFound and fixed calculation errors in 'TotalSale':")
    print(discrepancies[['Date', 'ItemName', 'TotalSale', 'CalculatedSale']])


df['TotalSale'] = df['CalculatedSale']
df.drop(columns=['CalculatedSale'], inplace=True)


df['Date'] = pd.to_datetime(df['Date'])

print("\n[4] Cleaned Data Info:")
df.info()
print("\nCleaned Data (First 5 Rows):")
print(df.head())



print("\n[5] Performing Data Analysis...")


total_revenue = np.sum(df['TotalSale'])
print(f"\nTotal Revenue: ${total_revenue:.2f}")


best_selling_item = df.groupby('ItemName')['QuantitySold'].sum().idxmax()
print(f"Best-Selling Item (by quantity): {best_selling_item.title()}")


sales_by_category = df.groupby('Category')['TotalSale'].sum()
print("\nTotal Sales by Category:")
print(sales_by_category)



print("\n[6] Generating Visualizations...")


plt.figure(figsize=(10, 6))
sales_by_category.plot(kind='bar', color=['#4c72b0', '#55a868', '#c44e52', '#8172b2'])
plt.title('Total Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Total Revenue ($)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()


item_quantities = df.groupby('ItemName')['QuantitySold'].sum()
plt.figure(figsize=(10, 8))
plt.pie(item_quantities, labels=item_quantities.index.str.title(), autopct='%1.1f%%', startangle=140,
        wedgeprops={'edgecolor': 'black'})
plt.title('Proportion of Total Items Sold')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()



daily_sales = df.groupby('Date')['TotalSale'].sum()
plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales.values, marker='o', linestyle='-', color='green')
plt.title('Total Daily Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Revenue ($)')
plt.grid(True)
plt.ylim(bottom=0) # Start y-axis at 0
plt.tight_layout()

plt.show()

print("\n--- Analysis Complete ---")