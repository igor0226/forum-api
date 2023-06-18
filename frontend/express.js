const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const httpProxy = createProxyMiddleware({
    target: 'http://sa-backend-lb:5000',
});
const wsProxy = createProxyMiddleware({
    target: 'http://sa-backend-lb:5000',
    changeOrigin: true,
});
const staticHandler = express.static(`${__dirname}/dist`);

const app = express();

app.use('/analytics/endpoints', httpProxy);
app.use('/analytics/*/details', httpProxy);
app.use('/analytics/reports', httpProxy);
app.use('/analytics/monitoring', wsProxy);

app.use('/', staticHandler);
app.use('/reports', staticHandler);
app.use('/monitoring', staticHandler);
app.use('/versions', staticHandler);
app.use('/_healthz', (req, res) => {
    res.status(200).send({ message: 'i am alive' });
});

const server = app.listen(80);
server.on('upgrade', wsProxy.upgrade);
