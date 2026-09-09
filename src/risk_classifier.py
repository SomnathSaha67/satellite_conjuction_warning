"""
Labels each warning ACTIONABLE or IGNORE.
"""

from src.config import ACTIONABLE_THRESHOLD

def classify_risk(risk_value: float) -> str:
  return "ACTIONABLE" if risk_value >= ACTIONABLE_THRESHOLD else "IGNORE"