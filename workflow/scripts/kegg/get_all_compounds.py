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

compounds=get_df_kegg('http://rest.kegg.jp/list/compound')
compounds.columns=['compound_ID','text']
compounds['compound_name'] = compounds['text'].str.split(';')
compounds = compounds.explode('compound_name')
compounds=compounds.drop(columns='text')
compounds['compound_name']=compounds['compound_name'].str.lstrip()
compounds['compound_name']=compounds['compound_name'].str.rstrip()
compounds=compounds.drop_duplicates()
compounds=compounds.reset_index(drop=True)
compounds.to_csv(snakemake.output.compounds, index=False, sep='\t')
