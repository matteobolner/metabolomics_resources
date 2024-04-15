rule download_kegg_compounds:
    output:
        compounds="data/kegg/compounds.tsv"
    script:
        "../scripts/kegg/get_all_compounds.py"

rule download_kegg_pathways:
    output:
        pathways="data/kegg/pathways.tsv"
    script:
        "../scripts/kegg/get_all_pathways.py"

rule link_pathways_and_compounds:
    input:
        pathways="data/kegg/pathways.tsv",
        compounds="data/kegg/compounds.tsv"
    output:
        linked="data/kegg/linked_pathways_and_compounds.tsv"
    script:
        "../scripts/kegg/link_pathways_and_compounds.py"

rule merge_pathways_and_compounds:
    input:
        pathways="data/kegg/pathways.tsv",
        compounds="data/kegg/compounds.tsv",
        linked="data/kegg/linked_pathways_and_compounds.tsv"
    output:
        merged="data/kegg/merged_pathways_and_compounds.tsv"
    script:
        "../scripts/kegg/merge_pathways_and_compounds.py"
