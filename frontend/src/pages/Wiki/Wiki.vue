<template>
    <app-fragment className="page-wrapper">
        <p class="md-title section-title">Handlers info</p>
        <md-list>
            <api-card
                v-for="handler in handlers"
                :key="handler.url"
                :method="handler.method"
            >
                <template v-slot:content>
                    <div class="md-list-item-text api-card-url">{{ handler.path }}</div>
                </template>
                <template v-slot:expand>
                    <md-list>
                        <md-list-item class="md-inset">{{ handler.description }}</md-list-item>
                    </md-list>
                </template>
            </api-card>
        </md-list>
    </app-fragment>
</template>

<script>
    import config from '../../configs';

    export default {
        name: 'Wiki',

        created() {
            this.fetchEndpoints();
        },

        methods: {
            fetchEndpoints() {
                fetch(config.ENDPOINTS_URL())
                    .then(response => response.json())
                    .then(endpoints => {
                        this.handlers = endpoints;
                    });
            },
        },

        data: () => ({
            handlers: [],
        }),
    };
</script>
