from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'  # Change this!

# Database setup
def init_db():
    conn = sqlite3.connect('agent.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Preferences table
    c.execute('''CREATE TABLE IF NOT EXISTS preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        search_type TEXT,  -- 'buy' or 'rent'
        cities TEXT,  -- JSON array
        neighborhoods TEXT,  -- JSON array
        min_price INTEGER,
        max_price INTEGER,
        rooms TEXT,  -- JSON array like ["2", "3", "4+"]
        property_types TEXT,  -- JSON array
        must_haves TEXT,  -- JSON array
        deal_breakers TEXT,  -- JSON array
        additional_notes TEXT,
        co_searchers TEXT,  -- Comma-separated emails
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@app.route('/api/save-onboarding', methods=['POST'])
def save_onboarding():
    data = request.json
    
    try:
        # For MVP: Just save to session, skip database
        session['user_data'] = data
        session['user_id'] = 1  # Temporary user ID
        
        return jsonify({'success': True, 'redirect': '/loading'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/loading')
def loading():
    if 'user_id' not in session:
        return redirect(url_for('onboarding'))
    return render_template('loading.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('onboarding'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
