
FROM python:3.12.4-alpine AS builder

WORKDIR /app

COPY Pipfile Pipfile.lock ./
# COPY requirements.txt ./

RUN apk update && \
    apk add musl-dev mariadb-dev libffi-dev gcc && \
    pip install pipenv && \
    pipenv requirements > requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt



FROM python:3.12.4-alpine AS main

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERD 1

WORKDIR /usr/src/app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
COPY . .

RUN pip install --no-cache /wheels/* && \
    adduser --disabled-password appuser

USER appuser


ENTRYPOINT ["sh", "entrypoint.sh"]

