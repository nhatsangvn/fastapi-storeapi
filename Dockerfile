FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN  pip install --no-cache-dir -r /app/requirements.txt

COPY ./storeapi/ /app/storeapi
COPY ./.env /app/

CMD ["uvicorn", "storeapi.main:app", "--host", "0.0.0.0", "--port", "80"]
