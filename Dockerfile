FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY pyproject.toml poetry.lock ${LAMBDA_TASK_ROOT}/

RUN pip install --upgrade pip && pip install poetry

RUN poetry install -vvv

COPY . ${LAMBDA_TASK_ROOT}/

ENV PYTHONPATH=${LAMBDA_TASK_ROOT}/source

RUN poetry run python source/manage.py collectstatic --noinput

CMD ["app.lambda_handler"]
