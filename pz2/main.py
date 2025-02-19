# Варіант 21. Аналіз розподілу даних. Використайте pd.qcut() для поділу даних на квантилі, проаналізуйте розподіл.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 10**6  # 1 мільйон записів
data = {
    'id': np.arange(n),
    'value': np.random.rand(n) * 1000,
    'category': np.random.choice(['A', 'B', 'C', 'D'], size=n)
}
df = pd.DataFrame(data)

df['category'] = df['category'].astype('category')

def categorize(value):
    if value < 250:
        return 'low'
    elif value < 750:
        return 'medium'
    else:
        return 'high'

df['value_category'] = df['value'].apply(categorize)

bins = [0, 250, 750, 1000]
labels = ['low', 'medium', 'high']
df['value_category_vec'] = pd.cut(df['value'], bins=bins, labels=labels)

quantiles = pd.qcut(df['value'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
df['quantile'] = quantiles

print(df['quantile'].value_counts())

print(df['value'].describe())

print(df['quantile'].value_counts(normalize=True))

df['value'].hist(bins=50)
plt.title("Гістограма значень")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

df['quantile'].value_counts().plot(kind='bar')
plt.title("Розподіл квантилів")
plt.xlabel("Quantile")
plt.ylabel("Count")
plt.show()
