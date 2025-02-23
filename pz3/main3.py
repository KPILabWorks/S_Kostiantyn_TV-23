import pyarrow.csv as pc
import pyarrow.compute as pcpt
import pyarrow as pa
import time
import psutil
import os
import pandas as pd
import numpy as np


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 2)


def generate_large_energy_file(file_path, num_rows=10 ** 7):
    df = pd.DataFrame({
        "timestamp": pd.date_range(start="2023-01-01", periods=num_rows, freq="min"),
        "energy_consumption": np.random.uniform(100, 1000, num_rows)
    })
    df.to_csv(file_path, index=False)
    print(f"Згенеровано файл: {file_path} з {num_rows} рядками.")


def process_large_table(file_path):
    start_time = time.time()
    start_mem = get_memory_usage()

    read_options = pc.ReadOptions(use_threads=True, block_size=10 ** 6)
    convert_options = pc.ConvertOptions(column_types={"energy_consumption": pa.float64()})

    table = pc.read_csv(file_path, read_options=read_options, convert_options=convert_options)

    avg_consumption = pcpt.mean(table["energy_consumption"])

    end_time = time.time()
    end_mem = get_memory_usage()

    print(f"Середнє енергоспоживання: {avg_consumption.as_py()}")
    print(f"Час виконання: {end_time - start_time:.2f} сек")
    print(f"Використана пам'ять: {end_mem - start_mem:.2f} МБ")

file_path = "large_energy_data.csv"
generate_large_energy_file(file_path)

process_large_table(file_path)
