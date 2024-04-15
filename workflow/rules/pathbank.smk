rule download_pathbank_data:
    output:
        pathways='data/pathbank/pathbank_pathways.csv',
        metabolites='data/pathbank/pathbank_metabolites.csv'
    params:
        dir="data/pathbank/"
    script:
        "../scripts/pathbank/get_pathbank.py"
