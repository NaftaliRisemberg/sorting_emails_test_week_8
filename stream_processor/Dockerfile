FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY app.py .
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]