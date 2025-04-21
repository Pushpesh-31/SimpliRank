import pandas as pd
import sqlite3
from datetime import datetime

def calculate_score(pred_df):
    gt_df = pd.read_csv("app/data/ground_truth.csv")
    merged = pd.merge(gt_df, pred_df, on="id")
    return ((merged['target'] - merged['prediction'])**2).mean()

def update_leaderboard(team, score, filename):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    today = datetime.now().date()
    cursor.execute("SELECT value FROM config WHERE key = 'max_submissions_per_day'")
    max_subs = int(cursor.fetchone()[0])
    count = cursor.execute("SELECT COUNT(*) FROM submissions WHERE team=? AND date(submitted_at)=?", (team, today)).fetchone()[0]
    if count >= max_subs:
        return False
    cursor.execute("INSERT INTO submissions (team, score, filename) VALUES (?, ?, ?)", (team, score, filename))
    cursor.execute("INSERT INTO leaderboard (team, score) VALUES (?, ?)", (team, score))
    conn.commit()
    conn.close()
    return True

def get_leaderboard():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    result = cursor.execute("SELECT team, MIN(score) as score FROM leaderboard GROUP BY team ORDER BY score ASC").fetchall()
    return [{"team": row[0], "score": row[1]} for row in result]

def get_submission_history():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return [dict(r) for r in conn.execute("SELECT * FROM submissions ORDER BY submitted_at DESC")]

def set_daily_limit(limit):
    conn = sqlite3.connect("db.sqlite3")
    conn.execute("UPDATE config SET value = ? WHERE key = 'max_submissions_per_day'", (str(limit),))
    conn.commit()
    conn.close()
