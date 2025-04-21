import re
import pandas as pd
import numpy as np

def parse_ycsb_log(log_file_path):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    test_runs = []

    title_pattern = re.compile(r'-- (.*?) --')

    metrics_patterns = {
        'Record Count': re.compile(r'\[Record Count\], (\d+)'),
        'Total Ops': re.compile(r'\[Total Ops\], (\d+)'),
        'RunTime': re.compile(r'\[OVERALL\], RunTime\(ms\), (\d+)'),
        'Throughput': re.compile(r'\[OVERALL\], Throughput\(ops/sec\), (\d+\.\d+)'),
        'GC Young (%)': re.compile(r'\[TOTAL_GC_TIME_%_G1_Young_Generation\], Time\(%\), (\d+\.\d+)'),
        'GC Old (%)': re.compile(r'\[TOTAL_GC_TIME_%_G1_Old_Generation\], Time\(%\), (\d+\.\d+)'),
        'Read Ops': re.compile(r'\[READ\], Operations, (\d+)'),
        'Read Latency': re.compile(r'\[READ\], AverageLatency\(us\), (\d+\.\d+)'),
        'Update Ops': re.compile(r'\[UPDATE\], Operations, (\d+)'),
        'Update Latency': re.compile(r'\[UPDATE\], AverageLatency\(us\), (\d+\.\d+)'),
    }

    current_test = {}
    for line in lines:
        title_match = title_pattern.match(line)
        if title_match:
            if current_test:
                test_runs.append(current_test)
            current_test = {}
        else:
            for metric, pattern in metrics_patterns.items():
                match = pattern.search(line)
                if match:
                    current_test[metric] = match.group(1)
        
        if len(current_test) == len(metrics_patterns):
            test_runs.append(current_test)
            current_test = {}
    
    df = pd.DataFrame(test_runs)

    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].apply(pd.to_numeric, errors='coerce')

    return df

log_file_path = "data_a.txt"
df = parse_ycsb_log(log_file_path)

df.to_csv('results_workload_a.csv', index=False)

print(df)
