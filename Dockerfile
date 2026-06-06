FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api ./api
COPY angrybirds ./angrybirds
COPY levels ./levels
COPY pygame_main.py .

EXPOSE 8000

CMD ["uvicorn", "api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
