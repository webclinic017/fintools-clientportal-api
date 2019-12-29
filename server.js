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

function getChart(ticker, time, exchange) {
  return new Promise((resolve, reject) => {
    // Get ticker conid
    ibRequest('POST', '/v1/portal/iserver/secdef/search', { symbol: ticker })
      .then((r) => {
        var s = r.data.filter(i => i.description == exchange);
        var conid = s[0].conid;
        // Get OHLC data
        ibRequest('GET', '/v1/portal/iserver/marketdata/history',
              { conid: conid, period: time, bar: '1h' }, conid)
          .then((s) => {
            console.log('data', s.data);
            console.log('detail', s.detail);
            resolve({
              data: s.data.data,
              high: s.data.high,
              low: s.data.low,
              ticker: s.data.symbol,
              text: s.data.text
            });
          })
    }).catch((err) => {
      reject({ error: err });
      console.log('ERROR: ' + err);
    }) //ibRequest
  }) // Promise
}

///////////////////// ENDPOINTS ///////////////////////
// Serve rest from 'public' dir
app.use(express.static('public'))

app.get('/snapshot/:tickers', (req,res) => {
  // tickers = list of conids, coma separated
  // Need to call this twice
  var tickers = req.params.tickers;
  var url = '/v1/portal/iserver/marketdata/snapshot'
    + '?conids=' + tickers + '&fields=83';
  ibRequest('GET', url)
  .then((r) => {
    ibRequest('GET', url)
    .then((s) => {
      debug = true;
      if (debug) console.log(s);
      if (s.data.error != null) throw s.data.error;
      var ret = [];
      var s = s.data;
      for (let i = 0; i < s.length; ++i) {
        ret.push({
          symbol: s[i][55],
          con_id: s[i].conid,
          price_ClosePrevious: s[i][7296],
          price_AfterHours: s[i][31],
          priceChangeAfterHours: s[i][82],
          priceChangePerc: s[i][83],
        })
      }
      res.setHeader('Content-Type', 'application/json');
      res.send(ret);
    })
  }).catch((err) => {
      res.status(400).json({ error: err });
      console.log('ERROR: ' + err);
  }) //ibRequest
});

app.get('/snapshot-single/:ticker', (req,res) => {
  // ticker = a single ticker, conid, e.g. 12345
  // Need to call this twice
  var tickers = req.params.ticker;
  var url = '/v1/portal/iserver/marketdata/snapshot'
    + '?conids=' + tickers + '&fields=83';
  ibRequest('GET', url)
  .then((r) => {
    ibRequest('GET', url)
    .then((s) => {
      debug = true;
      if (debug) console.log(s);
      if (s.data.error != null) throw s.data.error;
      var ret = s.data[0];
      res.setHeader('Content-Type', 'application/json');
      res.send(ret);
    })
  }).catch((err) => {
      res.status(400).json({ error: err });
      console.log('ERROR: ' + err);
  }) //ibRequest
});

app.get('/conid/:ticker', (req,res) => {
  var ticker = req.params.ticker;
  ibRequest('POST', '/v1/portal/iserver/secdef/search', { symbol: ticker })
    .then((r) => {
      var s = r.data.filter(i => i.description == 'NASDAQ');
      res.send({
        conid: s[0].conid,
      });
    })
    .catch((err) => {
      console.log('ERROR:', err);
      res.status(500).json(err);
    })
})

app.get('/lseconid/:ticker', (req,res) => {
  var ticker = req.params.ticker;
  ibRequest('POST', '/v1/portal/iserver/secdef/search', { symbol: ticker })
    .then((r) => {
      var s = r.data.filter(i => i.description == 'LSE');
      console.log('Filtered: ', s);
      if (!s.length) {
        console.log('Could not find ticker');
        res.status(404).send();
        return;
      }
      console.log(s[0]);
      res.send({
        conid: s[0].conid,
        ticker: ticker
      });
    })
    .catch((err) => {
      console.log('ERROR:', err);
      res.status(500).json(err);
    })
})

app.get('/chart/:ticker/:time', (req,res) => {
  var ticker = req.params.ticker,
      time = req.params.time;
  getChart(ticker, time, 'NASDAQ')
    .then((chart) => { res.send(chart); })
    .catch((err) => { res.status(400).json({ error: err }); })
});

app.get('/lsechart/:ticker/:time', (req,res) => {
  // TODO
  var ticker = req.params.ticker,
      time = req.params.time;
  getChart(ticker, time, 'LSE')
    .then((chart) => { res.send(chart); })
    .catch((err) => { res.status(400).json({ error: err }); })
});

app.get('/winners/:loc/:perc/:price', (req,res) => {
  // loc = US or EU
  var loc = req.params.loc,
      perc = req.params.perc,
      price = req.params.price;
  // Get scanner results
  if (loc == 'US') {
    var instrument = 'STK',
        ibLocation = 'STK.US.MAJOR';
  } else if (loc == 'UK') {
    var instrument = 'STOCK.EU',
        ibLocation = 'STK.EU.LSE';
  } else {
    throw 'Unknown location';
  }
  ibRequest('POST', '/v1/portal/iserver/scanner/run', {
    type: "TOP_PERC_GAIN",
    instrument: instrument,
    filter: [
      {
        code: "changePercAbove",
        value: parseInt(perc),
      },
      {
        code: "priceBelow",
        value: parseInt(price),
      },
    ],
    location: ibLocation,
    size: "10"
  }).then((r) => {
    debug = true;
    console.log(r);
    if (r.data.error != null) throw r.data.error;
    var ret = [];
    var r = r.data.contracts;
    for (let i = 0; i < r.length; ++i) {
      if (debug) { console.log('item', r[i]); }
      ret.push({
        symbol: r[i].symbol,
        con_id: r[i].con_id,
        company_name: r[i].company_name
      })
    }
    res.setHeader('Content-Type', 'application/json');
    res.send(ret);
  }).catch((err) => {
      res.status(500).json({ error: err });
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
