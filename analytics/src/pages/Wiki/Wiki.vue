<template>
    <app-fragment className="report-wrapper">
        <p class="md-title section-title">Handlers info</p>
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
    </app-fragment>
</template>

<script>
    export default {
        name: 'Wiki',

        created() {
            this.fetchEndpoints();
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
        },

        data: () => ({
            handlers: [],
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

    .api-card-url {
        font-size: 20px;
    }

    .api-card_method_get .md-list-item-text.api-card-method {
        background-color: var(--md-theme-default-primary);
    }

    .api-card_method_post .md-list-item-text.api-card-method {
        background-color: var(--md-theme-default-accent);
    }
</style>
