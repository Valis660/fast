FROM python:3.11.9

WORKDIR /app

COPY req.txt req.txt
RUN pip install -r req.txt

COPY . .

#CMD ["python", "src/main.py"]
CMD alembic upgrade head; python src/main.py