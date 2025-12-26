import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/customer_feedback.csv")

def fetch_csv_feedback() -> pd.DataFrame:
    """
    Sækja customer feedback fra csv skra og skila datafram
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"CSV finnst ekki {DATA_PATH}. "
        )

    df = pd.read_csv(DATA_PATH)

    if "feedback" not in df.columns:
        raise ValueError("Vantar 'feedback' column i csv")

    return df[["feedback"]]
