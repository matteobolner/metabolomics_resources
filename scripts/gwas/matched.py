import pandas as pd
import re

start_pattern = "\x1b[01;31m\x1b[K"
end_pattern = "\x1b[m\x1b[K"

def extract_all_between_patterns(text, start_pattern, end_pattern):
    pattern = re.compile(f'{re.escape(start_pattern)}(.*?){re.escape(end_pattern)}')
    matches = pattern.findall(text)
    return matches

colored=pd.read_table("data/gwas/matches_colored.txt", header=None)
colored.columns=['string']
colored['matches']=colored['string'].apply(lambda x:extract_all_between_patterns(x, start_pattern, end_pattern))

normal=pd.read_table("data/gwas/matches_non_colored.txt", header=None)

normal.columns=['annotation_lc']
matches=pd.concat([normal, colored], axis=1)

matches=matches.drop(columns='string')

testdict={i:j for i,j in zip(matches['annotation_lc'], matches['matches'])}


gwas=pd.read_table("data/gwas/gwas_single_gene_annotation.tsv")

gwas['annotation_lc']=gwas['annotation'].str.lower()



excel=pd.read_excel("input/LW_5e05_genes_gwascatalog_MetabolonInfo.xlsx")

gwas[gwas['annotation_lc'].str.contains("1-stearoyl-2-dihomo-linol")]

gwas['KEGG_compounds']=gwas['annotation_lc'].apply(lambda x:testdict[x])
