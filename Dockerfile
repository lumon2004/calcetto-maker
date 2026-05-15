FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN cp players.example.json players.json || true

CMD ["python", "main.py"]