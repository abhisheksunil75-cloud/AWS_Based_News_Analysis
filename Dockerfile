FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8051
CMD ["streamlit", "run", "app.py", "--server.port=8051", "--server.address=0.0.0.0"]
