import csv

genes = []

for x in range(1,3):
    with open("./split_files/" +str(x) + "_all_genes_genes.csv", newline='') as csvfile:
        csvreader =  csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            genes.append(row)

with open("./all_genes_annotated.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for gene in genes:
        writer.writerow(gene)
