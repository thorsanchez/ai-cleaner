import requests
import pandas as pd

API_URL = "https://dummyjson.com/comments"

def fetch_comments(limit: int =20) -> pd.DataFrame:
    response = requests.get(API_URL)
    response.raise_for_status

    data = response.json()

    comments_list = data.get("comments", [])
    df = pd.DataFrame(comments_list)
    df = df.head(limit)

    return df[['body']]
#print(fetch_comments(4))