'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..', 'extension');
let install;
const sandbox = { module: { exports: {} }, require: name => name === 'vortex-api' ? {}
  : name === './config.json' ? JSON.parse(fs.readFileSync(path.join(root, 'config.json'), 'utf8')) : require(name) };
vm.runInNewContext(fs.readFileSync(path.join(root, 'index.js'), 'utf8'), sandbox);
sandbox.module.exports.default({ registerGame: () => {}, registerInstaller: (id, priority, supported, fn) => { install = fn; } });
install(JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))).then(result => {
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}).catch(error => {
  console.error(`error: archive validation ${process.argv[2]}: ${error.message}`);
  process.exitCode = 1;
});
