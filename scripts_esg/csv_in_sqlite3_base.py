import pandas as pd
import sqlite3


csv_path = r'/electro.csv'

# Название таблицы в базе данных
table_name = 'esg_electroproduct'

# Имена колонок в CSV, которые нужно взять
columns_in_csv = ['1', '2','3']

# Названия колонок в таблице SQLite, в которые вставляем (их порядок)
target_columns = ['code', 'title', 'rubric_id']

# Читаем только нужные колонки из CSV
df = pd.read_csv(csv_path, usecols=columns_in_csv)

# Подключение к базе
conn = sqlite3.connect('../db.sqlite3')
cursor = conn.cursor()

# Загрузка данных в таблицу (если таблица уже существует)
df.columns = target_columns  # переименовать колонки, чтобы они совпадали с таблицей

# Вставляем DataFrame в таблицу
df.to_sql(table_name, conn, if_exists='append', index=False)

conn.close()