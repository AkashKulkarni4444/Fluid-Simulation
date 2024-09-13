import pstats

# Load the profiling data from results.prof
profiler_stats = pstats.Stats('results.prof')

# Sort statistics by cumulative time
profiler_stats.sort_stats('cumulative')

# Dump the sorted statistics to a binary file
dump_file_path = 'sorted_results.prof'
profiler_stats.dump_stats(dump_file_path)

# Load the dumped statistics
sorted_stats = pstats.Stats(dump_file_path)

# Open a file for writing the sorted profiling results
output_file_path = 'results.txt'
with open(output_file_path, 'w') as output_file:
    # Redirect the output to the file
    sorted_stats.print_stats(stream=output_file)

print(f"Profiling results have been saved to {output_file_path}")
