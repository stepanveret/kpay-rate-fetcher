FROM python:3.9-slim

ENV LANG=C.UTF-8 \
    TZ=Europe/Moscow \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "fetch_data.py"]