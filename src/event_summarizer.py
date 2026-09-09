"""Turn repeated warning rows into one understandable row per event."""

import numpy as np
import pandas as pd

from src.risk_classifier import classify_risk

def summarize_events(df: pd.DataFrame) -> pd.DataFrame:
  """Keep the closest-to-TCA row and add history and trend columns."""
  event_history = df.sort_values(["event_id", "time_to_tca"], ascending=[True, False])
  history = event_history.groupby("event_id")

  first_risk = history["risk"].first()
  warning_count = history.size().rename("warning_count")
  risk_change = (history["risk"].last() - first_risk).rename("risk_change")
  risk_std = history["risk"].std().fillna(0).rename("risk_std")

  most_recent_idx = df.groupby("event_id")["time_to_tca"].idxmin()

  final_rows = df.loc[most_recent_idx].copy()
  final_rows = final_rows.merge(warning_count, on="event_id")
  final_rows = final_rows.merge(risk_change, on="event_id")
  final_rows = final_rows.merge(risk_std, on="event_id")
  final_rows["risk_trend"] = np.select(
    [final_rows["risk_change"] > 0.5, final_rows["risk_change"] < -0.5],
    ["RISING", "FALLING"],
    default="STABLE",
  )
  final_rows["status"] = final_rows["risk"].map(classify_risk)
  return final_rows.reset_index(drop=True)