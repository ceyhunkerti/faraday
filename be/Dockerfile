ARG PYTHON_IMAGE=3.10

FROM python:${PYTHON_IMAGE}

RUN pip install --upgrade pip
RUN mkdir -p /workspace/app
RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /workspace

COPY pyproject.toml pdm.lock README.md run.sh ./
COPY ./app /workspace/app
RUN chmod +x run.sh

RUN pdm install --prod --no-lock --no-editable
ENV PATH="$PATH:/workspace/.venv/bin"
