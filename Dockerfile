FROM python:3.10-slim-bullseye
WORKDIR /src
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry==1.3.0
COPY pyproject.toml poetry.lock /src/
RUN poetry config virtualenvs.create false
RUN poetry install --only main -n --no-root --no-dev

COPY . /src/

EXPOSE 8080
CMD ["python", "-m", "app"]
