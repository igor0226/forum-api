<template>
    <header>
        <md-toolbar class="md-primary">
            <h1 class="md-title">Backend analytics</h1>
            <md-tabs class="md-primary" md-sync-route>
                <md-tab md-label="Wiki" id="tab-wiki" to="/" exact></md-tab>
                <md-tab md-label="Reports" id="tab-reports" to="/reports" exact></md-tab>
                <md-tab md-label="Monitoring" id="tab-monitoring" to="/monitoring" exact></md-tab>
                <md-tab md-label="Change log" id="tab-change-log" to="/versions" exact></md-tab>
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
