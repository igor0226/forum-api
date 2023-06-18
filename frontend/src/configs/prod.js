export default {
    ENDPOINTS_URL: () => '/analytics/endpoints',
    WS_MONITORING_URL: () => `wss://${window.location.host}/analytics/monitoring`,
    REPORTS_URL: () => '/analytics/reports',
    ONE_REPORT_URL: reportName => `/analytics/${reportName}/details`,
};
