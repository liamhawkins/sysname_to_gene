import csv

with open("all_genes.csv", newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    file_count = 1
    data = []
    
    for row in csvreader:
        data.append(row[0])

    chunks = [data[x:x+1000] for x in range(0, len(data), 1000)]


    for subset in chunks:
        print(chunks.index(subset)+1)
        with open("./Output/" + str(chunks.index(subset)+1) + "_all_genes.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for gene in subset:
                writer.writerow([str(gene)])
            
