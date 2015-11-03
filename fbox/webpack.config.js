/* global __dirname */
var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var BundleTracker = require('webpack-bundle-tracker');
var autoprefixer = require('autoprefixer');
var nodeModulesDir = path.join(__dirname, 'node_modules');

var host = 'localhost';

var config = {
  context: path.join(__dirname, 'assets'),
  entry: {
    main: [
      'webpack-dev-server/client?http://' + host + ':3000',
      'webpack/hot/only-dev-server',
      './js/main',
    ],
    styles: [
      './scss/main.scss',
    ],
  },
  output: {
    path: path.resolve('./assets/build/'),
    publicPath: 'http://' + host + ':3000/assets/build/',
    filename: '[name]-[hash].js',
  },
  devtool: 'source-map',
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loaders: [
          'react-hot',
          'babel?cacheDirectory=' + encodeURIComponent(path.resolve(__dirname, 'tmp')),
        ],
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader'),
      },
      // Optionally extract less files
      // or any other compile-to-css language
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract(
          'css?sourceMap!postcss-loader!sass?outputStyle=expanded&sourceMap=true&includePaths[]='
          + encodeURIComponent(path.resolve(nodeModulesDir))),
      },
      {
        test: /\.less/,
        loader: ExtractTextPlugin.extract(
          'style-loader',
          'css-loader!less-loader?relative-urls'),
      },
      {
        test: /\.(png|woff|svg|eot|ttf)$/,
        loader: 'url-loader?limit=20000',
      },
    ],
    noParse: [],
  },
  postcss: [
    autoprefixer({
      browsers: ['last 2 versions'],
    }),
  ],
  resolve: {
    // Allow require('./blah') to require blah.jsx
    extensions: ['', '.js', '.jsx'],
    modulesDirectories: [
      'assets/js',
      'assets/scss',
      'assets/img',
      'node_modules',
    ],
    alias: {},
  },
  // Use the plugin to specify the resulting filename (and add needed behavior to the compiler)
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(), // don't reload if there is an error
    new BundleTracker({filename: './webpack-stats.json'}),
    new ExtractTextPlugin('[name].css', {allChunks: true}),
  ],
  debug: true,
  // dev server not working yet. Have to not extract css during development.
  devServer: {
    contentBase: path.join(__dirname, 'app', 'static', 'app', 'build'),
    inline: true,
    colors: true,
    quiet: false,
  },
};

module.exports = config;
