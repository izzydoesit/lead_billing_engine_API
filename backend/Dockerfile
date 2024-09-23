FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app
COPY gunicorn.conf.py .

EXPOSE 8080
# Run the FastAPI application with gunicorn
CMD ["gunicorn","-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-c", "gunicorn.conf.py"]
