# regexia_app.py  (improved, safe, copy-paste ready)
import streamlit as st
import pandas as pd
import re
import json
import glob
import os
import matplotlib.pyplot as plt
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import math
import hashlib
from io import BytesIO

st.set_page_config(page_title="Regexia OS", layout="wide")

# ---------------- Cached pattern loader ---------------- #
@st.cache_resource
def load_pattern_library(pattern_dir="patterns"):
    """
    Load JSON pattern packs from patterns/ folder and compile them.
    Cached so subsequent reruns do not re-read files.
    """
    library = {}
    if not os.path.exists(pattern_dir):
        return library
    for pf in glob.glob(os.path.join(pattern_dir, "*.json")):
        try:
            with open(pf, "r", encoding="utf-8") as f:
                data = json.load(f)
            name = data.get("name", os.path.basename(pf))
            patterns = data.get("patterns", [])
            compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
            library[name] = compiled
        except Exception as e:
            print("Error loading pattern pack:", pf, e)
    return library

PATTERN_LIBRARY = load_pattern_library()

# ---------------- Helpers ---------------- #
def split_into_chunks(text_series, chunk_size=5):
    all_chunks = []
    for idx, text in text_series.items():
        if pd.isna(text) or not isinstance(text, str):
            continue
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        for i in range(0, len(sentences), chunk_size):
            chunk = ' '.join(sentences[i:i+chunk_size])
            if chunk:
                all_chunks.append({'chunk_id': f'{idx}_{i}', 'chunk_text': chunk})
    return pd.DataFrame(all_chunks)

def apply_rules_to_text_simple(text, rules_dict):
    matches = {}
    score = 0
    for name, pattern in rules_dict.items():
        try:
            c = len(pattern.findall(text))
        except Exception:
            c = 0
        matches[name] = c
        score += c
    return matches, score

def highlight_matches_in_text(text, rules_dict):
    if text is None:
        return ""
    text = str(text)
    spans = []
    for name, regex in rules_dict.items():
        for m in regex.finditer(text):
            spans.append((m.start(), m.end()))
    if not spans:
        return text
    spans = sorted(spans, key=lambda x: x[0])
    merged = [list(spans[0])]
    for s, e in spans[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    html = ""
    last = 0
    for s, e in merged:
        html += text[last:s]
        html += f"<mark style='background: #fff176'>{text[s:e]}</mark>"
        last = e
    html += text[last:]
    return html

def get_uploaded_file_size(uploaded_file):
    # uploaded_file may be an UploadedFile with .size or we compute from .getbuffer()
    try:
        if hasattr(uploaded_file, "size"):
            return int(uploaded_file.size)
        # fallback
        return len(uploaded_file.getvalue())
    except Exception:
        return None

def make_run_key(file_name, file_size, text_col, options_dict):
    """
    Create a deterministic run key so we can cache results in session_state.
    """
    key_src = f"{file_name}|{file_size}|{text_col}|{json.dumps(options_dict, sort_keys=True)}"
    return hashlib.sha256(key_src.encode("utf-8")).hexdigest()

# ---------------- UI ---------------- #
st.title("⌘ Regexia — Visual Pattern Intelligence Engine")
st.write("Visual command-style interface for regex-based text analysis (no typing required)")

# ---------------- File Upload ---------------- #
uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])

if not uploaded_file:
    st.info("Upload a CSV to begin. Example sample data included in repository.")
    st.stop()

# get uploaded file info
file_size = get_uploaded_file_size(uploaded_file) or 0
file_name = getattr(uploaded_file, "name", "uploaded.csv")
file_mb = file_size / (1024*1024) if file_size else 0

st.success(f"✅ File loaded: **{file_name}** ({file_mb:.2f} MB)")
# read file into dataframe (use BytesIO to safely rewind)
try:
    # Use BytesIO to allow repeated reads if Streamlit reruns
    uploaded_bytes = uploaded_file.getvalue()
    df = pd.read_csv(BytesIO(uploaded_bytes))
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

st.dataframe(df.head())

