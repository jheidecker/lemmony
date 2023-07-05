FROM python:3.11.4-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN pip3 install build
COPY . .
RUN python3 -m build
RUN pip3 install dist/*.whl

CMD ["lemmony-cli"]