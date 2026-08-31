# CMPE 255 Assignment 1 Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible Adult Income data-science portfolio with tested code, generated evidence, and submission-ready documentation.

**Architecture:** A single Python analysis module downloads and validates the data, runs classification, clustering, anomaly detection, and writes machine-readable plus visual artifacts. Markdown deliverables explain the method, results, prompts, and recording journey.

**Tech Stack:** Python 3.12, pandas, NumPy, scikit-learn, Matplotlib, standard-library `unittest`

**Spec:** `docs/superpowers/specs/2026-08-31-assignment-1-portfolio-design.md`

## Global Constraints

- Keep the unrelated Ansible design file unchanged.
- Use only the UCI-hosted Adult data files; cite the Kaggle mirror in documentation.
- Fix random seeds at 42 and prevent preprocessing leakage with scikit-learn pipelines.
- Do not publish externally or change repository visibility before user review.

---

### Task 1: Tested analysis core

**Files:**
- Create: `tests/test_analysis.py`
- Create: `src/analysis.py`
- Create: `requirements.txt`

**Interfaces:**
- Produces: `load_adult(path: Path) -> pandas.DataFrame`, `clean_adult(frame: pandas.DataFrame) -> pandas.DataFrame`, and `run_analysis(frame: pandas.DataFrame, output_dir: Path) -> dict`

- [x] Write fixture-based tests that reject a malformed schema, normalize missing markers and target punctuation, and return deterministic classifier metrics.
- [x] Run `python -m unittest discover -s tests -v` and verify failure because `src.analysis` does not exist.
- [x] Implement the smallest complete pipeline using scikit-learn `Pipeline` and `ColumnTransformer`.
- [x] Run the unit tests and verify they pass.

### Task 2: Generate evidence

**Files:**
- Create: `artifacts/metrics.csv`
- Create: `artifacts/summary.json`
- Create: `artifacts/figures/*.png`
- Create: `docs/RESULTS.md`

**Interfaces:**
- Consumes: `python -m src.analysis`
- Produces: reproducible results referenced by the README and article draft

- [x] Run `python -m src.analysis` against the complete dataset.
- [x] Confirm the command exits zero and every declared artifact exists.
- [x] Inspect metrics for finite values and compare learned models with the dummy baseline.

### Task 3: Submission narrative

**Files:**
- Create: `README.md`
- Create: `docs/PROMPTS_AND_PROCESS.md`
- Create: `.gitignore`

**Interfaces:**
- Consumes: generated results from Task 2
- Produces: public-repository and recording-ready assignment deliverables

- [x] Write a concise README organized as Assignment 1 with source, setup, results, artifacts, limitations, and publishing checklist.
- [x] Document the original/adapted prompts without claiming a fabricated verbatim chat transcript.
- [x] Draft a paraphrased article and publish an end-to-end YouTube walkthrough grounded in measured outputs.
- [x] Run the full test suite and pipeline again, inspect `git diff --check`, and compare the repository against the assignment checklist.
