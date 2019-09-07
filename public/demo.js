// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = 'http://localhost:8080/';
var kUrlFilings = 'https://finapi.tk/filings/';
var kPlotNames = [];
var kPlot = null;
var kTime = '3m';

// CORS Request
function createRequest(method, url) {
  var req = new XMLHttpRequest();
  return new Promise((resolve, reject) => {
    req.onreadystatechange = function() {
      //authReceived = true;
      if (req.readyState == 4) {
      } else {
        return;
      }
      if (req.status >= 200 && req.status < 300) {
        try {
          resolve(JSON.parse(req.responseText));
        } catch(error) {
          reject('Invalid JSON payload');
        }
      } else {
        reject({
          status: req.status,
          statusText: req.statusText
        });
      }
    };
    req.open(method, url);
    req.send();
  });
};


/* GETTERS */
function getChart(ticker, time) {
  if(time == '')
    throw 'Time is not set';
  var url = kUrlIb + 'chartDemo/' + ticker + '/' + time;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve({ "ticker": ticker, "data": res }); })
      .catch((err) => { reject(err); });
  });
}


function getFilings(symbol) {
  // Output: JSON { symbol, data }
  if(symbol == '') throw 'Symbol is not set';
  return new Promise((resolve, reject) => {
    createRequest('GET', kUrlFilings + symbol)
      .then((r) => {
        // Repad data
        d = [];
        for(var i = 0; i < r.length; i++) {
          d[i] = {
            date: Date.parse(r[i].date),
            value: r[i].type
          };
        }
        if(debug) console.log({symbol: symbol, data: d});
        resolve({ symbol: symbol, data: d });
      }).catch((err) => { reject(err); });
  });
}


function getWinners() {
  console.log("Get winners");
  return new Promise((resolve, reject) => {
    createRequest('GET', kUrlIb)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  })
};

function drawPlot(timeRange) {
    ticker = document.getElementById('ticker').value;
    if (ticker != '') {
      getChart(ticker, timeRange)
        .then((d) => {
          var c = document.getElementById('canvas');
          if (c.getContext) {
            var p = new Plot(c.getContext('2d'));
            p.setData(d.data);
            //getFilings(d.ticker).then((filings) => {
            //  var plot = kPlots[filings.symbol];
            //  var d = [];
            //  for (var i in filings.data) {
            //    d.push({
            //      "date": new Date(filings.data[i].date)
            //      .toISOString().slice(0, 10),
            //      "label": filings.data[i].value,
            //    });
            //  }
            //  plot.setLines(d);
            //  plot.draw();
            //});
            p.draw();
          } else {
            throw 'Could not find canvas';
          }
        // then
      }); //getChart
    } else {
      alert('Set the ticker');
    }
}


// MAIN
var tickerField = document.getElementById('ticker');
tickerField.focus();
tickerField.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) { // Enter
    event.preventDefault();
    kTicker = document.getElementById('ticker').value;
    if (kTicker == '') {
      alert('Set the ticker');
    } else {
      drawPlot(kTime);
    }
  }
});

var kPlot = document.getElementById('plot');
// Canvas
var canvas = document.createElement('canvas');
canvas.id = 'canvas';
canvas.style = 'width:100%; height:50%; display: block;';
canvas.width = 800;
canvas.height = 400;
kPlot.appendChild(canvas);
