FROM thomasve/fastapi-cookiecutter-base:3.10

WORKDIR src
COPY src/ .
COPY pyproject.toml ./stub.toml

RUN poetry install

EXPOSE 7070
RUN pip install uvicorn
