FROM python:3.9-slim
RUN apt-get update && apt-get install -y iputils-ping
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
