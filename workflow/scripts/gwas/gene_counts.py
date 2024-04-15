import pandas as pd

gwas=pd.read_table("data/gwas/LW/gwas_with_kegg_compounds.tsv")
excel=pd.read_excel("input/LW_5e05_genes_gwascatalog_MetabolonInfo.xlsx")
excel['CHEMICAL_NAME']=excel['CHEMICAL_NAME'].str.rstrip("*")


gwas=gwas.merge(excel[['CHEMICAL_NAME','rs','p_wald']], on=['CHEMICAL_NAME','rs'], how='left')

identical=gwas[gwas['chemical_name_in_annotation']]
identical=identical[['SUPER_PATHWAY','SUB_PATHWAY','CHEMICAL_NAME','rs','gene_name','p_wald']]
identical=identical.drop_duplicates()
test=pd.DataFrame(identical[['gene_name','SUPER_PATHWAY','CHEMICAL_NAME']].value_counts())
test=test.reset_index()
test
test






identical['gene_name'].value_counts()
