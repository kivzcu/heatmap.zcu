const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = [
{
    entry: {
        index: './public/js/index.js',
        polyfills: './public/js/polyfills.js',
    },
    optimization: {
        minimize: true
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'public/js'),
        library: 'js'
    },
},
{
    plugins: [new MiniCssExtractPlugin()],
    entry: {
        style: './public/css/style.scss'
    },
    optimization: {
        minimize: true
    },
    output: {
        publicPath: '',
        path: path.resolve(__dirname, 'public/css')
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    { loader: 'style-loader' },
                    { loader: MiniCssExtractPlugin.loader },
                    { loader: 'css-loader' },
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: [
                                    [
                                        "autoprefixer"
                                    ],
                                ],
                            },
                        },
                    },
                    {
                        loader: 'sass-loader'
                    }
                ]
            },
            {
                test: /\.(png|jp(e*)g|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'img/'
                        }
                    }
                ]
            },
        ]
    }
}
]