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
#modules=get_df_kegg('http://rest.kegg.jp/list/module')
#networks=get_df_kegg('http://rest.kegg.jp/list/network')


compounds
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
