from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tax_data.download_latest import download_and_extract
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

TAX_DATA_PATH = "tax_data/tx_rates.csv"

def load_tax_data():
    return pd.read_csv(TAX_DATA_PATH)

@app.post("/calculate-tax")
async def calculate_tax(address: str = Form(...), amount: float = Form(...)):
    df = load_tax_data()
    zip_code = address.split()[-1]
    row = df[df["Zip"] == int(zip_code)].iloc[0]
    total_rate = row["Total Rate"]
    tax_amount = amount * total_rate
    return {
        "tax_rate": total_rate,
        "tax_amount": round(tax_amount, 2),
        "total_amount": round(amount + tax_amount, 2)
    }

@app.post("/filing-data")
async def filing_data(zip_code: str = Form(...)):
    df = load_tax_data()
    row = df[df["Zip"] == int(zip_code)].iloc[0]
    return {
        "zip": row["Zip"],
        "county": row["County"],
        "city": row["City"],
        "jurisdiction_code": f"{row['County']} - {row['City']}"
    }

@app.get("/admin", response_class=HTMLResponse)
async def admin_ui(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/admin/download-tax-data")
async def update_tax_data():
    download_and_extract()
    return {"status": "success"}
