// Minimal example to pull data from IB beta client API
var express = require('express');
var app = express();
var https = require('https');
var path = require('path');
var port = 8080;
var iburl = 'localhost';
var ibport = 5000;

// CORS Request
function ibRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: iburl,
      port: ibport,
      path: path,
      headers: { 'Accept': '*/*', 'User-Agent': 'curl/7.52.1' },
      method: method
    }
    process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
    var rq = https.request(options, (rs) => {
      let data = '';
      rs.on('data', (chunk) => {
        data += chunk;
      });
      rs.on('end', () => {
        try {
          if (data == '') {
            reject('No data received');
          } else {
            resolve(JSON.parse(data));
          }
        } catch(error) {
          reject('Invalid JSON: ' + error + ': ' + data);
        }
      });
    }).on("error", (err) => {
      console.log("Error: " + err.message);
      reject('Error: ' + err);
    });
    rq.end();
  });
};

ibRequest('GET', '/v1/portal/iserver/auth/status')
  .then((r) => {
    console.log('aa');
    console.log(r);
  }).catch((err) => {
    console.log('ERROR: ' + err);
  }) //ibRequest
