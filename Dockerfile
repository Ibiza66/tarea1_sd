FROM python:3.12-slim

WORKDIR /app

COPY response_generator/requirements.txt ./response_generator/requirements.txt
RUN pip install --no-cache-dir -r response_generator/requirements.txt

COPY response_generator ./response_generator
COPY data ./data

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "response_generator.app.main:app", "--host", "0.0.0.0", "--port", "8001"]