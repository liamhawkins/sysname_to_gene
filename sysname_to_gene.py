import csv
from collections import OrderedDict
from Bio import Entrez
import urllib

FILE_LIST = ["heart_up", "kidney_down", "kidney_up", "liver_down", "liver_up", "lung_down", "lung_up", "muscle_down", "muscle_up"]
Entrez.email = "liam.hawkins@carleton.ca"

def read_file(file):
    sys_names_list = []
    with open(file + ".csv", newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            sys_names_list.append(row[0])
    return sys_names_list

def search_ids(sys_list, file):
    id_dict = OrderedDict()
    gene_num = 1
    for sys_name in sys_list:


        while True:
            try:
                print("{}/{}:{} - searching for {}".format(gene_num, len(sys_list), file, sys_name))
                esearch_result = Entrez.esearch(db="gene", term=sys_name, retmod="xml")
            except (TimeoutError, urllib.error.URLError) as e:
                print("Timed-out Trying Again")
                continue
            break
        
        parsed_result = Entrez.read(esearch_result)
        gene_num += 1
        if len(parsed_result['IdList']) == 0:
            continue
        else:        
            id_dict[sys_name] = parsed_result['IdList'][0]

    return id_dict

def fetch_genes(id_dict):
    print("Fetching Genes")
    request = Entrez.read(Entrez.epost(db="gene", id=",".join(list(id_dict.values()))))
    webenv = request['WebEnv']
    querykey = request['QueryKey']
    efetch_result = Entrez.efetch(db="gene", webenv=webenv, query_key=querykey, retmode="xml")
    genes = Entrez.read(efetch_result)

    for gene in genes:
        query_gene_id = gene['Entrezgene_track-info']['Gene-track']['Gene-track_geneid']
        for sys_name, gene_id in id_dict.items():
            if gene_id == query_gene_id:
                id_dict[sys_name] = [id_dict[sys_name]] # convert to list so entrez result can be appending in dictionary
                id_dict[sys_name].append(gene)

    return id_dict

def parse_genes(id_dict):
    print("Parsing Genes")
    for sys_name in id_dict:
        gene_name = id_dict[sys_name][1]['Entrezgene_gene']['Gene-ref']['Gene-ref_locus']
        try:
            gene_mrna = id_dict[sys_name][1]['Entrezgene_locus'][0]['Gene-commentary_products'][0]['Gene-commentary_accession']
        except KeyError:
            gene_mrna = "NOTFOUND"
        try:
            gene_protein = id_dict[sys_name][1]['Entrezgene_locus'][0]['Gene-commentary_products'][0]['Gene-commentary_products'][0]['Gene-commentary_accession']
        except KeyError:
            gene_protein = "NOTFOUND"

        id_dict[sys_name] = id_dict[sys_name][:-1]
        id_dict[sys_name].extend([gene_name, gene_mrna, gene_protein])

    return id_dict

def write_file(file, sys_names_list, id_dict):
    with open(file + "_genes.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["SystematicName", "GeneID", "GeneName", "mRNA Accession", "Protein Accession"])

        for sys_name in sys_names_list:
            if sys_name in id_dict:
                writer.writerow([sys_name] + id_dict[sys_name])
            else:
                writer.writerow([sys_name, "NO RESULTS"])

        print("DONE")


if __name__ == "__main__":   

    for file in FILE_LIST:    
        sys_names_list = read_file(file)
        id_dict = search_ids(sys_names_list, file)
        id_dict = fetch_genes(id_dict)
        id_dict = parse_genes(id_dict)
        write_file(file, sys_names_list, id_dict)
