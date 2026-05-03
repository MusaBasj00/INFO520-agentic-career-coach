FROM python:3.11-slim

WORKDIR /app

COPY mcp-server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp-server/app ./app
COPY data ./data

ENV PORT=8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