# ---------------- Text Column Selection ---------------- #
text_like_cols = [col for col in df.columns if df[col].dtype == "object"]
if not text_like_cols:
    st.error("❌ No text-like columns detected. Make sure your CSV has at least one column with text.")
    st.stop()

text_col = st.selectbox("Select the column that contains text:", text_like_cols)
st.info(f"Using **{text_col}** as the text column.")

# ---------------- Safety for large files ---------------- #
MAX_SAFE_MB = 10
if file_mb > MAX_SAFE_MB:
    st.warning(f"⚠️ The uploaded file is large ({file_mb:.2f} MB). Processing may take a long time on this machine.")
    proceed_large = st.checkbox("I understand and want to process this large file (may take several minutes)")
    if not proceed_large:
        st.stop()

# ---------------- Pattern Selection (use a form to batch settings) ---------------- #
with st.form("pattern_form"):
    st.markdown("## ⚙️ Pattern Selection (Regex + Command UI)")
    st.markdown("### 📚 Pattern Library (JSON Packs)")
    if PATTERN_LIBRARY:
        selected_packs = st.multiselect("Choose Pattern Packs", list(PATTERN_LIBRARY.keys()))
    else:
        st.info("No JSON pattern packs found in /patterns folder.")
        selected_packs = []

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📌 Predefined Patterns")
        emotional = st.checkbox("Emotional Words (crisis, fear, danger)")
        numbers = st.checkbox("Numbers / Percentages")
        exaggeration = st.checkbox("Exaggeration (always, 100%, never)")
        self_promote = st.checkbox("Self Promotion (only I, trust me)")
        attack = st.checkbox("Attack Words (fake, corrupt, enemy)")
    with col2:
        st.markdown("### 🛠 Visual Regex Builder")
        custom_word = st.text_input("Specific word or phrase")
        include_digits = st.checkbox("Must contain numbers (0-9)")
        exact_match = st.checkbox("Exact word match only")

    use_parallel = st.checkbox("⚡ Enable Parallel Processing (Faster for large files)")

    submitted = st.form_submit_button("▶ Run Pattern Analysis")

# ---------------- Build final_rules (compiled regex dict) ---------------- #
final_rules = {}
# add packs from PATTERN_LIBRARY (each pack may be a list of compiled regex)
for pack in selected_packs:
    for i, rule_obj in enumerate(PATTERN_LIBRARY.get(pack, [])):
        final_rules[f"{pack} #{i+1}"] = rule_obj

# builtin patterns
if emotional:
    final_rules["Emotional"] = re.compile(r"\b(crisis|fear|danger|threat|panic)\b", re.I)
if exaggeration:
    final_rules["Exaggeration"] = re.compile(r"\b(100%|always|never|guaranteed|best)\b", re.I)
if self_promote:
    final_rules["Self Promotion"] = re.compile(r"\b(I alone|only I|trust me)\b", re.I)
if attack:
    final_rules["Attack"] = re.compile(r"\b(fake|corrupt|enemy|liar)\b", re.I)
if numbers:
    final_rules["Numbers"] = re.compile(r"\d+", re.I)
if custom_word.strip():
    if exact_match:
        final_rules["Custom"] = re.compile(fr"\b{re.escape(custom_word)}\b", re.I)
    else:
        final_rules["Custom"] = re.compile(custom_word, re.I)
if include_digits:
    final_rules["Digit Constraint"] = re.compile(r"\d+", re.I)

# ---------------- Prepare run key to cache results in session_state ---------------- #
options = {
    "packs": selected_packs,
    "emotional": emotional,
    "exaggeration": exaggeration,
    "self_promote": self_promote,
    "attack": attack,
    "numbers": numbers,
    "custom_word": custom_word,
    "include_digits": include_digits,
    "exact_match": exact_match,
    "use_parallel": use_parallel
}
run_key = make_run_key(file_name, file_size, text_col, options)

# If results previously computed for same run_key, show cached results
if submitted and run_key in st.session_state and st.session_state.get("last_run_key") == run_key:
    st.info("Using cached results from previous run.")
    result_df = st.session_state["result_df"]
else:
    result_df = None

