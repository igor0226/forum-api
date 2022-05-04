# Modern python backend

## Technologies:
1) aiohttp
2) asyncpg
3) PostgreSql
4) jinja2

## Launch

1) Build docker image
```shell
./scripts/build_docker.sh
```
2) Launch it
```shell
./scripts/run_docker.sh
```
3) Launch python server
```shell
python app.py
```

## Analytics tools
Simple Vue.js frontend project.
It can be used for performance reports reviewing

Launch:
```shell
cd analytics
npm i
npm run dev
```