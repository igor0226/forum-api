FROM python:3.8.15-alpine3.15

RUN adduser -D worker
USER worker
WORKDIR /home/worker

RUN mkdir backend
COPY --chown=worker:worker . backend

RUN cd backend && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt && \
    mkdir log && mkdir log/rps && touch log/rps/rps.json

ENV PATH="/home/worker/backend/venv/bin:$PATH"
ENV DEPLOY="local-kuber"

CMD ["python", "backend/app.py", "--log-performance=True"]

EXPOSE 5000:5000
