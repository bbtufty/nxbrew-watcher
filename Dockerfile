FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install -e .

ENV CONFIG_DIR=/config
ENV DOCKER_ENV=true

ENTRYPOINT ["python", "nxbrew_watcher.py"]
