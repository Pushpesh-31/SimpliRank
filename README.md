# 🏆 SimpliRank - Leaderboard for Data Science Competitions

SimpliRank is a secure, deployable leaderboard app built with FastAPI and SQLite. It enables teams to register, submit predictions, get auto-scored, and track their rank live — while giving admins complete control over the competition.

---

## 🚀 Features

- 📝 Team registration (username + email + password)
- 🔐 Login-free submission with password auth
- 📊 Automatic score calculation (default: RMSE)
- 🧮 SQLite backend — no DB setup needed
- ✉️ Optional email notifications on team registration
- 👩‍💼 Admin panel to:
  - Approve/reject teams
  - Upload ground truth files
  - Set daily submission limits
  - View full submission history
- 🖼️ Custom branding with SimpliRank logo
- 🧾 Ready for Railway deployment

---

## 🧰 Tech Stack

- [x] FastAPI
- [x] Jinja2 templating
- [x] SQLite
- [x] Uvicorn
- [x] Pandas
- [x] SMTP (optional email support)

---

## 🧪 Setup

### Step 1: Install requirements
```bash
pip install -r requirements.txt
```

### Step 2: Run locally
```bash
uvicorn app.main:app --reload
```

---

## 🌐 Environment Variables (via Railway or .env)

| Variable         | Description                        |
|------------------|------------------------------------|
| `ADMIN_PASSWORD` | Password used for admin actions    |
| `SMTP_USER`      | Email for sending notifications    |
| `SMTP_PASSWORD`  | SMTP password or app password      |
| `SMTP_SERVER`    | Default: smtp.gmail.com            |
| `SMTP_PORT`      | Default: 587                       |
| `ADMIN_EMAIL`    | Email to notify for registrations  |

If email is not needed, skip `SMTP_` and `ADMIN_EMAIL` setup.

---

## 📂 Project Structure

```
.
├── app/
│   ├── main.py
│   ├── utils.py
│   ├── email_utils.py
│   ├── data/
│   │   └── ground_truth.csv
│   ├── templates/
│   │   ├── index.html
│   │   ├── leaderboard.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── forgot.html
│   │   └── admin.html
│   └── static/
│       └── logo.png
├── requirements.txt
├── railway.toml
├── README.md
└── db.sqlite3 (auto-created on first run)
```

---

## 🧠 Ground Truth File Format

Upload via `/admin` panel:

```csv
id,target
1,100
2,150
3,200
```

Submissions should match with:

```csv
id,prediction
1,102.4
2,148.9
3,198.7
```

---

## 🧭 Admin Panel

- Navigate to `/admin`
- Use actions with the correct admin password (default: `admin123`)
- Actions:
  - Approve or reject teams
  - Upload new ground truth file
  - Set submission limit
  - View submission history in real-time

---

## 🌍 Deploy on Railway

1. Create a new Railway project
2. Upload or connect to GitHub
3. Set environment variables
4. Use this start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📄 License

MIT — use and improve freely. Built to simplify competitions, not complicate them.

---

Made with ❤️ by Pushpesh & ChatGPT

---

## 🙌 Acknowledgments

This project was initiated and directed by **Pushpesh Sharma**, inspired by years of organizing hackathons and Datathons through SPE.

If you fork this project or reuse parts of SimpliRank, a mention or attribution would be appreciated!

GitHub: [github.com/pushpeshsharma](https://github.com/pushpeshsharma)
