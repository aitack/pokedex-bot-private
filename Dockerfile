FROM python:3.12@sha256:17b9724493d916f56565c131f389faff2597f46dec6ce09516f95125bc9f519f
WORKDIR /bot
COPY requirements.txt /bot/
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.txt \
    && useradd --create-home --shell /usr/sbin/nologin bot
COPY --chown=bot:bot . /bot
USER bot
CMD ["python", "main.py"]
