<template>
    <app-fragment className="report-wrapper">
        <p class="md-title section-title">Speed reports</p>
        <md-list>
            <md-list-item
                v-for="report in reportTitles"
                :key="report"
                v-on:md-expanded="onReportExpand(report)"
                class="api-card"
                md-expand
            >
                <div class="report-card-title">Report #{{ report }}</div>

                <md-list slot="md-expand">
                    <md-list v-if="reportDetailsMap[report]">
                        <md-list-item
                            class="md-inset"
                            v-for="handler in reportDetailsMap[report]"
                            :key="handler.path"
                            md-expand
                        >
                            <div class="report-card-title">{{ handler.path }}</div>
                            <md-list slot="md-expand">
                                <md-list-item
                                    v-for="mark in handler.percentiles"
                                    :key="mark.name"
                                >{{ mark.name }} {{ mark.value }}</md-list-item>
                            </md-list>
                        </md-list-item>
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
        margin-left: 20px;

        font-size: 20px;
    }
</style>
