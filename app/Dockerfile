#FROM docker.arvancloud.ir/python:3.11-slim
#
#WORKDIR /app
#
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY main.py .
#
#CMD ["python", "main.py"]



FROM docker.arvancloud.ir/python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM docker.arvancloud.ir/python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

COPY --from=builder /root/.local /root/.local

COPY main.py .

CMD ["python", "main.py"]

