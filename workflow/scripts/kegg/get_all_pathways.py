import requests
import pandas as pd
from io import StringIO

def get_df_kegg(url,species, sep='\t'):
    data=requests.get(url)
    if len(data.text)==1:
        raise ValueError("No data found")
    if sep=='whitespace':
        pathways=pd.read_table(StringIO(data.text), header=None, delim_whitespace=True)
    else:
        pathways=pd.read_table(StringIO(data.text), header=None, sep=sep)
    pathways[0]=pathways[0].str.replace(species, "")
    return(pathways)

pathways_ssc=get_df_kegg('http://rest.kegg.jp/list/pathway/ssc', 'ssc')

pathways_ssc.columns=['pathway_ID','pathway_name']
pathways_ssc.to_csv(snakemake.output.pathways, index=False, sep='\t')
