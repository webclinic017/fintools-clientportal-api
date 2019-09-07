var express = require('express');
var app = express();
var path = require('path');
var port = 8080;


// Serve rest from 'public' dir
app.use(express.static('public'))

app.get('/chartDemo/:ticker/:time', (req,res) => {
  var ticker = req.params.ticker,
      time = req.params.time;
  var k = 0;
  switch (time) {
    case '1d':
      k = 1;
      break;
    case '1m':
      k = 2;
      break;
    case '3m':
      k = 3;
      break;
    default:
      console.log('Invalid time: ', time);
      res.status(400).json({ error: 'Invalid time ',time });
  }
  var c = [
    {
      "date": "2019-04-23",
      "open": k*1.52,
      "close": k*1.73,
      "high": k*2,
      "low": k*1.47,
      "volume": 175201,
      "label": "Apr 23, 19",
    },
    {
      "date": "2019-04-24",
      "open": k*1.52,
      "close": k*1.73,
      "high": k*k,
      "low": k*1.47,
      "volume": 584261,
      "label": "Apr 24, 19",
    },
    {
      "date": "2019-04-24",
      "open": 1.52,
      "close": 1.73,
      "high": k,
      "low": 0.1,
      "volume": 584261,
      "label": "Apr 24, 19",
    }
  ];

  res.send(c);
});

console.log('Listening on port', port);
app.listen(8080);
