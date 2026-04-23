# 🎓 Explainable Student Performance Analysis System

## 📌 Overview

This project implements a **rule-based Explainable AI system** for analyzing student performance.

It predicts whether a student will **PASS or FAIL** based on academic, behavioral, and lifestyle factors, and provides:

- ✔ Decision (PASS / FAIL)
- ✔ Confidence Score (%)
- ✔ Stability / Robustness (%)
- ✔ Human-readable explanation
- ✔ Bulk analysis for entire datasets

This system is **NOT machine learning-based**. It uses **logic, probability, and simulation techniques**.

---

## 🚀 Features

### 🔹 1. Single Student Analysis
- Analyze one student at a time
- Full explanation of decision
- Shows:
  - Logical rules triggered
  - Confidence level
  - Stability of decision
  - Key influencing factors

---

### 🔹 2. Bulk Analysis (CSV)
- Upload `.csv` 
- Analyze **entire dataset (400+ students)**
- Outputs:
  - PASS / FAIL for each student
  - Confidence & Stability scores
  - Summary dashboard
  - Graphs (distribution)
  - Filtered results
  - High-risk students list

---

### 🔹 3. Explainability
- Human-readable rules (not symbols)
- Shows *why* a decision was made
- Helps teachers understand results easily

---

### 🔹 4. Confidence (Probabilistic Reasoning)
- Based on **conditional probability**
- Measures how strongly evidence supports a decision

\[
P(\text{Decision} \mid \text{Evidence}) = \frac{\text{Support for Decision}}{\text{Total Support}}
\]

---

### 🔹 5. Stability / Robustness
- Uses **Monte Carlo perturbation**
- Slightly changes input values and checks:
  - Does decision change?
- Measures **how reliable the decision is**

---

## 🧠 Concepts Used

This project covers syllabus topics:

### ✔ Mathematical Foundations
- Vectors (feature representation)
- Weighted scoring system

### ✔ Logic
- Propositional logic
- Rule-based inference

### ✔ Probabilistic Reasoning
- Conditional probability
- Evidence-based decision making

### ✔ Simulation
- Monte Carlo perturbation for robustness

---

## ⚙️ How It Works

1. Input student data
2. Convert data → logical facts
3. Apply rules (PASS / FAIL)
4. Compute scores
5. Calculate confidence
6. Perform perturbation (stability test)
7. Display results with explanation

---

## 📊 Dataset

- Student dataset (`student-mat.csv`)
- Used only as **input data**
- No training involved

---

## 🖥️ User Interface

Built using **Streamlit**

### Modes:
- 🔍 Single Student Mode
- 📊 Bulk Analysis Mode

### Features:
- Sidebar navigation
- Clean dashboard
- Graphs and tables
- File upload support

---

## 📁 File Structure
project/
│
├── frontend_combined.py # Main UI (Single + Bulk)
├── rules.py # Rule definitions
├── utils.py # Inference & decision logic
├── confidence.py # Confidence calculation
├── stability.py # Robustness analysis
├── student-mat.csv # Dataset
└── README.md


---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install streamlit pandas

python -m streamlit run app.py
http://localhost:8501