FROM python:3.11

RUN pip install --no-cache-dir poetry==1.2.2

WORKDIR /app

COPY poetry.lock ./
COPY pyproject.toml ./

RUN poetry export > /tmp/requirements.txt && \
	pip install --no-cache-dir -r /tmp/requirements.txt

COPY wait_and_load/ ./wait_and_load/

ENTRYPOINT [ "python" ]
CMD [ "-m", "wait_and_load" ]
