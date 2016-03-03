/* global __dirname */
var config = require('./webpack.config.js');
var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var webpack = require('webpack');


// Remove webpack-dev-server
config.debug = false;
config.devtool = 'source-map';
config.entry = {
  main: './js/main',
  styles: './scss/main.scss',
};
config.module.loaders = [
  {
    test: /\.jsx?$/,
    exclude: /node_modules/,
    loaders: [
      'babel?presets[]=es2015,cacheDirectory=' + encodeURIComponent(path.resolve(__dirname, 'tmp')),
    ],
  },
  {
    test: /\.css$/,
    loader: ExtractTextPlugin.extract('style', 'css'),
  },
  {
    test: /\.scss$/,
    loader: ExtractTextPlugin.extract('style', 'css!postcss!sass'),
  },
  {
    test: /\.less/,
    loader: ExtractTextPlugin.extract('style', 'css!less?relative-urls'),
  },
  {
    test: /\.(png|woff|svg|eot|ttf)$/,
    loader: 'url-loader?limit=20000',
  },
];
config.output = {
  path: path.resolve('./assets/dist/'),
  publicPath: '/static/app/dist/',
  filename: '[name]-[hash].js',
};

config.plugins = [
  new BundleTracker({filename: './tmp/webpack-stats-prod.json'}),
  new ExtractTextPlugin('[name]-[hash].css', {allChunks: true}),
  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production'),
    },
  }),

  // keeps hashes consistent between compilations
  new webpack.optimize.OccurenceOrderPlugin(),

  // minifies your code
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false,
    },
  }),
];

module.exports = config;
