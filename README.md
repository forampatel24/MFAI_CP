# Stability- and Confidence-Aware Explainable AI Decision System

## Overview
This project implements an explainable AI decision system that provides:

- Decision (Eligible / Not Eligible)
- Confidence Score (%)
- Stability Score (%)
- Human-readable explanation

The system is rule-based and does not use machine learning.

---

## Key Features

- Rule-based decision logic using propositional reasoning
- Probabilistic confidence calculation using rule weights
- Stability analysis using perturbation-based sensitivity testing
- Eigenvalue-based interpretation of system sensitivity
- Terminal-based output

---

## Concepts Used

- Vectors and linear combinations
- Matrix operations
- Eigenvalues (for sensitivity analysis)
- Propositional logic and inference
- Probabilistic reasoning

---

## How It Works

1. Input data is read from dataset
2. Rules are applied to determine decision
3. Confidence is calculated based on satisfied rules
4. Inputs are slightly varied (perturbation)
5. Stability is calculated based on decision consistency
6. Results are printed with explanation

---

## Dataset

The dataset is used only for input examples.
