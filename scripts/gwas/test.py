import pandas as pd

gwas=pd.read_excel("input/LW_5e05_genes_gwascatalog_MetabolonInfo.xlsx")

gwas=gwas[~gwas['CHEMICAL_NAME'].isna()]
gwas=gwas[['CHEM_ID','SUPER_PATHWAY','SUB_PATHWAY','CHEMICAL_NAME','HMDB','genes±500K','GWAScatalog']]
gwas=gwas[gwas['genes±500K']!='No_genes']
gwas=gwas[~gwas['GWAScatalog'].isna()]
gwas=gwas.drop(columns=['genes±500K'])
gwas=gwas.reset_index(drop=True)

#gwas.to_csv('data/gwas/gwas_single_gene_annotation.tsv', index=False, sep='\t')

#def fill_id(id):
#    while len(id)<5:
#        id="0"+id
#    return(id)

compounds=pd.read_table("data/kegg/compounds.tsv")
compounds=compounds[compounds['compound_name'].apply(len)>3]
compounds['compound_name']=compounds['compound_name'].str.lower()
compounds[['compound_name']].drop_duplicates().to_csv("data/kegg/all_compounds_list.tsv", index=False)


gwas['GWAScatalog']=gwas['GWAScatalog'].str.split("#")
gwas=gwas.explode("GWAScatalog")
gwas['gene_name']=gwas['GWAScatalog'].str.split(":").str[0]
gwas['annotation']=gwas['GWAScatalog'].str.split(":").str[1::]
gwas['annotation']=gwas['annotation'].str.join(":")
gwas['annotation']=gwas['annotation'].str.split(";")
gwas=gwas.explode("annotation")
gwas=gwas.drop(columns=['GWAScatalog'])
gwas=gwas.reset_index(drop=True)
gwas['CHEMICAL_NAME']=gwas['CHEMICAL_NAME'].str.rstrip("*")
gwas['chemical_name_in_annotation']=gwas.apply(lambda row: row['CHEMICAL_NAME'] in row['annotation'], axis=1)

gwas.to_csv("data/gwas/gwas_single_gene_annotation.tsv", index=False, sep='\t')

gwas[['annotation']].drop_duplicates().to_csv("data/gwas/gwas_annotations_only.tsv")


compound_names_lower = {name.lower() for name in compounds['compound_name']}

def search_compounds(input_text):
    matching_compounds = [name for name in compound_names_lower if name in input_text.lower()]
    return (matching_compounds)


all_annotations=[i for i in gwas['annotation']]

ann={}

counter=0

len(gwas['annotation'].unique())

for i in gwas['annotation'].unique():
    counter+=1
    print(counter)
    i_lower = i.lower()
    matching_compounds = search_compounds(i)
    ann[i]=matching_compounds


gwas['KEGG_compounds']=gwas['annotation'].apply(lambda x:ann[x])

def filter_substrings(input_list):
    filtered_list = []
    for item in input_list:
        is_substring = False
        for other_item in input_list:
            if item != other_item and item in other_item:
                is_substring = True
                break
        if not is_substring:
            filtered_list.append(item)
    return filtered_list

gwas['KEGG_compounds']=gwas['KEGG_compounds'].apply(filter_substrings)

compounds_dict={i:j for i,j in zip(compounds['compound_name'], compounds['compound_ID'])}

def filter_ids(input_list):
    return list(set([compounds_dict[i] for i in input_list]))

gwas['KEGG_compound_ids']=gwas['KEGG_compounds'].apply(filter_ids)

gwas.to_csv("data/gwas/gwas_with_kegg_compound_annotation.tsv", sep='\t', index=False)
