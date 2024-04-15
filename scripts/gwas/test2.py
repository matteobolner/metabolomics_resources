import pandas as pd
test=pd.read_table("data/gwas/gwas_with_kegg_compound_annotation.tsv")
test[['']]


test2=pd.read_excel("input/LW_5e05_genes_gwascatalog_MetabolonInfo_2.xlsx")
test2.columns



a=set(test2[test2['check_automatico_ricerca_trova']=='yes']['CHEMICAL_NAME'].unique())

b=set(test[test['chemical_name_in_annotation']]['CHEMICAL_NAME'])
a=set([i.rstrip("*") for i in a])
b.difference(a)
a.difference(b)





test=test[test['compound_name'].apply(len)>=3]
test[['compound_name']].drop_duplicates().to_csv("data/kegg/all_compounds_list.tsv", index=False, sep='\t')
