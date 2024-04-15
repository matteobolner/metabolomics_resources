rule download_smpdb_data:
    output:
        'data/smpdb/smpdb_pathways.csv'
    params:
        pathways='data/smpdb/',
        metabolites='data/smpdb/metabolites/'
    script:
        "../scripts/smpdb/get_smpdb.py"
