var express = require('express');
var app = express();
var https = require('https');
var path = require('path');
var port = 8080;
var iburl = 'localhost';
var ibport = 5000;
var debug = true;

// Convert object to url query string
// Example: { one: two, three: four }
// converts to ?one=two&three=four
function urlparams(data) {
  var i = 0,
      encoded = '?'
  Object.keys(data).forEach((key) => {
    if (i > 0) encoded += '&';
    encoded += key + '=' + data[key];
    i++;
  });
  return encoded;
}

// CORS Request
function ibRequest(method, path, body = null, detail = null) {
  return new Promise((resolve, reject) => {
    var options = {
      hostname: iburl,
      port: ibport,
      path: path,
      method: method,
      headers: {
        'Accept': '*/*',
        'User-Agent': 'curl/7.52.1'
      }
    }
    if (body != null) {
      if (method == 'POST') {
        body = JSON.stringify(body);
        options.data = body;
        options.headers['Content-Type'] = 'application/json';
        options.headers['Content-Length'] = body.length;
      } else if (method == 'GET') {
        // Request is GET, so params are urlencoded
        options.path = path + urlparams(body);
      } else {
        console.log("ERROR, we shouldn't be here");
      }
    }
    process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
    console.log(method, options.path);
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
            resolve({ data: JSON.parse(data), detail: detail });
          }
        } catch(error) {
          reject('Invalid JSON: ' + error + ': ' + data);
        }
      });
    }).on("error", (err) => {
      console.log("Error: " + err.message);
      reject('Error: ' + err);
    });
    if (body != null && method == 'POST') {
      rq.write(body);
    }
    rq.end();
  });
};


///////////////////// ENDPOINTS ///////////////////////
// Serve rest from 'public' dir
app.use(express.static('public'))

app.get('/chart/:ticker/:time', (req,res) => {
  // TODO
  var ticker = req.params.ticker,
      time = req.params.time;
  // Get ticker conid
  ibRequest('POST', '/v1/portal/iserver/secdef/search', { symbol: ticker })
    .then((r) => {
      var s = r.data.filter(i => i.description == 'NASDAQ');
      var conid = s[0].conid;
      // Get OHLC data
      ibRequest('GET', '/v1/portal/iserver/marketdata/history',
            { conid: conid, period: time }, conid)
        .then((s) => {
          console.log('data', s.data);
          console.log('detail', s.detail);
          res.send(s.data.data);
        })
  }).catch((err) => {
      res.status(400).json({ error: err });
      console.log('ERROR: ' + err);
  }) //ibRequest
});

app.get('/winners/:perc/:price', (req,res) => {
  // TODO
  var perc = req.params.perc,
      price = req.params.price;
  // Get scanner results
  ibRequest('POST', '/v1/portal/iserver/scanner/run', {
    type: "TOP_PERC_GAIN",
    instrument: "STK",
    filter: [
      {
        code: "priceBelow",
        value: parseInt(price)
      }
    ],
    location: "STK.US.MAJOR",
    size: "10"
  }).then((r) => {
    debug = true;
    if (debug) { console.log('body', r); }
    var ret = [];
    var r = r.data.contracts;
    for (let i = 0; i < r.length; ++i) {
      ret.push({
        symbol: r[i].symbol,
        con_id: r[i].con_id,
        company_name: r[i].company_name
      })
    }
    res.setHeader('Content-Type', 'application/json');
    res.send(ret);
  }).catch((err) => {
      res.status(400).json({ error: err });
      console.log('ERROR: ' + err);
  }) //ibRequest
});

app.get('/chartDemo/:ticker/:time', (req,res) => {
  var ticker = req.params.ticker,
      time = req.params.time;
  var k = 0;
  switch (time) {
    case '1d': k = 1; break;
    case '1m': k = 2; break;
    case '3m': k = 3; break;
    default:
      console.log('Invalid time: ', time);
      res.status(400).json({ error: 'Invalid time ',time });
  }
  var c = [
    { "date": "2019-04-23", "open": k*1.52, "close": k*1.73, "high": k*2, "low": k*1.47, "volume": 175201, "label": "Apr 23, 19", },
    { "date": "2019-04-24", "open": k*1.52, "close": k*1.73, "high": k*k, "low": k*1.47, "volume": 584261, "label": "Apr 24, 19", },
    { "date": "2019-04-24", "open": 1.52, "close": 1.73, "high": k, "low": 0.1, "volume": 584261, "label": "Apr 24, 19", }
  ];
  res.send(c);
});

app.post('/get', (req, res) => {
  console.log('AAAAA'+req.body);
});

console.log('Listening on port', port);
app.listen(8080);
