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
                    this.makeChartSeries(rpsList);
                } else {
                    this.updateChartSeries(data);
                }
            });

            socket.addEventListener('open', () => {
                socket.send('INIT');
            });
        },

        methods: {
            getTime(baseDate, secOffset) {
                return new Date(baseDate + secOffset * 1000);
            },

            updateChartSeries(newRps) {
                const newPoint = { x: this.getTime(Date.now(), 0), y: Number(newRps) };
                const newData = [...this.series[0].data, newPoint].slice(-50);

                this.series = [{
                    name: 'rps',
                    data: newData,
                }];
            },

            makeChartSeries(rpsList) {
                const baseDate = Date.now();
                const rpsListLen = rpsList.length;

                this.series = [{
                    name: 'rps',
                    data: rpsList.map((rps, i) => {
                        const date = this.getTime(baseDate, i - rpsListLen);
                        return {
                            x: date.getTime(),
                            y: rps,
                        };
                    }),
                }];
            },
        },

        data() {
            return {
                options: {
                    chart: {
                        id: 'vuechart-example',
                        type: 'line',
                    },
                    xaxis: {
                        type: 'datetime',
                        labels: {
                            datetimeUTC: false,
                        },
                    },
                    tooltip: {
                        x: {
                            format: 'dd.MM.yyyy HH:mm:ss',
                        },
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
