# 🧩 Regexia — Visual Pattern Intelligence System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Backend-Flask-green?style=for-the-badge&logo=flask)
![GCP](https://img.shields.io/badge/Deployment-Google_Cloud_Run-red?style=for-the-badge&logo=google-cloud)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker)
![Status](https://img.shields.io/badge/Status-Live_&_Secure-success?style=for-the-badge)

> **Transparent. Explainable. Offline-Capable. Open-Source.**

**Regexia** is a next-generation linguistic intelligence engine designed to detect bias, manipulation, misinformation patterns, and aggressive rhetoric inside political speeches and long-form text. 

Formerly a local Streamlit prototype, **Regexia v3.0** has been re-architected as a scalable **Flask Web Application** with a custom high-performance HTML/JS frontend, deployed globally via **Google Cloud Run**.

---

## 🎯 Problem Statement

In a world drowned in AI-generated content and manipulated narratives, it is increasingly difficult to determine:
* **Hidden Manipulation:** Which texts contain buried emotional triggers?
* **Rhetorical Attacks:** Are political messages coherent or purely aggressive?
* **Statistical Inflation:** Are claims artificially exaggerated?

Traditional tools are often slow, manual, and lack transparency. **Regexia solves this** by providing a real-time, explainable, regex-driven scanning engine.

---

## 💡 The Solution

Regexia provides a transparent, regex-driven linguistic scanning engine that detects:
* 🔥 **Emotional Triggers:** Fear, anger, and urgency cues.
* ⚔️ **Attack Vectors:** Ad hominem and aggressive language.
* 📢 **Exaggeration:** Hyperbolic phrases and absolute terms.

### **Core Features**
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
root@regexia:~$ system_ready... waiting_for_input

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

### **Key Technical Features**
* **Architecture:** Decoupled Flask Backend (API) + Custom HTML5/CSS3 Frontend.
* **Performance:** High-speed scanning using Python's `re` module and `Pandas` vectorization.
* **Visual Intelligence:** Cyberpunk-inspired UI with real-time DOM manipulation for results.
* **Explainability:** "Glass-box" design—users can see exactly *why* a text received a specific bias score.
* **Deployment:** Containerized with Docker and served via HTTPS on Serverless Cloud Infrastructure.

---

## 🏗️ System Architecture

Regexia follows a modular Model-View-Controller (MVC) pattern:

1.  **Input Layer:** User uploads CSV datasets via the Web Interface.
2.  **Processing Layer (Flask):** * Pandas parses the CSV.
    * The `Analyzer` engine scans text against `attack.json`, `emotional.json`, and `exaggeration.json`.
    * A scoring algorithm calculates the Risk Index (0-100%).
3.  **Presentation Layer (Frontend):**
    * Data is returned as JSON.
    * Vanilla JavaScript renders interactive tables and Plotly.js charts.
    * CSS Grid provides a responsive, modern experience.
<img width="1809" height="500" alt="image" src="https://github.com/user-attachments/assets/5a0a4dc6-ca8c-4942-8d96-85d29fc88085" />

### **Project Structure**
```bash
/Regexia-Bias-Engine
│── /static
│   ├── style.css          # Cyberpunk UI styling
│   └── script.js          # Async fetch logic & DOM rendering
│── /templates
│   └── index.html         # Main application interface
│── attack.json            # Dictionary: Aggressive rhetoric
│── emotional.json         # Dictionary: Emotional triggers
│── exaggeration.json      # Dictionary: Hyperbole detection
│── app.py                 # Flask Backend & API Routes
│── Dockerfile             # Container configuration for Cloud Run
│── requirements.txt       # Python dependencies
└── README.md              # Documentation
```
---
## 🚀 Getting Started (Local Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Ruchi0214/Regexia.git
cd Regexia
```
### 2️⃣ Install Dependencies - Regexia requires Python 3.9+ and a few lightweight libraries (Flask, Pandas, Gunicorn).
```
pip install -r requirements.txt
```
### 3️⃣ Launch the Engine - Start the Flask development server.
```
python app.py
```
### 4️⃣ Access @ http://127.0.0.1:5000 

---
---
## ☁️ Global Deployment - Google Cloud Compute Engine
### 1️⃣ Prepare the Environment
```
git clone [https://github.com/Ruchi0214/Regexia.git](https://github.com/Ruchi0214/Regexia.git)
cd Regexia
```
### 2️⃣ Service Configuration
```
gcloud services enable artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com
```
### 3️⃣ Production Deployment
--source . : Builds from the current directory.
--platform managed : Uses the fully managed Cloud Run platform.
--allow-unauthenticated : Makes the web app publicly accessible.
--region us-central1 : Deploys to the Iowa data center for low latency.
```
gcloud run deploy regexia-app \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```
### 4️⃣ Link @ https://regexia-app-293799990245.us-central1.run.app/ 

