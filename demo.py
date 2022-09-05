#!/usr/bin/python3

import pandas as pd

print('\n\nreading demo_more.csv')
df = pd.read_csv('demo_more.csv')
print(df.dtypes)

print('\n\nreading demo_less.csv')
df = pd.read_csv('demo_less.csv')
print(df.dtypes)

print('\n\nreading demo_less.csv with new logic')
df = pd.read_csv('demo_less.csv', dtype=str).apply(pd.to_numeric, errors='ignore')
print(df.dtypes)
