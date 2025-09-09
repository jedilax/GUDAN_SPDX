FROM python:3.11-slim
WORKDIR /app

COPY require.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r require.txt

COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
