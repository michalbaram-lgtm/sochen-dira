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
        conn = sqlite3.connect('agent.db')
        c = conn.cursor()
        
        # Save user
        c.execute('INSERT INTO users (email, name, phone) VALUES (?, ?, ?)',
                 (data['email'], data.get('name'), data.get('phone')))
        user_id = c.lastrowid
        
        # Save preferences
        c.execute('''INSERT INTO preferences 
                    (user_id, search_type, cities, neighborhoods, min_price, max_price, 
                     rooms, property_types, must_haves, deal_breakers, additional_notes, co_searchers)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (user_id, 
                  data['searchType'],
                  json.dumps(data.get('cities', [])),
                  json.dumps(data.get('neighborhoods', [])),
                  data.get('minPrice'),
                  data.get('maxPrice'),
                  json.dumps(data.get('rooms', [])),
                  json.dumps(data.get('propertyTypes', [])),
                  json.dumps(data.get('mustHaves', [])),
                  json.dumps(data.get('dealBreakers', [])),
                  data.get('additionalNotes'),
                  data.get('coSearchers')))
        
        conn.commit()
        conn.close()
        
        session['user_id'] = user_id
        return jsonify({'success': True, 'redirect': '/loading'})
    
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Email already registered'}), 400
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
