FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv venv /opt/venv
ENV \
    UV_PROJECT_ENVIRONMENT="/opt/venv" \
    PATH="/opt/venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.12
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --home /home/appuser appuser
RUN uv venv /opt/venv && \
    chown -R appuser:appgroup /opt/venv
WORKDIR /webapp
RUN chown -R appuser:appgroup /webapp
COPY pyproject.toml /webapp
RUN chmod 644 /webapp/pyproject.toml
USER appuser
RUN uv lock
USER root
RUN --mount=type=cache,target=/home/appuser/.cache/uv \
    chown -R appuser:appgroup /home/appuser/.cache/uv
USER appuser
RUN --mount=type=cache,target=/home/appuser/.cache/uv \
    uv sync --frozen --no-install-project
COPY app /webapp/app
USER root
RUN chmod -R 755 /webapp/app
USER appuser
EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--no-access-log", "--log-level", "info"]
