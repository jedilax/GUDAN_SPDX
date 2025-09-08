FROM python:3.9-slim

WORKDIR /app

# copy your code
COPY app.py /app

# install Flask + MySQL connector
RUN pip install --no-cache-dir flask mysql-connector-python

EXPOSE 5000

CMD ["python", "app.py"]
