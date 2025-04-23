import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

distances_cm = [5, 10, 25, 50]
file_names = {5: 'RawData_5.csv', 10: 'RawData_10.csv', 25: 'RawData_25.csv', 50: 'RawData_50.csv'}

mean_fields = {}

for d in distances_cm:
    df = pd.read_csv(file_names[d])

    df.columns = df.columns.str.strip()

    df["Time (s)"] = df["Time (s)"].astype(float)
    df["Absolute field (µT)"] = df["Absolute field (µT)"].astype(float)

    mean_field = df["Absolute field (µT)"].mean()
    mean_fields[d] = mean_field

    plt.plot(df["Time (s)"], df["Absolute field (µT)"], label=f"{d} см (середнє: {mean_field:.2f} µT)")

plt.title("Абсолютне магнітне поле залежно від часу (ноутбук)")
plt.xlabel("Час (сек)")
plt.ylabel("Абсолютне магнітне поле (µT)")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sorted_d = sorted(mean_fields.items())
x = [item[0] for item in sorted_d]
y = [item[1] for item in sorted_d]

sns.lineplot(x=x, y=y, marker='o')
plt.title("Залежність середнього рівня магнітного поля від відстані (ноутбук)")
plt.xlabel("Відстань до наутбуку (см)")
plt.ylabel("Середнє абсолютне поле (µT)")
plt.grid(True)
plt.tight_layout()
plt.show()
