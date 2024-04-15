import pandas as pd

#gwas=pd.read_excel("input/LW_5e05_genes_gwascatalog_MetabolonInfo.xlsx")
gwas=pd.read_excel(snakemake.input.gwas)
gwas=gwas[~gwas['CHEMICAL_NAME'].isna()]
gwas=gwas[['CHEM_ID','SUPER_PATHWAY','SUB_PATHWAY','CHEMICAL_NAME','HMDB','genes±500K','GWAScatalog','rs']]
gwas=gwas[gwas['genes±500K']!='No_genes']
gwas=gwas[~gwas['GWAScatalog'].isna()]
gwas=gwas.drop(columns=['genes±500K'])
gwas=gwas.reset_index(drop=True)

compounds=pd.read_table(snakemake.input.compounds)
compounds=compounds[compounds['compound_name'].apply(len)>3]
compounds['compound_name']=compounds['compound_name'].str.lower()


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
gwas['chemical_name_in_annotation']=gwas.apply(lambda row: row['CHEMICAL_NAME'].lower() in row['annotation'].lower(), axis=1)
#gwas.to_csv("data/gwas/gwas_single_gene_annotation.tsv", index=False, sep='\t')
#gwas[['annotation']].drop_duplicates().to_csv("data/gwas/gwas_annotations_only.tsv")

compound_names_lower = {name.lower() for name in compounds['compound_name']}

def search_compounds(input_text):
    matching_compounds = [name for name in compound_names_lower if name in input_text.lower()]
    return (matching_compounds)

all_annotations=[i for i in gwas['annotation']]

ann={}

counter=0

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

#gwas.to_csv("data/gwas/gwas_with_kegg_compound_annotation.tsv", sep='\t', index=False)
gwas.to_csv(snakemake.output.annotated_gwas, sep='\t', index=False)
