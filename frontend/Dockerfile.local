FROM node:16.13.2-alpine

RUN adduser -D worker
USER worker

WORKDIR /home/worker

RUN mkdir frontend
COPY --chown=worker:worker . frontend

WORKDIR /home/worker/frontend

RUN npm ci && npm run build

CMD ["npm", "start"]

EXPOSE 80:80
