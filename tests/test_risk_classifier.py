from src.risk_classifier import classify_risk
from src.cdm_loader import load_cdms
from src.event_summarizer import summarize_events
from src.triage_queue import AlertQueue

import pandas as pd

def test_high_risk_flagged_actionable():
  assert classify_risk(-5.0) == "ACTIONABLE"      # Above '-6.0' cutoff

def test_low_risk_flagged_ignore():
  assert classify_risk(-10.2)=="IGNORE"           # Safe to ignore

def test_loader_keeps_all_columns_and_validates_required_columns(tmp_path):
  path = tmp_path / "cdms.csv"
  pd.DataFrame({
    "event_id": [1], "time_to_tca": [2.0], "risk": [-5.0],
    "miss_distance": [100.0], "unused_column": ["ignored"],
  }).to_csv(path, index=False)

  loaded = load_cdms(path)

  assert list(loaded.columns) == [
    "event_id", "time_to_tca", "risk", "miss_distance", "unused_column",
  ]

def test_summarizer_keeps_closest_warning_and_classifies_it():
  warnings = pd.DataFrame({
    "event_id": [1, 1, 2],
    "time_to_tca": [2.0, 0.5, 1.0],
    "risk": [-10.0, -5.0, -7.0],
    "miss_distance": [200.0, 100.0, 300.0],
  })

  summary = summarize_events(warnings).sort_values("event_id").reset_index(drop=True)

  assert summary["event_id"].tolist() == [1, 2]
  assert summary["risk"].tolist() == [-5.0, -7.0]
  assert summary["status"].tolist() == ["ACTIONABLE", "IGNORE"]

def test_alert_queue_returns_highest_risks_first():
  queue = AlertQueue()
  queue.add("low", -10.0)
  queue.add("high", -2.0)
  queue.add("middle", -6.0)

  assert queue.most_urgent(2) == [("high", -2.0), ("middle", -6.0)]

def test_priority_score_uses_multiple_signals():
  from src.priority_analysis import add_priority_score

  events = pd.DataFrame({
    "event_id": [1, 2],
    "risk": [-2.0, -10.0],
    "miss_distance": [100.0, 1000.0],
    "time_to_tca": [1.0, 10.0],
    "mahalanobis_distance": [20.0, 2.0],
    "risk_change": [3.0, -1.0],
  })

  scored = add_priority_score(events)

  assert scored.iloc[0]["event_id"] == 1
  assert scored["priority_score"].between(0, 1).all()