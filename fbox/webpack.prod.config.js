var config = require('./webpack.config.js');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require("extract-text-webpack-plugin");

var path = require('path');
var webpack = require('webpack');

config.entry.main = './js/main';

config.output.path = require('path').resolve('./assets/dist/');
config.output.publicPath = '/static/dist/';

config.plugins = [
  new BundleTracker({filename: './server/webpack-stats-prod.json'}),
  new ExtractTextPlugin("[name]-[hash].css", {allChunks: true}),
  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
    }}),

  // keeps hashes consistent between compilations
  new webpack.optimize.OccurenceOrderPlugin(),

  // minifies your code
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  })
];
config.debug = false;

module.exports = config;
