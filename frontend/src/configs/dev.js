export default {
    ENDPOINTS_URL: () => 'http://127.0.0.1:5000/analytics/endpoints',
    WS_MONITORING_URL: () => 'ws://127.0.0.1:5000/monitoring',
    REPORTS_URL: () => 'http://127.0.0.1:5000/analytics/reports',
    ONE_REPORT_URL: reportName => `http://127.0.0.1:5000/analytics/${reportName}/details`,
};
