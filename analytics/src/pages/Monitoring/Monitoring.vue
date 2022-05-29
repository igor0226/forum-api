<template>
    <app-fragment className="page-wrapper">
        <p class="md-title section-title">Traffic monitoring</p>
        <apexchart
            width="100%"
            height="500px"
            type="line"
            :options="options"
            :series="series"
        ></apexchart>
    </app-fragment>
</template>

<script>
    export default {
        name: 'Monitoring',

        created() {
            const socket = new WebSocket('ws://localhost:5000/monitoring');

            socket.addEventListener('message', ({ data }) => {
                if (data && data.indexOf('[') === 0) {
                    const rpsList = JSON.parse(data);
                    this.series = this.makeChartSeries(rpsList);
                    this.options = this.makeChartOptions(this.options, rpsList);
                } else {
                    this.updateChartSeries(data);
                    this.updateChartOptions();
                }
            });

            socket.addEventListener('open', () => {
                socket.send('INIT');
            });
        },

        methods: {
            updateChartSeries(rps) {
                this.series = this.makeChartSeries([...this.series[0].data, Number(rps)]);
            },

            makeChartSeries(rpsList) {
                return [{
                    name: 'rps',
                    data: rpsList,
                }];
            },

            updateChartOptions() {
                const date = new Date(Date.now());
                const timestamp = `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;

                this.options = {
                    ...this.options,
                    xaxis: {
                        timestamps: [...this.options.xaxis.timestamps, timestamp],
                    },
                };
            },

            makeChartOptions(options, rpsList) {
                const baseDate = Date.now();
                const rpsListLen = rpsList.length;

                return {
                    ...options,
                    xaxis: {
                        timestamps: rpsList.map((_, i) => {
                            const date = new Date(baseDate - rpsListLen + i);
                            return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
                        }),
                    },
                };
            },
        },

        data() {
            return {
                options: {
                    chart: {
                        id: 'vuechart-example',
                    },
                    xaxis: {
                        timestamps: [],
                    },
                },
                series: [{
                    name: 'rps',
                    data: [],
                }],
            };
        },
    };
</script>

<style>
</style>
