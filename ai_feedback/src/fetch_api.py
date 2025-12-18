import requests
import pandas as pd

API_URL = "https://dummyjson.com/comments"

def fetch_comments(limit: int = 20) -> pd.DataFrame:
    #fetch comment fra api og return pandas Dataframe
    response = requests.get(API_URL)
    response.raise_for_status #stoppa ef api villa

    data = response.json()

    #extract nested body sem er i comments
    comments_list = data.get("comments", [])



    #convert yfir í DataFrame
    df = pd.DataFrame(comments_list)
    #geyma fyrstu 20 bara 
    df = df.head(limit)

    #bara geyma þessa dalka
    return df[['body']]

#print(fetch_comments(2))