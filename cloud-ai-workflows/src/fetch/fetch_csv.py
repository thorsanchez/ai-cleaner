import pandas as pd
import io
import requests

#old real tickets
CSV_URL = "https://raw.githubusercontent.com/stephen-talari/public/main/sample-servicenow-incidents.csv"

def fetch_csv_feedback(limit: int = 20) -> pd.DataFrame:
    """
    Fetch frá public git
    skilar datframe með ticket texta og metadata
    """
    try:
        response = requests.get(CSV_URL, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Eror donwloading csv: {e}")

    # Lesa csv
    df = pd.read_csv(io.StringIO(response.text))

    # short_description og description fyrir texta
    required_cols = ['short_description', 'description']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing cols in csv: {missing}")

    # sameina fyrir llm input
    df['title'] = df['short_description'].fillna("")
    df['description'] = df['description'].fillna("")
    df['text'] = df['title'] + "\n\n" + df['description']

    # fleiri mikilvæg data
    df.rename(columns={
        "number": "ticket_id",
        "priority": "reported_severity",
        "category": "category"
    }, inplace=True)

    # hreinsa og limit
    df = df.dropna(subset=['text'])
    df['text'] = df['text'].str.strip()
    df = df.head(limit)
    df['source'] = "csv_servicenow_incidents"

    cols = ['ticket_id', 'text', 'title', 'description', 'reported_severity', 'category', 'source']
    return df[[col for col in cols if col in df.columns]]


#Test
if __name__ == "__main__":
    df = fetch_csv_feedback(5)
    print(df[['title', 'text']].head(3))