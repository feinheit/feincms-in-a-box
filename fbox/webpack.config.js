var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var BundleTracker = require('webpack-bundle-tracker');
var _target = process.env.NODE_ENV === 'production' ? 'dist' : 'build';
var autoprefixer = require('autoprefixer');
var node_modules_dir = path.join(__dirname, 'node_modules');


var config = {
  context: path.join(__dirname, 'assets'),
  entry: {
    main: [ 'webpack-dev-server/client?http://localhost:3000',
            'webpack/hot/only-dev-server',
            './js/main'],
    styles: ['./scss/app.scss', './scss/select.less'],
    editor: './scss/editor.scss'
  },
  output: {
    path: path.resolve('./assets/build/'),
    publicPath: 'http://localhost:3000/assets/build/',
    filename: '[name]-[hash].js'
  },
  devtool: 'source-map',
  module: {
    loaders: [
      // Transform JSX in .jsx files
      { test: /\.jsx?$/, exclude: /node_modules/, loaders: ['react-hot', 'babel']},
        // Extract css files
      {
        test: /\.css$/,
          loader: ExtractTextPlugin.extract("style-loader!css-loader")
      },
      // Optionally extract less files
      // or any other compile-to-css language
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract(
            "css?sourceMap!postcss-loader!sass?outputStyle=expanded&sourceMap=true&includePaths[]="
            + encodeURIComponent(path.resolve(node_modules_dir, 'zurb-foundation-5/scss')))
      },
      {
        test: /\.less/,
        loader: ExtractTextPlugin.extract("style-loader", "css-loader!less-loader?relative-urls")
      },
      { test: /\.(png|woff|svg|eot|ttf)$/, loader: "url-loader?limit=20000" }
    ],
    noParse: []
  },
  postcss: [ autoprefixer({ browsers: ['last 2 versions'] }) ],
  resolve: {
    // Allow require('./blah') to require blah.jsx
    extensions: ['', '.js', '.jsx'],
    modulesDirectories: ['assets/js',
                       'assets/scss',
                       'assets/img',
                       'node_modules'],
    alias: {}
  },
  // Use the plugin to specify the resulting filename (and add needed behavior to the compiler)
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(), // don't reload if there is an error
    new BundleTracker({filename: './webpack-stats.json'}),
    new ExtractTextPlugin("[name].css", {allChunks: true})
  ],
  debug: true,
  // dev server not working yet. Have to not extract css during development.
  devServer: {
    contentBase: path.join(__dirname, 'app', 'static', 'app', 'build'),
    inline: true,
    colors: true,
    quiet: false
  }

};


module.exports = config;
