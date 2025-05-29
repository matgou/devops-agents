
# In kubernetes_admin/Dockerfile
FROM python:3.13-slim
WORKDIR /app

RUN pip install poetry
ENV PORT=8080
RUN apt update && apt install -y kubernetes-client/stable prometheus/stable && apt clean
COPY . .

RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

USER myuser
RUN poetry install

ENV PATH="/home/myuser/.local/bin:$PATH"
CMD poetry run uvicorn main:app --host 0.0.0.0 --port $PORT
