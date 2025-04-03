import time
import pandas as pd
import numpy as np
import psycopg2
import sqlalchemy
import matplotlib.pyplot as plt
import pyarrow.parquet as pq
import h5py

np.random.seed(42)
n_rows = 1_000_000
data = {
    'timestamp': pd.date_range(start='2023-01-01', periods=n_rows, freq='min'),
    'energy_consumption': np.random.rand(n_rows) * 100,
    'temperature': np.random.rand(n_rows) * 40 - 10,
    'humidity': np.random.rand(n_rows) * 100
}
df = pd.DataFrame(data)

def measure_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    return time.time() - start_time, result

csv_file = "energy_data.csv"
csv_write_time, _ = measure_time(df.to_csv, csv_file, index=False)
csv_read_time, _ = measure_time(pd.read_csv, csv_file)

parquet_file = "energy_data.parquet"
parquet_write_time, _ = measure_time(df.to_parquet, parquet_file, engine='pyarrow')
parquet_read_time, _ = measure_time(pd.read_parquet, parquet_file)

hdf5_file = "energy_data.h5"
hdf_write_time, _ = measure_time(df.to_hdf, hdf5_file, key='data', mode='w')
hdf_read_time, _ = measure_time(pd.read_hdf, hdf5_file)

engine = sqlalchemy.create_engine("postgresql+psycopg2://test:test1234@localhost/energdji")
sql_write_time, _ = measure_time(df.to_sql, 'energy_data', con=engine, if_exists='replace', index=False)
sql_read_time, _ = measure_time(pd.read_sql, 'SELECT * FROM energy_data', con=engine)

formats = ["CSV", "Parquet", "HDF5", "PostgreSQL"]
write_times = [csv_write_time, parquet_write_time, hdf_write_time, sql_write_time]
read_times = [csv_read_time, parquet_read_time, hdf_read_time, sql_read_time]

x = np.arange(len(formats))
width = 0.4

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, write_times, width, label='Час запису (сек)')
ax.bar(x + width/2, read_times, width, label='Час читання (сек)')

ax.set_xlabel("Формат збереження")
ax.set_ylabel("Час (секунди)")
ax.set_title("Порівняння швидкості обробки різних форматів")
ax.set_xticks(x)
ax.set_xticklabels(formats)
ax.legend()

plt.show()
