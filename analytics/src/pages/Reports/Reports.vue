<template>
    <md-list>
        <md-list-item class="api-card api-card_method_get" md-expand>
          <div class="md-list-item-text api-card-method">GET</div>
          <div class="md-list-item-text api-card-url">/user/profile</div>

          <md-list slot="md-expand">
            <md-list-item class="md-inset">World</md-list-item>
            <md-list-item class="md-inset">Europe</md-list-item>
            <md-list-item class="md-inset">South America</md-list-item>
          </md-list>
        </md-list-item>

        <md-list-item class="api-card api-card_method_post" md-expand>
          <span class="md-list-item-text api-card-method">POST</span>
          <span class="md-list-item-text api-card-url">/user/edit</span>

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
