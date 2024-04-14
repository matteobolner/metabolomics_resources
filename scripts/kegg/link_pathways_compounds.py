import requests
import pandas as pd
from io import StringIO

compounds=pd.read_table("data/kegg/compounds.tsv")
pathways=pd.read_table("data/kegg/pathways.tsv")

def get_df_kegg(url, sep='\t'):
    data=requests.get(url)
    if len(data.text)==1:
        raise ValueError("No data found")
    if sep=='whitespace':
        pathways=pd.read_table(StringIO(data.text), header=None, delim_whitespace=True)
    else:
        pathways=pd.read_table(StringIO(data.text), header=None, sep=sep)
    return(pathways)


pathways_compounds=[]
for index,row in pathways.iterrows():
    print(index)
    try:
        tempdf=get_df_kegg(f"https://rest.kegg.jp/link/cpd/{row['pathway_ID']}")
        tempdf.columns=['pathway_ID','compound_ID']
        tempdf['pathway_ID']=tempdf['pathway_ID'].str.replace("path:","")
        tempdf['compound_ID']=tempdf['compound_ID'].str.replace("cpd:","")
        pathways_compounds.append(tempdf)
    except ValueError:
        continue

pathways_compounds=pd.concat(pathways_compounds)
pathways_compounds=pathways_compounds.to_csv("data/kegg/pathways_and_compounds.tsv", index=False, sep='\t')
