import duckdb
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

views_df = duckdb.sql("SELECT * FROM 'data/content_views.parquet'").df()
content_df = duckdb.sql("SELECT * FROM 'data/content_metadata.parquet'").df()
adventurers_df = duckdb.sql("SELECT * FROM 'data/adventurer_metadata.parquet'").df()

df = views_df.merge(content_df, on='content_id').merge(adventurers_df, on='adventurer_id')
df = df.drop(columns=['rating', 'playlist_id', 'month_x', 'day_x', 'day_of_month_x', 'year_x', 'studio', 'minutes', 'title', 'month_y', 'day_y', 'day_of_month_y', 'year_y', 'age', 'name', 'honorific', 'gender', 'region', 'seconds_viewed', 'publisher_id'])

content_features = ["genre_id", "language_code"]
adventurer_features = ["primary_language", "favorite_genre"]

features = content_features + adventurer_features

categorical = ["genre_id", "language_code", "primary_language", "favorite_genre"]
numerical = []

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
    ]
)

X = preprocessor.fit_transform(df[features])

content_X = df[content_features].copy()
content_X["primary_language"] = None
content_X["favorite_genre"] = None

adventurer_X = df[adventurer_features].copy()
adventurer_X["genre_id"] = None
adventurer_X["language_code"] = None

all_X = pd.concat([content_X, adventurer_X], axis=0)
preprocessor.fit(all_X)

content_encoded = preprocessor.transform(content_X)
adventurer_encoded = preprocessor.transform(adventurer_X)

knn = NearestNeighbors(metric="cosine")
knn.fit(content_encoded)

def recommend_for_adventurer(adventurer_id, k=5):
    a_vec = adventurer_encoded[df['adventurer_id'] == adventurer_id]
    distances, indices = knn.kneighbors(a_vec, n_neighbors=k*50)  # extra neighbors
    candidate_content_ids = df.iloc[indices[0]]['content_id'].unique()

    viewed = set(views_df.loc[views_df['adventurer_id'] == adventurer_id, 'content_id'])
    recommended_ids = [c for c in candidate_content_ids if c not in viewed][:k]

    recommended_contents = content_df[content_df['content_id'].isin(recommended_ids)]
    return recommended_contents

advs = ["ih3j", "utgz", "2nxf"]

for adv in advs:
    recs = recommend_for_adventurer(adv)
    print(recs[['content_id', 'title', 'genre_id', 'language_code']])
