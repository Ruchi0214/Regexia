# 🔍 Regexia — Real-Time Linguistic Pattern Intelligence Engine  
### *Transparent. Explainable. Offline-Capable. Open-Source.*

Regexia is a next-generation linguistic intelligence engine designed to detect **bias, manipulation, misinformation patterns**, and **AI-generated linguistic artefacts** inside political speeches, tweets, news articles, and long-form text.

It combines:

- ⚡ High-speed parallel regex scanning  
- 🧠 AI-aligned explainability  
- 👁️ Real-time linguistic pattern visualisation  
- 📦 Plug-and-play pattern libraries (JSON rule packs)  
- 🖥️ Full interactive dashboard built on Streamlit  
- 🗄️ SQLite database support  
- 🔍 CLI-style command simulation  
- 🧩 Text chunking + pattern scoring engine  

---

## 🎯 Problem Statement  
In a world drowned in **AI-generated content**, **misinformation**, and **manipulated political narratives**, it has become increasingly difficult to determine:

- What content is genuine?
- What text contains hidden emotional manipulation?
- Which speeches use repeated rhetorical strategies?
- Are political messages coherent or contradictory?
- Are statistics, claims, and attacks artificially inflated?

Traditional fact-checking tools are:

❌ Slow  
❌ Mostly manual  
❌ Not explainable  
❌ Not transparent  
❌ Not real-time  

Regexia solves this.

---

## 💡 Proposed Solution  

Regexia provides a **transparent, explainable, regex-driven linguistic scanning engine** that can detect:

- Emotional triggers  
- Exaggeration patterns  
- Self-promotion cues  
- Attacks and adversarial phrases  
- Repeated rhetoric  
- Statistical manipulation  
- Hidden linguistic structures used in propaganda  

### The system supports:

- **Parallel text processing** (multi-core scanning)  
- **Real-time explainability view** (highlighted text)  
- **Interactive dashboard** (graphs, pattern counts, score distribution)  
- **Exportable reports (CSV + SQLite database)**  
- **Pattern library plugins (researchers can add rule-packs)**  
- **Command-line inspired UI**, such as:  

regexia scan --file speeches.csv --column text --emotional --attack


---

## 🧪 Student Research Table (Required for Internship Submission)

| Student Name | Text Source Title | Text Type | Problem I Want to Solve | Why It Matters | My Method | What I Measure | Expected Output | File Path / URL | Where I Save Results |
|--------------|------------------|----------|--------------------------|----------------|------------|----------------|----------------|------------------|------------------------|
| Ruchika | Political Speech Dataset | Text Documents | Detect hidden linguistic patterns and bias in political text using regex + parallel processing | Understand how language influences perception; learn pattern recognition | Regex-driven scanning, pattern libraries, chunking, multiprocessing | Pattern frequency, emotional density, manipulation cues | Interactive dashboard, graphs, CSV report | `/projects/regexia/input/speech_dataset.txt` | `/projects/regexia/output/analysis_report.csv` |

---
## System Architecture Overview
Regexia follows a modular and scalable architecture:

1. **Input Layer**  
   The user uploads a CSV which is parsed using Pandas.

2. **Detection Layer**  
   Regexia automatically identifies text-like columns.

3. **Chunking Layer**  
   Long text is broken into manageable chunks for efficient pattern scanning.

4. **Pattern Engine**  
   - Predefined patterns  
   - JSON-based pattern packs  
   - Visual regex builder  
   All patterns are compiled into a unified rule set.

5. **Processing Layer**  
   Multiprocessing scans each chunk in parallel for maximum speed.

6. **Scoring Engine**  
   Each chunk receives a bias score based on detected patterns.

7. **Output Layer**  
   - Interactive graphs  
   - Explainability with highlighted text  
   - CSV output  
   - SQLite storage  
   - Full dashboard


## System Architecture Diagram
<img width="1533" height="923" alt="image" src="https://github.com/user-attachments/assets/aaa6d060-7e05-459a-9fa7-9a87c501af81" />

---

## 🚀 Features

### 1. **Pattern Library (JSON Rule Packs)**
Load multiple patterns such as:
- Political rhetoric  
- Emotional intensity words  
- Logical fallacies  
- Corporate influence patterns  
- Climate discourse framing  
…and more.

Researchers can contribute new libraries.

---

### 2. **Explainability View**
Regexia highlights the exact words that triggered detection using `<mark>` colouring.

Example:

> The **<mark>crisis</mark>** is worsening because **<mark>they</mark>** are **<mark>corrupt</mark>**.

---

### 3. **Command-Line Mode (Simulated UI)**
Users can preview commands like:
regexia scan --file speeches.csv --column text --exaggeration --selfpromote

---

### 4. **Parallel Processing Engine**
Regexia uses multiprocessing to scan **thousands of text chunks per second**, ensuring real-time performance.

---

### 5. **Interactive Visual Dashboard**
Includes:

- Score distribution histogram  
- Rule hit frequency graphs  
- Highest-scoring biased texts  
- Highlighted explanations  
- Downloadable CSV summaries  

---

### 6. **SQLite Database Support**
Save results to a local database for long-term research or integration.
regexia_results.db


---

# 🌍 Deployment & Access

Regexia is deployed to a live environment for evaluation and demonstration.  
This allows reviewers, mentors, and stakeholders to test the system without manual installation.

### 🔗 Live Application URL  
👉 **http://3.151.245.227:8501**

*(Runs on HTTP since the project does not use a custom domain. Fully functional.)*

---

## 💻 Deployment Architecture (AWS EC2)

Regexia is deployed using:

- Ubuntu 22.04 EC2 instance  
- Python 3 virtual environment  
- Streamlit  
- Open ports:  
  - **80** for HTTP  
  - **8501** for Streamlit  

---

## ⚙️ Server Setup Commands

```bash         
git clone https://github.com/Ruchi0214/Regexia.git
cd Regexia
python3 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
pip install -r requirements.txt
python -m pip install --upgrade pip
pip --version
streamlit run regexia_app.py
```
## 🛠️ Systemd Auto-Restart Setup
Create service file:
sudo nano /etc/systemd/system/regexia.service

```[Unit]
Description=Regexia Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Regexia
ExecStart=/home/ubuntu/Regexia/venv/bin/streamlit run regexia_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```
## Enable:

sudo systemctl daemon-reload
sudo systemctl enable regexia.service
sudo systemctl start regexia.service
---
## 📦 Requirements
- streamlit
- pandas
- matplotlib
- regex
- numpy
- sqlite3
- json

📊 Sample Output


## 🧠 Why Regexia Matters
Regexia brings:
- Transparency
- Explainability
- Speed
- Scalability
- Open-source ethics
It empowers journalists, researchers, analysts, and policy groups to understand how language shapes public opinion.

## 🏁 Final Notes
Regexia is not a toy project.
It is a prototype of a real-time linguistic intelligence system that could evolve into:
- A misinformation scanner
- A political discourse analytics engine
- A content authenticity verifier
- writer’s assistant for bias reduction

If you like this project, ⭐ star the repository!
