FROM python:3.10.12

WORKDIR "/grpc-app"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 50051
CMD ["python", "server.py"]
