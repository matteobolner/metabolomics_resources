import pandas as pd
import requests
import zipfile
import io

def download_zipped_csv(url, outdir):
    #url="https://smpdb.ca/downloads/smpdb_pathways.csv.zip"
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Extract all contents to a specific directory
        z.extractall(outdir)

download_zipped_csv('https://pathbank.org/downloads/pathbank_all_pathways.csv.zip', snakemake.params.dir')

download_zipped_csv('https://pathbank.org/downloads/pathbank_all_metabolites.csv.zip', snakemake.params.dir)
