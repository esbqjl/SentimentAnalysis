import csv

with open('freqs.tsv', 'r') as infile:
    reader = csv.reader(infile, delimiter='\t')
    lines = [line + [sum(float(val) for val in line[1:] if val) / (len(line) - 1)] 
             for line in reader]

with open('freqs-means.tsv', 'w') as outfile:
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerows(lines)

