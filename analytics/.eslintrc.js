module.exports = {
    env: {
        browser: true,
        node: true,
        es6: true,
        commonjs: true,
    },
    extends: [
        'airbnb',
        'plugin:vue/base',
    ],
    parserOptions: {
        parser: require('babel-eslint'),
        ecmaVersion: 6,
    },
    plugins: [
        'html',
    ],
    rules: {
        quotes: ['error', 'single'],
        indent: ['error', 4],
        'global-require': 'off',
        'vue/script-indent': ['error', 4, {
            baseIndent: 1,
        }],
        'arrow-parens': ['error', 'as-needed'],
    },
    overrides: [{
        files: ['*.vue'],
        rules: {
            indent: 'off',
        },
    }],
};
