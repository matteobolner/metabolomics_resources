import requests
import pandas as pd
from io import StringIO

#compounds=pd.read_table("data/kegg/compounds.tsv")
#pathways=pd.read_table("data/kegg/pathways.tsv")
compounds=pd.read_table(snakemake.input.compounds)
pathways=pd.read_table(snakemake.input.pathways)

def fill_id(input_id):
    input_id=str(input_id)
    while len(input_id)<5:
        input_id="0"+input_id
    return(input_id)


pathways['pathway_ID']=pathways['pathway_ID'].apply(fill_id)
pathways['pathway_ID']="map"+pathways['pathway_ID']

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
    try:
        tempdf=get_df_kegg(f"https://rest.kegg.jp/link/cpd/{row['pathway_ID']}")
        tempdf.columns=['pathway_ID','compound_ID']
        tempdf['pathway_ID']=tempdf['pathway_ID'].str.replace("path:","")
        tempdf['compound_ID']=tempdf['compound_ID'].str.replace("cpd:","")
        pathways_compounds.append(tempdf)
    except ValueError:
        print(index)
        continue

pathways_compounds=pd.concat(pathways_compounds)
#pathways_compounds=pathways_compounds.to_csv("data/kegg/pathways_and_compounds.tsv", index=False, sep='\t')
pathways_compounds=pathways_compounds.to_csv(snakemake.output.linked, index=False, sep='\t')
