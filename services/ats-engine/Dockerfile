FROM python:3.11-slim
WORKDIR /app
COPY services/ats-engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY packages/scoring /packages/scoring
ENV PYTHONPATH=/packages/scoring
COPY services/ats-engine/app ./app
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
