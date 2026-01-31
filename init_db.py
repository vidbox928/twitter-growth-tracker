#!/usr/bin/env python3
"""
Initialize SQLite database for Twitter growth tracking
"""

import sqlite3
import os

DB_PATH = 'twitter_growth.db'

def init_database():
    """Create database schema"""
    
    # Remove old database if exists
    if os.path.exists(DB_PATH):
        print(f"⚠️  Database {DB_PATH} already exists. Skipping creation.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Growth metrics table
    cursor.execute('''
    CREATE TABLE growth (
        date TEXT PRIMARY KEY,
        followers INTEGER NOT NULL,
        following INTEGER NOT NULL,
        tweets_count INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tweets table
    cursor.execute('''
    CREATE TABLE tweets (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        text TEXT NOT NULL,
        likes INTEGER DEFAULT 0,
        retweets INTEGER DEFAULT 0,
        replies INTEGER DEFAULT 0,
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX idx_growth_date ON growth(date DESC)')
    cursor.execute('CREATE INDEX idx_tweets_created ON tweets(created_at DESC)')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized: {DB_PATH}")
    print("📊 Tables created: growth, tweets")

if __name__ == '__main__':
    init_database()
