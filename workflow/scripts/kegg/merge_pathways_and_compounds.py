import pandas as pd
import seaborn as sns

#pathways=pd.read_table("data/kegg/pathways.tsv")
#compounds=pd.read_table("data/kegg/compounds.tsv")
#pathways_and_compounds=pd.read_table("data/kegg/pathways_and_compounds.tsv")

pathways=pd.read_table(snakemake.input.pathways)

compounds=pd.read_table(snakemake.input.compounds)

pathways_and_compounds=pd.read_table(snakemake.input.linked)

pathway_compound_counts=pathways_and_compounds['pathway_ID'].value_counts()
too_large=pathway_compound_counts[pathway_compound_counts>1000]
pathways_and_compounds=pathways_and_compounds[~pathways_and_compounds['pathway_ID'].isin(too_large.index)]
pathways_and_compounds=pathways_and_compounds.merge(pathways)
pathway_compound_counts=pathways_and_compounds['pathway_ID'].value_counts()

pathways_and_compounds=pathways_and_compounds.merge(compounds)

#pathways_and_compounds.to_csv("data/kegg/merged_pathways_and_compounds.tsv", index=False, sep='\t')
pathways_and_compounds.to_csv(snakemake.output.merged, index=False, sep='\t')
