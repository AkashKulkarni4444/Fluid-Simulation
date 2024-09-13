# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the CSV data into a DataFrame
# df = pd.read_csv("infoResults.csv")

# # Convert time strings to numeric values (seconds)
# def time_str_to_seconds(time_str):
#     time_str = time_str.strip()
#     if time_str.endswith('ms'):
#         return float(time_str[:-3]) / 1000
#     elif time_str.endswith('s'):
#         return float(time_str[:-2])
#     else:
#         return None

# df['averageTimeTaken (s)'] = df['averageTimeTaken'].apply(time_str_to_seconds)
# df['standardDeviation (s)'] = df['standardDeviation'].apply(time_str_to_seconds)

# # Plotting
# plt.figure(figsize=(12, 8))

# # Scatter plot for average time taken
# for prog_type, marker in [('serial', 'o'), ('gpu', 's'), ('gpu_opt', '^')]:
#     subset = df[df['programmType'] == prog_type]
#     plt.scatter(subset['iterations'], subset['averageTimeTaken (s)'], label=prog_type, marker=marker)

# plt.xscale('log')  # Use log scale for x-axis (iterations)
# plt.yscale('log')  # Use log scale for y-axis (time)
# plt.xlabel('Iterations')
# plt.ylabel('Average Time Taken (seconds)')
# plt.title('Performance Comparison')
# plt.legend()

# plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
df = pd.read_csv("infoResults.csv")

# Convert time strings to numeric values (seconds)
def time_str_to_seconds(time_str):
    time_str = time_str.strip()
    if time_str.endswith('ms'):
        return float(time_str[:-3]) / 1000
    elif time_str.endswith('s'):
        return float(time_str[:-2])
    else:
        return None

df['averageTimeTaken (s)'] = df['averageTimeTaken'].apply(time_str_to_seconds)
df['standardDeviation (s)'] = df['standardDeviation'].apply(time_str_to_seconds)

# Plotting
plt.figure(figsize=(12, 8))

# Line plot for average time taken
for prog_type, linestyle in [('serial', '-'), ('gpu', '--'), ('gpu_opt', ':')]:
    subset = df[df['programmType'] == prog_type]
    plt.plot(subset['iterations'], subset['averageTimeTaken (s)'], label=prog_type, linestyle=linestyle)

plt.xscale('log')  # Use log scale for x-axis (iterations)
plt.yscale('log')  # Use log scale for y-axis (time)
plt.xlabel('Iterations')
plt.ylabel('Average Time Taken (seconds)')
plt.title('Performance Comparison')
plt.legend()

plt.show()
