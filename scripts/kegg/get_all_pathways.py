import requests
import pandas as pd
from io import StringIO

def get_df_kegg(url, sep='\t'):
    data=requests.get(url)
    if len(data.text)==1:
        raise ValueError("No data found")
    if sep=='whitespace':
        pathways=pd.read_table(StringIO(data.text), header=None, delim_whitespace=True)
    else:
        pathways=pd.read_table(StringIO(data.text), header=None, sep=sep)
    return(pathways)

pathways=get_df_kegg('http://rest.kegg.jp/list/pathway/')
pathways.columns=['pathway_ID','pathway_name']
pathways.to_csv("data/kegg/pathways.tsv", index=False, sep='\t')
