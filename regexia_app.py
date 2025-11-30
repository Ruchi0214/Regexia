# regexia_app.py
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

# -----------------------------------------------------------
# PATTERN LIBRARY LOADER
# Loads JSON regex packs from /patterns folder
# -----------------------------------------------------------

def load_pattern_library(pattern_dir="patterns"):
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

# ---------------- HELPERS ---------------- #

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
    # guard against non-string
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

# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(page_title="Regexia OS", layout="wide")
st.title("⌘ Regexia — Visual Pattern Intelligence Engine")
st.write("Visual command-style interface for regex-based text analysis (no typing required)")

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File Loaded Successfully")
    st.dataframe(df.head())

    # ---------------- TEXT COLUMN SELECTION ---------------- #
    text_like_cols = [col for col in df.columns if df[col].dtype == "object"]
    if not text_like_cols:
        st.error("❌ No text-like column found in the file.")
        st.stop()
    text_col = st.selectbox("Select the column that contains text:", text_like_cols)
    st.info(f"Using **{text_col}** as the text column.")

    # ---------------- PATTERN SELECTION ---------------- #
    st.markdown("## ⚙️ Step 2: Pattern Selection (Regex + Command UI)")
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

    # ---------------- BUILD FINAL REGEX ---------------- #
    final_rules = {}
    # add packs
    for pack in selected_packs:
        for i, rule_obj in enumerate(PATTERN_LIBRARY.get(pack, [])):
            final_rules[f"{pack} #{i+1}"] = rule_obj

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
            # allow raw regex if user writes it
            final_rules["Custom"] = re.compile(custom_word, re.I)
    if include_digits:
        final_rules["Digit Constraint"] = re.compile(r"\d+", re.I)

    # ---------------- COMMAND SIMULATION ---------------- #
    st.markdown("### 💻 Command Simulation (Preview)")
    cmd = f"regexia scan --file uploaded.csv --column {text_col}"
    if emotional: cmd += " --emotional"
    if exaggeration: cmd += " --exaggeration"
    if self_promote: cmd += " --selfpromote"
    if attack: cmd += " --attack"
    if numbers: cmd += " --numbers"
    if custom_word.strip(): cmd += f" --custom '{custom_word}'"
    if include_digits: cmd += " --digits"
    st.code(cmd)

    st.markdown("---")

    # ---------------- PARALLEL PROCESSING TOGGLE ---------------- #
    use_parallel = st.checkbox("⚡ Enable Parallel Processing (Faster for large files)")

    # ---------------- RUN BUTTON ---------------- #
    if st.button("▶ Run Pattern Analysis"):
        if not final_rules:
            st.warning("Please select at least ONE pattern to analyze")
            st.stop()

        st.info("Running analysis...")

        texts = df[text_col].astype(str).tolist()

        # Thread-based parallelism (safer cross-platform than spawn-based multiprocessing)
        if use_parallel:
            workers = min(8, (os.cpu_count() or 2))
            with ThreadPoolExecutor(max_workers=workers) as ex:
                results = list(ex.map(lambda t: apply_rules_to_text_simple(t, final_rules), texts))
            # results is list of (matches, score)
            all_results = []
            for (matches, score), text in zip(results, texts):
                row = {text_col: text}
                row.update(matches)
                row["Total Score"] = score
                all_results.append(row)
        else:
            all_results = []
            for text in texts:
                matches, score = apply_rules_to_text_simple(text, final_rules)
                row = {text_col: text}
                row.update(matches)
                row["Total Score"] = score
                all_results.append(row)

        # ---------------- CONVERT TO DATAFRAME ---------------- #
        result_df = pd.DataFrame(all_results)

        # ---------------- RESULTS TABLE ---------------- #
        st.subheader("📋 Results Preview")
        st.dataframe(result_df.head(20))

        # ---------------- SCORE GRAPH ---------------- #
        st.subheader("📊 Score Distribution")
        plt.figure(figsize=(8,4))
        plt.hist(result_df["Total Score"], bins=10)
        plt.xlabel("Total Pattern Matches")
        plt.ylabel("Number of Text Lines")
        st.pyplot(plt)

        # ---------------- RULE COUNTS ---------------- #
        st.subheader("🔥 Rule Hit Count")
        pattern_cols = [col for col in result_df.columns if col not in [text_col, "Total Score"]]
        if pattern_cols:
            rule_totals = result_df[pattern_cols].sum()
            st.bar_chart(rule_totals)
        else:
            st.info("No rule columns to chart.")

        # ---------------- TOP TEXTS ---------------- #
        st.subheader("⚠️ Highest Scoring Texts")
        st.dataframe(result_df.sort_values(by="Total Score", ascending=False).head(10))

        # ---------------- EXPLAINABILITY VIEW ---------------- #
        st.subheader("🔍 Explainability View (Highlighted Text)")
        st.write("The following text shows exactly which words triggered your selected patterns:")
        top_n = st.slider("Show top N texts", 3, 25, 8)
        top_rows = result_df.sort_values(by="Total Score", ascending=False).head(top_n)
        for idx, row in top_rows.iterrows():
            st.markdown(f"**Score: {row['Total Score']}**", unsafe_allow_html=True)
            highlighted_text = highlight_matches_in_text(row[text_col], final_rules)
            st.markdown(highlighted_text, unsafe_allow_html=True)
            st.markdown("---")

        # ---------------- EXPORT ---------------- #
        st.subheader("⬇ Download Your Results")
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(label="Download CSV", data=csv, file_name="regexia_results.csv", mime="text/csv")

        # ---------------- SAVE TO DATABASE ---------------- #
        if st.button("💾 Save Results to Database (SQLite)"):
            try:
                conn = sqlite3.connect("regexia_results.db")
                result_df.to_sql("analysis", conn, if_exists="replace", index=False)
                conn.close()
                st.success("Results saved to regexia_results.db")
            except Exception as e:
                st.error(f"Could not save DB: {e}")
