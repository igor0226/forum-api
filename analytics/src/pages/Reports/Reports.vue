<template>
    <md-list>
        <md-list-item
            :class="cn(handler.method)"
            md-expand
            v-for="handler in handlers"
            :key="handler.url"
        >
            <div class="md-list-item-text api-card-method">{{ handler.method }}</div>
            <div class="md-list-item-text api-card-url">{{ handler.path }}</div>

            <md-list slot="md-expand">
                <md-list-item class="md-inset">World</md-list-item>
                <md-list-item class="md-inset">Europe</md-list-item>
                <md-list-item class="md-inset">South America</md-list-item>
            </md-list>
        </md-list-item>
    </md-list>
</template>

<script>
    export default {
        name: 'Reports',
        created() {
            fetch('http://localhost:5000/analytics/endpoints', {
                headers: { 'content-type': 'application/json' },
            })
                .then(response => response.json())
                .then(endpoints => {
                    this.handlers = endpoints;
                });
        },
        methods: {
            cn: method => `api-card api-card_method_${method.toLowerCase()}`,
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

    .api-card_method_get .md-list-item-text.api-card-method {
        background-color: var(--md-theme-default-primary);
    }

    .api-card_method_post .md-list-item-text.api-card-method {
        background-color: var(--md-theme-default-accent);
    }

    .api-card-url {
        font-size: 20px;
    }
</style>
