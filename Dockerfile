FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.5.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 3000

CMD ["python", "app/main.py"]
