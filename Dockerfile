FROM python:3.15@sha256:df3f05ff4d74833f52146edd195c8f7913581b57796a820fb7e373457ace9bad
WORKDIR /bot
COPY requirements.txt /bot/
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.txt \
    && useradd --create-home --shell /usr/sbin/nologin bot
COPY --chown=bot:bot . /bot
USER bot
CMD ["python", "main.py"]
