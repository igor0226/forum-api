<template>
    <app-fragment className="report-wrapper">
        <p class="md-title section-title">Handlers</p>
        <md-list>
            <md-list-item
                v-for="handler in handlers"
                :key="handler.url"
                :class="cn(handler.method)"
                md-expand
            >
                <div class="md-list-item-text api-card-method">{{ handler.method }}</div>
                <div class="md-list-item-text api-card-url">{{ handler.path }}</div>

                <md-list slot="md-expand">
                    <md-list-item class="md-inset">{{ handler.description }}</md-list-item>
                </md-list>
            </md-list-item>
        </md-list>
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
            this.fetchEndpoints();
            this.fetchReportTitles();
        },

        methods: {
            cn: method => `api-card api-card_method_${method.toLowerCase()}`,

            fetchEndpoints() {
                fetch('http://localhost:5000/analytics/endpoints')
                    .then(response => response.json())
                    .then(endpoints => {
                        this.handlers = endpoints;
                    });
            },

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
                        console.log(details);
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
            handlers: [],
            reportTitles: [],
            reportDetailsMap: {},
        }),
    };
</script>

<style>
    .md-list-item-text.api-card-method {
        max-width: 80px;
        margin: 0 20px;
        padding: 4px 16px;

        border-radius: 8px;

        color: #fff;
        font-weight: bold;

        flex: none;
    }

    .api-card_method_get .md-list-item-text.api-card-method {
        background-color: var(--md-theme-default-primary);
    }

    .api-card_method_post .md-list-item-text.api-card-method {
        background-color: var(--md-theme-default-accent);
    }

    .api-card-url {
        font-size: 20px;
    }

    .md-title.section-title {
        margin: 36px;

        font-size: 24px;
    }

    .report-card-title {
        margin-left: 20px;

        font-size: 20px;
    }
</style>
