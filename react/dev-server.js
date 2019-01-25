const webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const chalk = require('chalk');
const path = require('path');
const devConfig = require('./webpack.dev');

const HOST = '127.0.0.1';
const PORT = 3000;

const options = {
    host: HOST,
    port: PORT
};

WebpackDevServer.addDevServerEntrypoints(devConfig, options);
const compiler = webpack(devConfig);
const server = new WebpackDevServer(compiler, options);

server.listen(PORT, HOST, function (err) {
  if (err) {
    return console.log(err);
  }
  console.log(chalk.blue(`Listening at http://${HOST}:${PORT}/`));
});