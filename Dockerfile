FROM python:3.10.12

WORKDIR "/home/bavanmendon/Documents/Anhalt/Distributed Software Architecture/Practicals/dsa-project"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
