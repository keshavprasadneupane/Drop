FROM ghcr.io/astral-sh/uv:latest AS uv_bin
FROM python:3.12-slim
COPY --from=uv_bin /uv /uvx /bin/

ENV UV_LINK_MODE=copy
# Tell uv to put the container environment completely outside of /app
ENV UV_PROJECT_ENVIRONMENT=/pyenv

WORKDIR /app

COPY uv.lock pyproject.toml /app/

RUN uv sync --frozen --no-install-project

COPY . .

RUN uv sync --frozen

RUN chmod +x run.sh
EXPOSE 8000
CMD ["./run.sh"]