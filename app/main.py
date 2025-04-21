from fastapi import FastAPI, Form, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import pandas as pd
import sqlite3
import os
from app.utils import calculate_score, update_leaderboard, get_leaderboard, get_submission_history, set_daily_limit
from app.email_utils import send_email

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(username):
    conn = sqlite3.connect("db.sqlite3")
    row = conn.execute("SELECT username, hashed_password, approved FROM teams WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row:
        return {"username": row[0], "hashed_password": row[1], "approved": row[2]}
    return None

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit/")
def submit_file(team: str = Form(...), password: str = Form(...), file: UploadFile = File(...)):
    user = get_user(team)
    if not user or not pwd_context.verify(password, user["hashed_password"]) or not user["approved"]:
        raise HTTPException(status_code=403, detail="Invalid login or approval pending.")
    df = pd.read_csv(file.file)
    score = calculate_score(df)
    success = update_leaderboard(team, score, file.filename)
    if not success:
        raise HTTPException(status_code=403, detail="Submission limit reached.")
    return {"team": team, "score": score}

@app.get("/leaderboard", response_class=HTMLResponse)
def leaderboard(request: Request):
    return templates.TemplateResponse("leaderboard.html", {"request": request, "leaderboard": get_leaderboard()})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    hashed = pwd_context.hash(password)
    conn = sqlite3.connect("db.sqlite3")
    conn.execute("INSERT OR IGNORE INTO teams (username, hashed_password, approved, email) VALUES (?, ?, 0, ?)", (username, hashed, email))
    conn.commit()
    conn.close()
    admin_email = os.getenv("ADMIN_EMAIL")
    if admin_email:
        send_email("New SimpliRank Team", f"Team {username} registered. Please approve.", admin_email)
    return {"message": "Registered. Awaiting approval."}

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    conn = sqlite3.connect("db.sqlite3")
    teams = conn.execute("SELECT username, approved FROM teams").fetchall()
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "submissions": get_submission_history(), "teams": teams})

@app.post("/admin/approve")
def approve_team(username: str = Form(...), password: str = Form(...)):
    if password != os.getenv("ADMIN_PASSWORD", "admin123"):
        raise HTTPException(status_code=403, detail="Wrong admin password.")
    conn = sqlite3.connect("db.sqlite3")
    conn.execute("UPDATE teams SET approved = 1 WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return {"message": f"{username} approved."}

@app.post("/admin/reject")
def reject_team(username: str = Form(...), password: str = Form(...)):
    if password != os.getenv("ADMIN_PASSWORD", "admin123"):
        raise HTTPException(status_code=403, detail="Wrong admin password.")
    conn = sqlite3.connect("db.sqlite3")
    conn.execute("DELETE FROM teams WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return {"message": f"{username} rejected."}

@app.post("/admin/upload")
async def upload_ground_truth(file: UploadFile = File(...), password: str = Form(...)):
    if password != os.getenv("ADMIN_PASSWORD", "admin123"):
        raise HTTPException(status_code=403, detail="Invalid admin password.")
    contents = await file.read()
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")
    try:
        with open("app/data/ground_truth.csv", "wb") as f:
            f.write(contents)
        return {"message": "Ground truth file uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file: {str(e)}")

@app.post("/admin/set-limit")
def admin_set_limit(password: str = Form(...), limit: int = Form(...)):
    if password != os.getenv("ADMIN_PASSWORD", "admin123"):
        return {"error": "Invalid password"}
    set_daily_limit(limit)
    return {"message": "Limit updated"}
