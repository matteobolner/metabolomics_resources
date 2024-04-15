rule annotate_gwas_with_kegg_compounds:
    input:
        gwas="input/{breed}_5e05_genes_gwascatalog_MetabolonInfo.xlsx",
        compounds="data/kegg/compounds.tsv"
    output:
        annotated_gwas="data/gwas/{breed}/gwas_with_kegg_compounds.tsv",
    script:
        "../scripts/gwas/annotate_with_kegg_compounds.py"
