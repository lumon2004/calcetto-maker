FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN cp giocatoriCalcetto.example.json giocatoriCalcetto.json || true

CMD ["python", "main.py"]