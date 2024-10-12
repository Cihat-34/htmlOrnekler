
import pandas as pd
import numpy as np


# 'student_scores.csv' dosyasını okuma işlemi
df = pd.read_csv('C:\Users\FUJITSU\Desktop\CihatPython\student_scores.csv')

# DataFrame'i görüntüleme
print(df)

print(df.info())
print(df.describe())
print(df.head())

data = {
    'Branch': ['A', 'B', 'A', 'C', 'B', 'C'],
    'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02', '2023-01-01', '2023-01-02'],
    'Sales': [1500, 2000, 1800, 2500, 2200, 1900]
}
df = pd.DataFrame(data)
daily_average_sales = df.groupby('Branch')['Sales'].mean()
print("Şube bazında günlük ortalama satışlar:")
print(daily_average_sales)

total_sales_per_branch = df.groupby('Branch')['Sales'].sum()
print("Şube bazında toplam satış miktarları:")
print(total_sales_per_branch)