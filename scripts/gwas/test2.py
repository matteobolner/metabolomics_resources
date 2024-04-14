import pandas as pd
test=pd.read_table("data/kegg/compounds.tsv")
test=test[test['compound_name'].apply(len)>=3]
test[['compound_name']].drop_duplicates().to_csv("data/kegg/all_compounds_list.tsv", index=False, sep='\t')
