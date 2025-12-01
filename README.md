🚀 Regexia — Visual Pattern Intelligence Engine

Regexia is a linguistic pattern analysis engine that detects bias, emotional manipulation, misinformation signals, and rhetorical patterns inside political and social text — powered by regex, parallel processing, and an interactive Streamlit UI.

💡 What Problem Does Regexia Solve?
In a world filled with:
AI-generated content
Fake news
Manipulated speeches
Context-free political claims

…people struggle to understand what’s real.

Regexia identifies hidden language patterns behind political speeches, tweets, and media statements using explainable, transparent logic.

🌟 Key Features
🔍 Pattern Library (Extensible)
Emotional triggers: crisis, fear, panic
Exaggeration: always, never, 100% guaranteed
Self-promotion: only I, trust me
Attack words: fake, corrupt, liar
Statistical claims: 9 out of 10 people…
Supports custom user-generated regex

⚡ Parallel Text Processing
Automatically chunks huge documents
Scans each chunk using multiprocessing
Real-time performance even for large datasets

🖥 Command-Line Simulation
Looks and feels like a terminal:
regexia scan --file speeches.csv --column text --attack

🎨 Interactive Web UI (Streamlit)
Upload CSV
Select text column
Choose regex patterns
Visual graphs + explainability
Export results to CSV
Save to SQLite database

🧠 Explainability Engine
Highlights exactly which words triggered the patterns — transparent & honest.

📁 Project Structure
Regexia/
│── regexia_app.py
│── patterns/
│   ├── emotional.json
│   ├── exaggeration.json
│── requirements.txt
│── README.md

▶ How to Run Locally
pip install -r requirements.txt
streamlit run regexia_app.py

🌐 Live Deployment (AWS EC2)

live URL:http://3.151.245.227:8501

🧪 Requirements
streamlit
pandas
numpy
matplotlib
plotly# Regexia
Regex-based Political Bias Analysis Engine
