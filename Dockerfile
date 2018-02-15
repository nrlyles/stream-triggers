FROM python:2.7

COPY dist/stream_trigger*tar.gz /
RUN pip install stream_trigger*tar.gz


CMD ["python", "-m", "stream_trigger.stream_trigger"]

