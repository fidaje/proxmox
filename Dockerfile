FROM python:3.10-slim

WORKDIR /app

RUN useradd -m bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R bot:bot /app
USER bot

CMD ["python", "main.py"]