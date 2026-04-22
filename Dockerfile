FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY UI_UX/ ./frontend/

ENV FLASK_APP=backend/app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "backend/app.py"]
