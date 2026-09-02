# Six Part 2 Replications Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three tested experiments and organize all six Part 2 replications for unambiguous grading.

**Architecture:** One small Python module implements the three additions using existing dependencies. A replication index and six numbered README directories separate the deliverables while generated evidence stays beside the experiment that produced it.

**Tech Stack:** Python 3.12, pandas, NumPy, scikit-learn, Matplotlib, `unittest`

**Spec:** `docs/superpowers/specs/2026-09-01-six-replications-design.md`

## Global Constraints

- Add no dependencies.
- Keep random state 42.
- Preserve the existing Adult Income metrics and public links.
- Do not claim AutoGluon feature parity; label the benchmark AutoML-style.
- Use chronological—not random—time-series evaluation.

---

### Task 1: Tested experiment functions

**Files:**
- Create: `tests/test_replications.py`
- Create: `src/replications.py`

**Interfaces:**
- Produces: `mine_association_rules(frame: DataFrame, min_support: float, min_confidence: float) -> DataFrame`
- Produces: `benchmark_models(frame: DataFrame, max_rows: int = 12000) -> DataFrame`
- Produces: `forecast_time_series(frame: DataFrame, test_months: int = 24) -> tuple[dict, DataFrame]`

- [x] Write tests with literal expected association support/confidence, four expected benchmark candidates, and chronological forecast output.
- [x] Run `python -m unittest tests/test_replications.py -v`; expect import failure for `src.replications`.
- [x] Implement direct pair counting, four-candidate cross-validation, and seasonal-naive/Ridge forecasting.
- [x] Run the new tests and the existing full suite.

### Task 2: Evidence generation

**Files:**
- Create: `replications/12_timeseries_forecasting/data/air_passengers.csv`
- Create: generated CSV/JSON/PNG artifacts under replications 04, 07, and 12

**Interfaces:**
- Consumes: `python -m src.replications`
- Produces: `rules.csv`, `metrics.csv`, `forecast.csv`, and three PNG figures

- [x] Download and validate the 144-row AirPassengers CSV from the documented R dataset mirror.
- [x] Run `python -m src.replications` and confirm every expected artifact exists.
- [x] Inspect all numerical results and figures before writing conclusions.

### Task 3: Six-project presentation

**Files:**
- Create: `replications/README.md`
- Create: six numbered replication README files for projects 03, 04, 06, 07, 11, and 12
- Modify: `README.md`
- Modify: `docs/RESULTS.md`
- Modify: `docs/PROMPTS_AND_PROCESS.md`

**Interfaces:**
- Consumes: verified generated evidence
- Produces: a grader-facing count of exactly six mapped replications

- [x] Write the six-project index and concise experiment conclusions.
- [x] Update the root README to say exactly six, link evidence, and disclose the supplemental-video requirement.
- [x] Run tests, both analysis commands, local-link validation, `git diff --check`, and artifact checks.
