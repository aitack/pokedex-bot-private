FROM python:3.15@sha256:f17ec845ebdd4f3347431579e1c22eaeec82913f039f2a54b937c7ff870bacdb
WORKDIR /bot
COPY requirements.txt /bot/
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.txt \
    && useradd --create-home --shell /usr/sbin/nologin bot
COPY --chown=bot:bot . /bot
USER bot
CMD ["python", "main.py"]