# ---------------- Process only when user clicks submit ---------------- #
if submitted:
    if not final_rules:
        st.warning("Please select at least ONE pattern to analyze")
        st.stop()

    # If cached and same key, we already loaded above
    if result_df is None:
        st.info("Running analysis... (this may take time for large files)")
        texts = df[text_col].astype(str).tolist()
        total = len(texts)
        progress_bar = st.progress(0)
        status_text = st.empty()

        all_results = []
        try:
            if use_parallel:
                workers = min(8, (os.cpu_count() or 2))
                status_text.text(f"Processing {total} texts using {workers} threads...")
                with ThreadPoolExecutor(max_workers=workers) as ex:
                    # ex.map returns iterator; iterate to update progress
                    for i, (matches_score) in enumerate(ex.map(lambda t: apply_rules_to_text_simple(t, final_rules), texts), start=1):
                        matches, score = matches_score
                        text = texts[i-1]
                        row = {text_col: text}
                        row.update(matches)
                        row["Total Score"] = score
                        all_results.append(row)
                        if i % 10 == 0 or i == total:
                            progress_bar.progress(min(i/total, 1.0))
            else:
                status_text.text(f"Processing {total} texts sequentially...")
                for i, text in enumerate(texts, start=1):
                    matches, score = apply_rules_to_text_simple(text, final_rules)
                    row = {text_col: text}
                    row.update(matches)
                    row["Total Score"] = score
                    all_results.append(row)
                    if i % 10 == 0 or i == total:
                        progress_bar.progress(min(i/total, 1.0))

            result_df = pd.DataFrame(all_results)
            st.session_state["result_df"] = result_df
            st.session_state["last_run_key"] = run_key
            status_text.success("Analysis complete.")
        except Exception as e:
            st.error(f"Processing failed: {e}")
            st.stop()

# ---------------- If we have results, render them ---------------- #
if result_df is not None and not result_df.empty:
    st.subheader("📋 Results Preview")
    st.dataframe(result_df.head(20))

    # Score histogram
    st.subheader("📊 Score Distribution")
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.hist(result_df["Total Score"], bins=10)
    ax.set_xlabel("Total Pattern Matches")
    ax.set_ylabel("Number of Text Lines")
    st.pyplot(fig)

    # Rule counts
    st.subheader("🔥 Rule Hit Count")
    pattern_cols = [col for col in result_df.columns if col not in [text_col, "Total Score"]]
    if pattern_cols:
        rule_totals = result_df[pattern_cols].sum()
        st.bar_chart(rule_totals)
    else:
        st.info("No rule columns to chart.")

    # Top texts
    st.subheader("⚠️ Highest Scoring Texts")
    st.dataframe(result_df.sort_values(by="Total Score", ascending=False).head(10))

    # Explainability view
    st.subheader("🔍 Explainability View (Highlighted Text)")
    st.write("The following text shows exactly which words triggered your selected patterns:")
    top_n = st.slider("Show top N texts", 3, 25, 8)
    top_rows = result_df.sort_values(by="Total Score", ascending=False).head(top_n)
    for idx, row in top_rows.iterrows():
        st.markdown(f"**Score: {row['Total Score']}**", unsafe_allow_html=True)
        highlighted_text = highlight_matches_in_text(row[text_col], final_rules)
        st.markdown(highlighted_text, unsafe_allow_html=True)
        st.markdown("---")

    # Download
    st.subheader("⬇ Download Your Results")
    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="Download CSV", data=csv, file_name="regexia_results.csv", mime="text/csv")

    # Save to SQLite
    if st.button("💾 Save Results to Database (SQLite)"):
        try:
            conn = sqlite3.connect("regexia_results.db")
            result_df.to_sql("analysis", conn, if_exists="replace", index=False)
            conn.close()
            st.success("Results saved to regexia_results.db")
        except Exception as e:
            st.error(f"Could not save DB: {e}")

else:
    if not submitted:
        st.info("Configure patterns and click ▶ Run Pattern Analysis to process the uploaded file.")
    else:
        st.info("No results produced (empty dataset or no matches).")
