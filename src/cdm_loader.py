"""Read and validate the complete warning table."""

import pandas as pd

REQUIRED_COLUMNS = ["event_id", "time_to_tca", "risk", "miss_distance"]

def load_cdms(path: str) -> pd.DataFrame:
  """Read every column so later analysis can inspect the full dataset."""
  df = pd.read_csv(path)
  missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
  if missing_columns:
    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
  if df.empty:
    raise ValueError("The input file contains no warning rows")
  if df[REQUIRED_COLUMNS].isna().any().any():
    raise ValueError("Required columns contain missing values")
  return df