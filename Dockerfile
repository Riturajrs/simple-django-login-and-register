FROM python:3.12

ENV IS_PRODUCTION True

WORKDIR /crypto

COPY pyproject.toml poetry.lock /crypto/

RUN pip install --upgrade pip && pip install poetry

RUN poetry install -vvv

COPY . /crypto/

ENV PYTHONPATH=/crypto/source

RUN poetry run python source/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]