**🔍 Regexia — Visual Pattern Intelligence Engine**
Regexia is a click-driven, command-line–inspired text intelligence engine that scans political speeches, tweets, articles, and long-form documents to identify linguistic patterns, bias indicators, and repeated rhetorical structures.

It combines:
⚙️ Regex-based precision
🧠 Explainable rule-based pattern analysis
⚡ Parallel processing
🖥 Interactive Streamlit UI
🗂 Pattern library (JSON)
💬 Command-line simulation
📊 Full visual analytics
🗄 SQLite storage
📥 CSV export
Regexia was designed to help users navigate today’s world of AI-generated misinformation, manipulated political messages, and biased rhetoric, while ensuring complete transparency.

**🎯 What Problem Does Regexia Solve?**
We live in a world filled with fake news, propaganda, AI-generated political content, and rapid misinformation. Traditional fact-checking tools are:
❌ Slow
❌ Manual
❌ Not explainable
❌ Hard to scale

Regexia provides an alternative:
**A transparent, rule-based, explainable text-analysis engine** that can detect bias, patterns, and rhetoric instantly.

**🧠 Core Idea**
Regexia breaks down large texts into analysable units, scans each line or chunk using patterns such as:
Emotional manipulation
Exaggeration
Self-promotion
Attacks / negative rhetoric
Statistical or numerical claims
Repetitive structures
Custom patterns shaped by the user

Then it generates:
A pattern score
Visual insights
Highlighted explainability view
CSV reports
SQLite database records

**🚀 How Regexia Works**
1. Upload a CSV File
You begin by uploading a CSV file.
Regexia:
Loads it instantly
Shows you the first rows
Detects all object/text-like columns
Lets you choose one column as the “text source”
This makes it work with any **dataset structure.**

2. Choose Patterns to Analyse
You get three ways to select patterns:
**A) Pattern Packs (JSON Pattern Library)**
Inside /patterns, you can store files like:
{
  "name": "emotional_rhetoric",
  "patterns": ["crisis", "fear", "danger", "threat", "panic"]
}
Regexia loads these automatically.

**B) Predefined Patterns**
Simply tick checkboxes:
Emotional triggers
Numbers
Exaggeration
Self-promotion
Attack keywords

**C) Visual Regex Builder**
You can build your own rule:
Enter a word / phrase
Choose exact match
Include digit requirement
Add fully custom regex
Regexia combines all selected patterns into final_rules.

**3. Command Simulation (CLI-style Preview)**-
Even though Regexia is GUI-based, it shows the equivalent terminal command:
regexia scan --file uploaded.csv --column article_text --emotional --attack --numbers
This mimics a developer-friendly CLI experience.

**4. Run Pattern Analysis**
When you click Run Pattern Analysis, Regexia:
Scans every line of text
Applies all regex rules
Counts matches for each rule
Calculates a Total Score
Produces a structured results table
If Parallel Processing is enabled, Regexia uses multiple cores.

**5. Visual Outputs**
✔** Score Distribution Histogram**
Shows how many texts contain heavy manipulation vs light or none.

**✔ Rule Hit Count Chart**
Displays which patterns appear the most.

**✔ Highest-Scoring Texts**
Lets you quickly view the most suspicious entries.

**✔ Explainability View**
All triggering words are highlighted:

Our nation is in <mark>crisis</mark> and <mark>only I</mark> can fix it.

This is a key USP.

**6. Export Options**
**CSV Export**
Download all analysis results instantly.

**SQLite Database Export**
Regexia creates:

regexia_results.db

containing a complete analysis table.

This allows further research, queries, or integration into dashboards.

📁 Project Structure
Regexia/
│
├── regexia_app.py
├── requirements.txt
├── README.md
│
└── patterns/
      ├── emotional.json
      ├── exaggeration.json
      └── custom_pack.json


You can add unlimited JSON pattern packs.

**🧪 Sample Input / Output**
**📥 Sample Input (CSV)**
"Our nation is in crisis and only I can fix it."
"The economy is 100% stable and will always improve."
"These corrupt people are lying to you."

**📤 Sample Output Table**
text	Emotional	Exaggeration	Self Promotion	Attack	Numbers	Total Score
Our nation is in crisis and only I can fix it.	1	0	1	0	0	2
The economy is 100% stable and will always improve.	0	2	0	0	1	3
These corrupt people are lying to you.	0	0	0	1	0	1
🔍 Explainability View
Our nation is in <mark>crisis</mark> and <mark>only I</mark> can fix it.
The economy is <mark>100%</mark> stable and will <mark>always</mark> improve.
These <mark>corrupt</mark> people are <mark>lying</mark> to you.
<img width="1367" height="330" alt="image" src="https://github.com/user-attachments/assets/4cfb6d6a-8dda-4f32-a75d-40bd7da4720a" />


📦 Technologies Used
Streamlit
Python
Pandas
Matplotlib
Regex
SQLite
Multiprocessing
JSON pattern packs

🛠 Installation (Local Machine)
git clone https://github.com/Ruchi0214/Regexia.git
cd Regexia
pip install -r requirements.txt
streamlit run regexia_app.py

🛠 Deploying on AWS EC2
Launch EC2 (Ubuntu)
Install Git
Clone your repo
Create virtual environment
Install dependencies
Run Streamlit on port 8501
Open security group: port 8501
Use nohup for background running
deployment command:
nohup streamlit run regexia_app.py --server.port 8501 --server.address 0.0.0.0 &

**📥 requirements.txt**
streamlit==1.33.0
pandas==2.1.4
matplotlib==3.7.2
numpy==1.26.4

**🎓 What I Learned**
By building Regexia, I gained hands-on experience with:
Advanced Regex
Pattern recognition
Text chunking and NLP logic
Explainable text intelligence
Web UI development using Streamlit
Parallel processing
Database integration
Deploying on AWS EC2



Live Link: http://3.151.245.227:8501 
