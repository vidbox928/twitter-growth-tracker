#!/usr/bin/env python3
"""
Collect Twitter data using bird CLI and store in SQLite
"""

import sqlite3
import json
import subprocess
import os
from datetime import datetime, date

DB_PATH = 'twitter_growth.db'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
CT0 = os.getenv('CT0')

def run_bird_command(cmd):
    """Run bird CLI command with auth"""
    env = os.environ.copy()
    if AUTH_TOKEN:
        env['AUTH_TOKEN'] = AUTH_TOKEN
    if CT0:
        env['CT0'] = CT0
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return None, str(e), 1

def get_account_info():
    """Get current account stats"""
    stdout, stderr, code = run_bird_command('bird whoami')
    
    if code != 0:
        print(f"❌ Failed to get account info: {stderr}")
        return None
    
    # Parse output
    lines = stdout.strip().split('\n')
    info = {}
    
    for line in lines:
        if '🙋' in line:
            # Extract username (simplified parsing)
            info['username'] = '@opkceo'
        elif '🪪' in line:
            parts = line.split()
            if len(parts) > 1:
                info['user_id'] = parts[-1]
    
    # For now, use mock data (bird CLI doesn't return follower count in whoami)
    # In production, would need to call Twitter API or parse profile
    info['followers'] = 42  # TODO: Get real count
    info['following'] = 15
    info['tweets_count'] = 8
    
    return info

def get_recent_tweets(limit=10):
    """Get recent tweets from timeline"""
    stdout, stderr, code = run_bird_command(f'bird home -n {limit}')
    
    if code != 0:
        print(f"❌ Failed to get tweets: {stderr}")
        return []
    
    # Parse tweets (simplified - bird CLI output parsing)
    # In production, would parse the actual output format
    tweets = []
    
    # Mock data for now
    tweets.append({
        'id': '1234567890',
        'created_at': datetime.now().isoformat(),
        'text': 'Building OpenPasskey - the card scheme for crypto. Payments are the main bus. 🏗️',
        'likes': 12,
        'retweets': 3,
        'replies': 2
    })
    
    return tweets

def save_growth_data(conn, info):
    """Save daily growth metrics"""
    today = date.today().isoformat()
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO growth (date, followers, following, tweets_count)
        VALUES (?, ?, ?, ?)
    ''', (today, info['followers'], info['following'], info['tweets_count']))
    
    conn.commit()
    print(f"✅ Saved growth data: {info['followers']} followers")

def save_tweets(conn, tweets):
    """Save tweet performance data"""
    cursor = conn.cursor()
    
    for tweet in tweets:
        cursor.execute('''
            INSERT OR REPLACE INTO tweets (id, created_at, text, likes, retweets, replies)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            tweet['id'],
            tweet['created_at'],
            tweet['text'],
            tweet['likes'],
            tweet['retweets'],
            tweet['replies']
        ))
    
    conn.commit()
    print(f"✅ Saved {len(tweets)} tweets")

def generate_json_export(conn):
    """Generate data.json for frontend"""
    cursor = conn.cursor()
    
    # Get current stats
    cursor.execute('SELECT * FROM growth ORDER BY date DESC LIMIT 1')
    current_row = cursor.fetchone()
    
    if not current_row:
        print("⚠️  No data in database yet")
        return
    
    current = {
        'date': current_row[0],
        'followers': current_row[1],
        'following': current_row[2],
        'tweets_count': current_row[3]
    }
    
    # Get 30-day history
    cursor.execute('SELECT * FROM growth ORDER BY date DESC LIMIT 30')
    history = []
    for row in cursor.fetchall():
        history.append({
            'date': row[0],
            'followers': row[1],
            'following': row[2],
            'tweets_count': row[3]
        })
    
    history.reverse()  # Oldest first for chart
    
    # Get recent tweets
    cursor.execute('SELECT * FROM tweets ORDER BY created_at DESC LIMIT 10')
    recent_tweets = []
    for row in cursor.fetchall():
        recent_tweets.append({
            'id': row[0],
            'created_at': row[1],
            'text': row[2],
            'likes': row[3],
            'retweets': row[4],
            'replies': row[5]
        })
    
    # Export JSON
    data = {
        'current': current,
        'history': history,
        'recent_tweets': recent_tweets,
        'updated_at': datetime.now().isoformat()
    }
    
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Generated data.json ({len(history)} days of history)")

def main():
    """Main collection routine"""
    print("🐦 Collecting Twitter data...")
    
    # Check database exists
    if not os.path.exists(DB_PATH):
        print("❌ Database not found. Run init_db.py first!")
        return
    
    # Load auth from config
    global AUTH_TOKEN, CT0
    config_path = os.path.expanduser('~/.config/bird/.env')
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                if line.startswith('AUTH_TOKEN='):
                    AUTH_TOKEN = line.split('=', 1)[1].strip()
                elif line.startswith('CT0='):
                    CT0 = line.split('=', 1)[1].strip()
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Get account info
    info = get_account_info()
    if info:
        save_growth_data(conn, info)
    
    # Get recent tweets
    tweets = get_recent_tweets()
    if tweets:
        save_tweets(conn, tweets)
    
    # Generate JSON export
    generate_json_export(conn)
    
    conn.close()
    print("✅ Collection complete!")

if __name__ == '__main__':
    main()
