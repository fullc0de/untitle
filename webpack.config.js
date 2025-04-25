const path = require('path');

module.exports = {
  entry: './app/static/components/index.jsx',
  output: {
    path: path.resolve(__dirname, 'app/static/dist'),
    filename: 'bundle.js',
    publicPath: '/static/'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react']
          }
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  devServer: {
    host: '0.0.0.0',
    port: 3000,
    hot: true,
    watchFiles: ['app/static/components/**/*.jsx'],
    devMiddleware: {
      publicPath: '/static/dist/'
    },
    static: {
      directory: path.join(__dirname, 'app/static')
    },
    headers: {
      'Access-Control-Allow-Origin': '*'
    }
  }
}; 