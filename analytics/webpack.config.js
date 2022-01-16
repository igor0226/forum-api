const { VueLoaderPlugin } = require('vue-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const htmlWebpackPlugin = require('html-webpack-plugin');
const autoprefixer = require('autoprefixer');
const path = require('path');

module.exports = {
    entry: 'index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                },
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.(eot|ttf|woff|woff2)(\?\S*)?$/,
                loader: 'file-loader',
                options: {
                    name: '[name][contenthash:8].[ext]',
                },
            },
            {
                test: /\.(png|jpe?g|gif|webm|mp4|svg)$/,
                loader: 'file-loader',
                options: {
                    outputPath: 'assets',
                    esModule: false,
                },
            },
            {
                test: /\.s?css$/,
                use: [
                    'style-loader',
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: () => [autoprefixer()],
                        },
                    },
                ],
            },
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new htmlWebpackPlugin({
            template: path.resolve(__dirname, 'public', 'index.html'),
            favicon: './assets/favicon.ico',
          }),
    ],
    resolve: {
        alias: {
            vue$: 'vue/dist/vue.runtime.esm.js',
        },
        extensions: ['*', '.js', '.vue', '.json'],
    }
};