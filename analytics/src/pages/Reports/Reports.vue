<template>
    <app-fragment className="page-wrapper">
        <p class="md-title section-title">Speed reports</p>
        <md-list>
            <md-list-item
                v-for="report in reportTitles"
                :key="report"
                v-on:md-expanded="onReportExpand(report)"
                class="api-card"
                md-expand
            >
                <div class="report-card-title">
                    <md-icon class="report-card-icon" md-src="/report.svg"></md-icon>
                    <div class="reports-card-text">Report #{{ report }}</div>
                </div>

                <md-list slot="md-expand">
                    <md-list v-if="reportDetailsMap[report]">
                        <api-card
                            v-for="handler in reportDetailsMap[report]"
                            className="md-inset"
                            :key="handler.key"
                            :method="handler.method"
                        >
                            <template v-slot:content>
                                <div
                                    class="md-list-item-text report-card-title"
                                >{{ handler.path }}</div>
                            </template>
                            <template v-slot:expand>
                                <md-list>
                                    <md-list-item
                                        class="reports-card-mark"
                                        v-for="mark in handler.percentiles"
                                        :key="mark.name"
                                    >{{ mark.name }} {{ mark.value }}</md-list-item>
                                </md-list>
                            </template>
                        </api-card>
                    </md-list>

                    <md-list-item
                        class="md-inset"
                        v-else
                    >Loading...</md-list-item>
                </md-list>
            </md-list-item>
        </md-list>
    </app-fragment>
</template>

<script>
    export default {
        name: 'Reports',

        created() {
            this.fetchReportTitles();
        },

        methods: {
            fetchReportTitles() {
                fetch('http://localhost:5000/analytics/reports')
                    .then(response => response.json())
                    .then(reportTitles => {
                        this.reportTitles = reportTitles;
                    });
            },

            fetchReportDetails(reportName) {
                fetch(`http://localhost:5000/analytics/${reportName}/details`)
                    .then(response => response.json())
                    .then(details => {
                        this.reportDetailsMap = {
                            ...this.reportDetailsMap,
                            [reportName]: details,
                        };
                    });
            },

            onReportExpand(reportName) {
                if (this.reportDetailsMap[reportName]) {
                    return;
                }

                this.fetchReportDetails(reportName);
            },

            getReportDetails(reportName) {
                const report = this.reportDetailsMap[reportName];

                return { report, fetched: Boolean(report) };
            },
        },

        data: () => ({
            reportTitles: [],
            reportDetailsMap: {},
        }),
    };
</script>

<style>
    .report-card-title {
        height: 24px;
        margin-left: 20px;

        font-size: 20px;
    }

    .md-icon.report-card-icon {
        display: inline-block;
    }

    .reports-card-text {
        display: inline-block;

        height: 24px;
        margin-left: 12px;
    }

    .reports-card-mark {
        padding-left: 48px;
    }
</style>
