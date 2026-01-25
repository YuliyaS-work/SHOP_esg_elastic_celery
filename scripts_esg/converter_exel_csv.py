import pandas as pd


df = pd.read_excel('../products/santeh.xls', engine='xlrd')
df.to_csv('../products/santeh.csv', index=False)