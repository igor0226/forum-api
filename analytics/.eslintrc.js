// eslint-disable-next-line
module.exports = {
    'env': {
        'browser': true,
        'node': true,
        'es2021': true,
    },
    'extends': [
        'eslint:recommended',
        'plugin:vue/essential',
        'plugin:@typescript-eslint/recommended',
    ],
    'parserOptions': {
        'ecmaVersion': 'latest',
        'parser': '@typescript-eslint/parser',
        'sourceType': 'module',
    },
    'plugins': [
        'vue',
        '@typescript-eslint',
    ],
    'rules': {
        '@typescript-eslint/no-var-requires': 'off',
        'quotes': ['error', 'single'],
    },
};
