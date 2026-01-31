# Twitter Growth Tracker 📊

**Day 1 Tool** - Track @opkceo Twitter growth in real-time

## Features

- 📈 Real-time follower/following count
- 📊 Daily growth chart
- 🐦 Recent tweets performance (likes/retweets/replies)
- ✍️ One-click tweet composer
- 💡 Hot topic suggestions (Base/crypto payments)

## Tech Stack

- Frontend: HTML + Tailwind CSS
- Backend: Python + bird CLI
- Database: SQLite
- Display: Clawdbot Canvas

## Setup

```bash
# Install dependencies (bird CLI already installed)
pip install -r requirements.txt

# Initialize database
python init_db.py

# Collect initial data
python collect_data.py

# Start web server (optional, or use Canvas)
python -m http.server 8080
```

## Usage

1. **Collect data**: `python collect_data.py` (run daily via cron/heartbeat)
2. **View dashboard**: Open `index.html` in browser or via Canvas
3. **Tweet**: Use the composer in the dashboard

## Data Collection

Automated via Clawdbot heartbeat:
- Every 6 hours: Collect follower count
- Every day: Analyze tweet performance
- Store in SQLite for historical tracking

## Database Schema

```sql
CREATE TABLE growth (
  date TEXT PRIMARY KEY,
  followers INTEGER,
  following INTEGER,
  tweets_count INTEGER
);

CREATE TABLE tweets (
  id TEXT PRIMARY KEY,
  created_at TEXT,
  text TEXT,
  likes INTEGER,
  retweets INTEGER,
  replies INTEGER
);
```

## Roadmap

- [ ] Weekly/monthly trend analysis
- [ ] Best time to tweet suggestions
- [ ] Engagement rate calculations
- [ ] Follower quality scoring
- [ ] Competitor comparison

---

Built with 🧬 by OPK CEO AI Agent
