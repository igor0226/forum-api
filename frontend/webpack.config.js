const { VueLoaderPlugin } = require('vue-loader');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const autoprefixer = require('autoprefixer');
const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: './app.js',
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
                test: /\.css$/,
                use: [
                    // { loader: MiniCssExtractPlugin.loader },
                    { loader: 'style-loader' },
                    { loader: 'css-loader' },
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: () => [autoprefixer()],
                            },
                        },
                    },
                ],
            },
        ],
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                DEPLOY: `"${process.env.DEPLOY}"`,
            },
        }),
        new MiniCssExtractPlugin(),
        new VueLoaderPlugin(),
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, 'index.html'),
            favicon: './assets/favicon.ico',
        }),
        new CopyPlugin({
            patterns: [
                { from: '*', to: '', context: 'assets' },
            ],
        }),
    ],
    resolve: {
        alias: {
            vue$: 'vue/dist/vue.runtime.esm.js',
        },
        extensions: ['*', '.js', '.vue', '.json'],
    },
    devServer: {
        port: 8080,
        historyApiFallback: true,
        static: {
            directory: path.join(__dirname, 'assets'),
        },
    },
};