<template>
    <header>
        <md-toolbar class="md-primary">
            <h1 class="md-title">Backend analytics</h1>
            <md-tabs class="md-primary">
                <md-tab md-label="Reports"></md-tab>
                <md-tab md-label="Monitoring"></md-tab>
                <md-tab md-label="Change log"></md-tab>
            </md-tabs>
        </md-toolbar>
    </header>
</template>

<script>
    export default {
        name: 'Header',
    };
</script>

<style>
    header .md-toolbar .md-title {
        font-size: 26px;
        font-weight: bold;
    }

    header .md-toolbar .md-button-content {
        font-size: 16px;
    }
</style>
