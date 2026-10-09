FROM debian:bookworm-slim@sha256:7c7b2c966bc9ee8cedfeef67e0e279108992c77681fa595db4a9d65c06ccc587
RUN useradd --uid 1000 --create-home tester \
    && mkdir /home/tester/.codex \
    && chown tester:tester /home/tester/.codex
USER root
RUN apt-get update && apt-get install -y --no-install-recommends bubblewrap && rm -rf /var/lib/apt/lists/*
USER tester
WORKDIR /home/tester
