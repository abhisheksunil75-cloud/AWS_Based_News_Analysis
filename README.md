# AWS Based News Analysis

An end-to-end, serverless data pipeline and interactive web dashboard built entirely on AWS. This project automates the ingestion of live news data, performs real-time sentiment analysis, and serves the insights through a containerized web application.

## 🏗️ Cloud Architecture

The system is broken down into two decoupled microservices: a backend data-fetching pipeline and a frontend presentation layer.

* **Automation:** AWS EventBridge triggers the pipeline on a 5-minute cron schedule.
* **Compute (Backend):** AWS Lambda executes the Python extraction script, pulling live data from the News API.
* **Processing:** TextBlob is utilized within Lambda to calculate sentiment scores for each article.
* **Storage:** * Analyzed data is pushed to a live **Amazon RDS (MySQL)** database.
    * Raw JSON payloads are backed up to an **Amazon S3** bucket.
* **Containerization:** The frontend application is packaged using Docker and stored in **Amazon ECR**.
* **Compute (Frontend):** **Amazon ECS (AWS Fargate)** hosts the Streamlit web server continuously, exposing the dashboard to the public internet on port 8051.

## 🛠️ Technology Stack
* **Cloud:** AWS (EventBridge, Lambda, S3, RDS, ECR, ECS Fargate)
* **Language:** Python 3.12
* **Database:** MySQL
* **Frontend:** Streamlit
* **Containerization:** Docker

## 🚀 Deployment Notes
The frontend dashboard is designed to run statelessly on AWS Fargate. To deploy locally for testing:

1. Clone the repository.
2. Build the Docker image: `docker build -t news-dashboard .`
3. Run the container: `docker run -p 8051:8051 news-dashboard`
4. Access the application at `http://localhost:8051`
