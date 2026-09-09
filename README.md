# Satellite Conjunction Warning Prioritization System

## Project Overview

Satellite conjunction datasets can contain many warnings for the same possible close approach. This project processes those warnings, summarizes each event, and produces a ranked list for human review.

## Problem

Satellite operators may need to review a large number of warnings while having limited time and attention. Repeated warnings can make it difficult to identify which events deserve closer inspection first.

The project addresses this information-management problem by converting a large warning dataset into a smaller, structured, and ranked event summary.

## Solution

The system:

1. Loads the complete warning dataset.
2. Validates the required input fields.
3. Groups repeated warnings by event.
4. Selects the warning closest to the predicted time of closest approach.
5. Measures risk history and risk trend for each event.
6. Combines multiple signals into an experimental priority score.
7. Produces CSV and text reports for further review.

The priority score uses risk, miss distance, time to closest approach, uncertainty-related distance, and risk change. The scoring weights are explicit and can be adjusted for future experiments.

## What It Does

For each event, the system produces:

- A representative warning row
- Warning count
- Latest risk value
- Risk change across the warning history
- Risk variation
- Risk trend: rising, falling, or stable
- Individual priority signals
- Combined priority score
- Priority category: high, medium, or low

The repository includes a small sample dataset so that anyone can run the project immediately. The original local dataset contains 162,634 warning rows, 103 columns, and 13,154 unique events, but it is not committed because it exceeds GitHub's standard file-size limit.

## Dataset

The project uses the [Collision Avoidance Challenge dataset on Kaggle](https://www.kaggle.com/datasets/shadmanrohan/collisionavoidancechallenge). It contains repeated satellite conjunction-warning records, where each row represents one warning for a possible close-approach event. Important fields include:

- `event_id`: identifies the close-approach event.
- `time_to_tca`: time remaining until the predicted closest approach.
- `risk`: the risk value supplied by the dataset.
- `miss_distance`: predicted distance between the objects at closest approach.
- `mahalanobis_distance`: an uncertainty-related measurement used by the priority analysis when available.

Two dataset options are available:

- `data/sample_train_data.csv`: a small, committed demonstration dataset used by the default configuration. It lets readers run and inspect the project immediately after cloning it.
- `data/train_data.csv`: the larger local dataset used for the full analysis. It contains 162,634 rows and 103 columns, but is excluded from GitHub because it is approximately 222 MB.

To run the full analysis, download the dataset from Kaggle, extract the CSV, place it at `data/train_data.csv`, and change `DATA_PATH` in `src/config.py` to use it. The smaller sample remains the default so the project can still run immediately after cloning.

## System Architecture

```text
Input CSV
   |
   v
CDM Loader
   |
   v
Input Validation
   |
   v
Event Summarizer
   |-- selects one warning per event
   |-- calculates warning history and risk trend
   |
   v
Priority Analysis
   |-- normalizes multiple signals
   |-- calculates weighted priority score
   |
   v
Report Writer
   |-- event summary CSV
   |-- priority event CSV
   |-- column report
   |-- numeric statistics
   |-- text summary
```

### Main Components

- `src/cdm_loader.py`: loads the complete dataset and validates required columns.
- `src/event_summarizer.py`: creates one summary row per event and calculates history-based values.
- `src/risk_classifier.py`: provides the baseline risk classification rule.
- `src/priority_analysis.py`: calculates normalized signals and the combined priority score.
- `src/triage_queue.py`: maintains the highest-scoring events using binary-search insertion.
- `src/report_writer.py`: writes analysis results to CSV and text files.
- `src/config.py`: stores paths and runtime settings.
- `src/main.py`: coordinates the complete workflow.
- `tests/`: contains automated tests for the main behaviors.

## Advantages

- **Transparent scoring:** Each priority result is based on visible input signals and documented weights.
- **Practical:** Large warning files are converted into manageable event-level reports.
- **Data-preserving:** All original input columns remain available for inspection and future analysis.
- **Modular:** Loading, summarization, scoring, queue management, and reporting are separated into independent components.
- **Tested:** The core functionality is covered by automated tests.
- **Extensible:** Additional signals, validation rules, reports, or visualizations can be added later.
- **Accessible:** The output files can be opened in common spreadsheet applications without requiring a database or web interface.

## Disadvantages and Scope

- The system depends on the quality and meaning of the supplied risk values.
- The priority weights are experimental and have not been validated against operational decisions.
- The system does not independently calculate collision probability or orbital mechanics.
- The current workflow processes a local CSV file rather than a live data feed.
- The ranking is intended to support human review, not replace professional satellite operators.
- The project does not recommend maneuvers or guarantee that an event is safe to ignore.

## Tools and Frameworks

- **Python:** application programming language
- **pandas:** CSV loading, grouping, filtering, statistics, and report preparation
- **NumPy:** numerical calculations and priority categorization
- **pytest:** automated testing
- **Python `bisect`:** ordered event insertion using binary search
- **CSV and TXT files:** input and output formats


## Setup

Install Python 3.10 or newer, then install the project dependencies:

```bash
python -m pip install pandas numpy pytest
```

The default demonstration dataset is:

```text
data/sample_train_data.csv
```

The larger local dataset can be used by changing `DATA_PATH` in `src/config.py` to `data/train_data.csv`. That file is intentionally ignored by Git because of its size.

## Running the Application

From the project directory, run:

```bash
python -m src.main
```

The program reads the sample dataset and creates an `outputs/` directory containing:

- `event_summary.csv`: one scored row per event
- `actionable_events.csv`: high- and medium-priority events
- `column_report.csv`: data type, missing values, and unique values for every input column
- `numeric_statistics.csv`: descriptive statistics for numeric columns
- `summary.txt`: a concise execution summary

## Running the Tests

Run the automated tests with:

```bash
python -m pytest tests/
```

The tests cover input loading, validation, event summarization, risk classification, multi-signal scoring, and priority ordering.
