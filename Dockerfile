FROM python:3.10.12

ENV POETRY_CACHE_DIR=/opt/.cache
ENV    POETRY_HOME=/opt/poetry
ENV    POETRY_VENV=/opt/poetry-venv

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python3 -m venv $POETRY_VENV && $POETRY_VENV/bin/pip install poetry==1.8.3

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry check && poetry config virtualenvs.create false && poetry install --no-interaction --no-dev

COPY . /app
RUN mv /app/src/* /app






