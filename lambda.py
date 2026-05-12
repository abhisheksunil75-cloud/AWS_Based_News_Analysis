import json
import os
import pg8000
import requests
import boto3
from textblob import TextBlob
from datetime import datetime

# Initialize S3 client OUTSIDE (better for Lambda performance)
s3 = boto3.client('s3')

def run_pipeline():
    
    API_KEY = os.environ.get("NEWS_API_KEY")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&pageSize=10&apiKey={API_KEY}"

    conn = pg8000.connect(
        host="news-db.c70wyi68w8wm.ap-south-1.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password=DB_PASSWORD,
        port=5432
    )
    cur = conn.cursor()

    try:
        # Create table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id SERIAL PRIMARY KEY,
                title TEXT,
                description TEXT UNIQUE,
                sentiment FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Fetch news
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("Error fetching news:", response.text)
            return

        data = response.json()
        articles = data.get('articles', [])

        print("Total Articles:", len(articles))

        # ✅ Store raw data in S3 (with timestamp)
        key = f"news/raw_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        s3.put_object(
            Bucket="news-task",
            Key=key,
            Body=json.dumps(articles)
        )

        # Process articles
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")

            text = f"{title}. {description}"

            sentiment_score = TextBlob(text).sentiment.polarity

            print(f"Title: {title}")
            print(f"Sentiment: {sentiment_score}")
            print("-" * 50)

            # Insert with conflict handling
            cur.execute(
                """INSERT INTO news(title, description, sentiment)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (description) DO NOTHING""",
                (title, description, sentiment_score)
            )

        conn.commit()

    except Exception as e:
        print("Error occurred:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()
        print("✅ Connection closed safely")


# 🔥 Lambda entry point
def lambda_handler(event, context):
    run_pipeline()
    return {
        "statusCode": 200,
        "body": json.dumps("Pipeline executed successfully!")
    }
