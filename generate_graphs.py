import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

files = {
    "A": "./results_workload_a.csv",
    "B": "./results_workload_b.csv",
    "C": "./results_workload_c.csv",
    "D": "./results_workload_d.csv",
    "E": "./results_workload_e.csv",
    "F": "./results_workload_f.csv",
    "G": "./results_workload_insert.csv"
}

workloads = []
for label, file in files.items():
    df = pd.read_csv(file)
    df["Workload"] = label
    
    if label == "G":
        df["Avg Response Time (ms)"] = df["RunTime"] / df["Insert Ops"]
    else:
        df["Avg Response Time (ms)"] = df["RunTime"] / df["Total Ops"]

    df["Record Count"] = df["Record Count"].astype(int)
    workloads.append(df)

combined_df = pd.concat(workloads, ignore_index=True)
sns.set(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.lineplot(data=combined_df, x='Record Count', y='Avg Response Time (ms)', hue='Workload', marker='o')
plt.title("Figure 1: Avg. Response Time vs Record Count by Workload")
plt.xscale("log")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
for label, df in zip(files.keys(), workloads):
    if label == "G":
        sns.lineplot(data=df, x='Record Count', y='Insert Latency', label=f'Insert (G)', marker='o')
    elif "Update Latency" in df.columns:
        sns.lineplot(data=df, x='Record Count', y='Update Latency', label=f'Update ({label})', marker='o')
plt.title("Figure 2: Operation Latency vs Record Count")
plt.xscale("log")
plt.ylabel("Latency (μs)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=combined_df, x='Record Count', y='Throughput', hue='Workload', marker='o')
plt.title("Figure 3: Throughput vs Record Count by Workload")
plt.xscale("log")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=combined_df, x='Record Count', y='RunTime', hue='Workload', marker='o')
plt.title("Figure 4: Total Run Time vs Record Count by Workload")
plt.xscale("log")
plt.ylabel("Run Time (ms)")
plt.tight_layout()
plt.show()
