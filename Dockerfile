FROM python:3.14-slim

WORKDIR /app

COPY modern_pygame/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY modern_pygame /app/modern_pygame

WORKDIR /app/modern_pygame
EXPOSE 8000

CMD ["uvicorn", "api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
