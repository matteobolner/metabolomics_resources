import pandas as pd


!!!
prova a estrarre nomi con nlp/spacy/ai prima di matchare
!!!


gwas=pd.read_table("data/gwas/gwas_with_kegg_compound_annotation.tsv")
kegg=pd.read_table("data/kegg/merged_pathways_and_compounds.tsv")

gwas['KEGG_compounds']=gwas['KEGG_compounds'].apply(eval)
gwas['KEGG_compound_ids']=gwas['KEGG_compound_ids'].apply(eval)


gwas=gwas[gwas['KEGG_compound_ids'].apply(len)>0]

def compounds_in_pathway(pathway, compounds):
    for i ii


gwas

gwas=gwas.explode(['KEGG_compound_ids'])



gwas=gwas.merge(kegg[['pathway_ID','compound_ID','pathway_name']], left_on='KEGG_compound_ids', right_on='compound_ID')
gwas
