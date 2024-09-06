#!/usr/bin/env python

import csv
import sys
from collections import defaultdict

# Read the CSV file
with open(sys.argv[1], 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Initialize a dictionary to store the sum of runtimes for each language
sums = defaultdict(float)
count = 0

# Calculate the sum of runtimes for each language
for row in data:
    count += 1
    for lang, runtime in row.items():
        if lang != 'Run':
            sums[lang] += float(runtime)

# Calculate averages for all languages
averages = {lang: total / count for lang, total in sums.items()}

# Get the average runtime for C
c_average = averages['c']

print("Ratios of average runtimes compared to C:")
for lang, average in averages.items():
    ratio = average / c_average
    print(f"{lang}: {ratio:.6f}")
