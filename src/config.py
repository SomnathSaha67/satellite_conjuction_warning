"""Settings used by the analysis experiment."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "sample_train_data.csv"
FULL_DATA_PATH = PROJECT_ROOT / "data" / "train_data.csv"
ACTIONABLE_THRESHOLD = -6.0
TOP_N = 5
OUTPUT_DIR = PROJECT_ROOT / "outputs"
