<template>
    <app-fragment className="page-wrapper">
        <p class="md-title section-title">Traffic monitoring</p>
    </app-fragment>
</template>

<script>
    export default {
        name: 'Monitoring',

        created() {
            const socket = new WebSocket('ws://localhost:5000/monitoring');

            // Соединение открыто
            socket.addEventListener('open', event => {
                socket.send('Igor!');
            });

            // Наблюдает за сообщениями
            socket.addEventListener('message', event => {
                console.log('Message from server ', event.data);
            });
        },
    };
</script>

<style>
</style>
