FROM python:3.11.4-slim-bookworm

ENV PYTHONUNBUFFERED=1

LABEL org.opencontainers.image.source=https://github.com/jheidecker/lemmony
LABEL org.opencontainers.image.description="Lemmony"
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app
RUN pip3 install build
COPY . .
RUN python3 -m build
RUN pip3 install dist/lemmony-0.0.5-py3-none-any.whl

CMD ["lemmony-cli"]