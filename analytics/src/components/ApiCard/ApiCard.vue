<template>
    <md-list-item
        :class="this.fullClassName"
        md-expand
    >
        <div
            class="md-list-item-text api-card-method"
        >{{ method }}</div>
        <slot name="content"></slot>
        <slot slot="md-expand" name="expand"></slot>
    </md-list-item>
</template>

<script>
    export default {
        name: 'ApiCard',

        props: {
            method: {
                type: String,
                default: 'GET',
            },

            className: {
                type: String,
                default: '',
            },
        },

        data() {
            return {
                fullClassName: this.cn(),
            };
        },

        methods: {
            cn() {
                const mod = this.method.toLowerCase();
                return `api-card api-card_method_${mod} ${this.className}`;
            },
        },
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
        background-color: #1976d2;
    }

    .api-card_method_post .md-list-item-text.api-card-method {
        background-color: #00b8d4;
    }
</style>
