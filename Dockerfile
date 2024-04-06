FROM python:3.10.2-slim

WORKDIR /app

RUN pip install poetry
# copy all files
COPY . .

RUN poetry install

EXPOSE 80

CMD ["poetry", "run", "python", "ice_breaker/app.py"]
