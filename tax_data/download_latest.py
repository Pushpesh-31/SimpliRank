import requests, zipfile, io, pandas as pd

def download_and_extract():
    url = "https://comptroller.texas.gov/taxes/sales/data/2024/january.zip"
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    csv_name = [name for name in z.namelist() if name.endswith(".csv")][0]
    df = pd.read_csv(z.open(csv_name))
    df.to_csv("tax_data/tx_rates.csv", index=False)
