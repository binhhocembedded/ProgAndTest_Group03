FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --no-cache-dir \
    flask==3.0.3 \
    flask-cors==4.0.1 \
    pymysql==1.1.1 \
    cryptography==42.0.8 \
    PyJWT==2.8.0

COPY backend/ ./backend/
COPY UI_UX/ ./frontend/

ENV FLASK_APP=backend/app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "backend/app.py"]
