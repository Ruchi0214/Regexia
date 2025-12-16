import os
import re
import json
import sqlite3
import pandas as pd
from flask import Flask, request, render_template, jsonify
from collections import Counter

app = Flask(__name__)

# --- CONFIGURATION ---
RULES_DICT = {
    'Emotional Trigger': {'regex': r'\b(crisis|danger|threat|fear|panic|emergency|urgent|deadly|catastrophe)\b', 'type': 'regex'},
    'Exaggeration': {'regex': r'\b(100%|always|never|total|completely|absolutely|guaranteed|forever|perfect)\b', 'type': 'regex'},
    'Self Promotion': {'regex': r'\b(I alone|only I|trust me|believe me|my achievement|I did this|I made)\b', 'type': 'regex'},
    'Fake Claim': {'regex': r'\d+ out of \d+ (experts|people|doctors|scientists)', 'type': 'regex'},
    'Attack Words': {'regex': r'\b(fake|corrupt|enemy|destroy|liar|crooked|radical|traitor)\b', 'type': 'regex'},
    'Repetition': {'type': 'logic'}
}

# --- OPTIMIZED ANALYSIS ENGINE ---
def analyze_text(text, active_rules, generate_html=False):
    if not isinstance(text, str): 
        text = str(text) if text is not None else ""
    
    matches = {}
    total_score = 0
    
    # Only prepare HTML if specifically requested (Speed Boost)
    highlighted = text.replace("<", "&lt;").replace(">", "&gt;") if generate_html else ""
    safe_preview = text[:100] + "..." 

    for rule_name in active_rules:
        rule = RULES_DICT.get(rule_name)
        if not rule: continue

        count = 0
        if rule['type'] == 'regex':
            pattern = re.compile(rule['regex'], re.IGNORECASE)
            found = pattern.findall(text)
            count = len(found)
            if count > 0 and generate_html:
                highlighted = pattern.sub(r'<span class="highlight">\g<0></span>', highlighted)
        
        elif rule['type'] == 'logic':
            words = re.findall(r'\w+', text.lower())
            repeats = [w for w, c in Counter(words).items() if c > 3]
            count = len(repeats)
            if count > 0 and generate_html:
                for w in repeats:
                    highlighted = re.sub(rf'\b{w}\b', f'<span class="highlight">{w}</span>', highlighted, flags=re.IGNORECASE)

        if count > 0:
            matches[rule_name] = count
            total_score += count

    return min(10, total_score), matches, highlighted, safe_preview

@app.route('/')
def index():
    return render_template('index.html', rules=RULES_DICT.keys())

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files: return jsonify({'error': 'No file'})
    
    file = request.files['file']
    col_name = request.form.get('column')
    
    try:
        active_rules = json.loads(request.form.get('rules'))
        df = pd.read_csv(file)
        
        # ⚡ SPEED LIMIT: Only process first 1000 rows for instant demo
        df = df.head(1000).fillna("")
        
        if col_name not in df.columns: 
            return jsonify({'error': f'Column "{col_name}" not found'})

        all_results = []
        rule_counts = Counter()

        # PASS 1: Calculate Scores Only (Fast)
        for idx, row in df.iterrows():
            text = row[col_name]
            # generate_html=False is much faster
            score, matches, _, safe_preview = analyze_text(text, active_rules, generate_html=False)
            
            rule_counts.update(matches)
            
            all_results.append({
                'id': int(idx),
                'score': int(score),
                'text_raw': str(text),
                'text_preview': safe_preview,
                'matches': matches
            })

        # Sort by score descending
        all_results.sort(key=lambda x: x['score'], reverse=True)

        # PASS 2: Generate Highlighting HTML ONLY for Top 50 (Efficient)
        top_hits_html = []
        for item in all_results[:50]:
            _, _, highlighted, _ = analyze_text(item['text_raw'], active_rules, generate_html=True)
            top_hits_html.append({
                'id': item['id'],
                'score': item['score'],
                'full_text': highlighted
            })

        # Prepare Lightweight Table Data
        table_data = [{
            'id': i['id'], 
            'score': i['score'], 
            'text': i['text_preview'], 
            'matches': i['matches']
        } for i in all_results[:200]]

        return jsonify({
            'total_rows': len(df),
            'table_data': table_data,
            'explain_data': top_hits_html, # Only top 50 have HTML
            'rule_counts': dict(rule_counts),
            'active_rules': active_rules
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)})

@app.route('/save_db', methods=['POST'])
def save_db():
    try:
        data = request.json.get('data')
        conn = sqlite3.connect('regexia_results.db')
        df = pd.DataFrame(data)
        if 'matches' in df.columns: df = df.drop(columns=['matches'])
        df.to_sql('analysis_results', conn, if_exists='replace', index=False)
        conn.close()
        return jsonify({'status': 'success', 'message': 'Saved to SQLite DB successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)