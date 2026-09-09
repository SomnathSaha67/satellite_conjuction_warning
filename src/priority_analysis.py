"""Create a transparent priority score from several easy-to-explain signals."""

import numpy as np
import pandas as pd

SIGNAL_WEIGHTS = {
  "risk_signal": 0.40,
  "distance_signal": 0.20,
  "time_signal": 0.15,
  "uncertainty_signal": 0.15,
  "trend_signal": 0.10,
}

def _percentile(values: pd.Series) -> pd.Series:
  """Put different units on the same 0-to-1 scale."""
  return values.rank(pct=True, method="average").fillna(0.0)

def add_priority_score(events: pd.DataFrame) -> pd.DataFrame:
  """Add signals, a weighted score, and a priority label to event summaries."""
  result = events.copy()
  result["risk_signal"] = _percentile(result["risk"])
  result["distance_signal"] = 1 - _percentile(result["miss_distance"])
  result["time_signal"] = 1 - _percentile(result["time_to_tca"])
  uncertainty = result.get("mahalanobis_distance", pd.Series(0.0, index=result.index))
  result["uncertainty_signal"] = _percentile(uncertainty)
  result["trend_signal"] = _percentile(result["risk_change"])
  result["priority_score"] = sum(
    result[column] * weight for column, weight in SIGNAL_WEIGHTS.items()
  )
  result["priority"] = np.select(
    [result["priority_score"] >= 0.75, result["priority_score"] >= 0.45],
    ["HIGH", "MEDIUM"],
    default="LOW",
  )
  return result.sort_values("priority_score", ascending=False).reset_index(drop=True)

def build_dataset_report(df: pd.DataFrame) -> pd.DataFrame:
  """Describe every input column without treating every column as a risk signal."""
  return pd.DataFrame({
    "column": df.columns,
    "data_type": [str(value) for value in df.dtypes],
    "missing_values": [int(value) for value in df.isna().sum()],
    "unique_values": [int(value) for value in df.nunique(dropna=False)],
  })

def build_event_statistics(events: pd.DataFrame) -> pd.DataFrame:
  """Return numeric event statistics for spreadsheet inspection."""
  numeric_columns = events.select_dtypes(include=np.number).columns
  return events[numeric_columns].describe().transpose().reset_index(names="column")