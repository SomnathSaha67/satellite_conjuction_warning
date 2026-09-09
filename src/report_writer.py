"""Write analysis results to files that can be opened in a spreadsheet."""

from pathlib import Path

import pandas as pd


def write_reports(
  raw_data: pd.DataFrame,
  scored_events: pd.DataFrame,
  output_dir: Path,
) -> None:
  """Create CSV and text reports without requiring charting software."""
  output_dir.mkdir(parents=True, exist_ok=True)

  scored_events.to_csv(output_dir / "event_summary.csv", index=False)
  scored_events[scored_events["priority"].isin(["HIGH", "MEDIUM"])].to_csv(
    output_dir / "actionable_events.csv", index=False,
  )

  column_report = pd.DataFrame({
    "column": raw_data.columns,
    "data_type": [str(value) for value in raw_data.dtypes],
    "missing_values": [int(value) for value in raw_data.isna().sum()],
    "unique_values": [int(value) for value in raw_data.nunique(dropna=False)],
  })
  column_report.to_csv(output_dir / "column_report.csv", index=False)

  numeric_statistics = raw_data.select_dtypes(include="number").describe().transpose()
  numeric_statistics.to_csv(output_dir / "numeric_statistics.csv")

  high_priority = int((scored_events["priority"] == "HIGH").sum())
  medium_priority = int((scored_events["priority"] == "MEDIUM").sum())
  rising_risk = int((scored_events["risk_trend"] == "RISING").sum())
  report = [
    "Satellite alert analysis summary",
    "================================",
    f"Warning rows read: {len(raw_data)}",
    f"Columns read: {len(raw_data.columns)}",
    f"Unique events: {scored_events['event_id'].nunique()}",
    f"High priority events: {high_priority}",
    f"Medium priority events: {medium_priority}",
    f"Rising-risk events: {rising_risk}",
    "",
    "Files:",
    "- event_summary.csv: one scored row per event",
    "- actionable_events.csv: HIGH and MEDIUM priority events",
    "- column_report.csv: data type, missing values, and unique values for every input column",
    "- numeric_statistics.csv: pandas statistics for every numeric input column",
  ]
  (output_dir / "summary.txt").write_text("\n".join(report), encoding="utf-8")
