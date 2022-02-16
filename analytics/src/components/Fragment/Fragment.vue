<template>
    <div :class="className">
        <slot></slot>
    </div>
</template>

<script>
    export default {
        name: 'Fragment',

        props: {
            className: {
                type: String,
                default: '',
            }
        }
    };
</script>
