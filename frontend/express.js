const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const httpProxy = createProxyMiddleware({
    target: 'http://sa-backend-lb:5000',
});

const wsProxy = createProxyMiddleware({
    target: 'http://sa-backend-lb:5000',
    changeOrigin: true,
});

const app = express();

app.use('/analytics/endpoints', httpProxy);
app.use('/analytics/*/details', httpProxy);
app.use('/analytics/reports', httpProxy);
app.use('/monitoring', wsProxy);
app.use(express.static(`${__dirname}/dist`));

const server = app.listen(80);
server.on('upgrade', wsProxy.upgrade);
