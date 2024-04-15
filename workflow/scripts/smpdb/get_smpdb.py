import pandas as pd
import requests
import zipfile
import io
import os
from pathlib import Path

Path(snakemake.params.pathways).mkdir(parents=True, exist_ok=True)
Path(snakemake.params.metabolites).mkdir(parents=True, exist_ok=True)

def download_zipped_csv(url, outdir):
    #url="https://smpdb.ca/downloads/smpdb_pathways.csv.zip"
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Extract all contents to a specific directory
        z.extractall(outdir)

download_zipped_csv('https://smpdb.ca/downloads/smpdb_pathways.csv.zip', snakemake.params.pathways)
download_zipped_csv('https://smpdb.ca/downloads/smpdb_metabolites.csv.zip', snakemake.params.metabolites)
