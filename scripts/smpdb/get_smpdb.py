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

download_zipped_csv('https://smpdb.ca/downloads/smpdb_pathways.csv.zip', 'data/smpdb/')

download_zipped_csv('https://smpdb.ca/downloads/smpdb_metabolites.csv.zip', 'data/smpdb/metabolites/')
