FROM python:3.11.9

WORKDIR /app

COPY req.txt req.txt
RUN pip install -r req.txt

COPY . .

# Production entrypoint: run migrations then start uvicorn on 0.0.0.0:8000
CMD bash -lc "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"