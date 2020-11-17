// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = '/';
var kUrlFilings = 'https://finapi.tk/filings/';
var kPlotNames = [];
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
        var r = req.responseText;
        try {
          resolve(JSON.parse(r));
        } catch(err) {
          reject('Invalid JSON payload: ' + r);
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
  var url = kUrlIb + 'chart/' + ticker + '/' + time;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve(res); })
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

function drawPlot(timeRange) {
    console.log('Drawing', timeRange);
    ticker = document.getElementById('ticker').value;
    var root = document.getElementById('plot');
    root.innerHTML = '';
    if (ticker != '') {
      tickers = ticker.split(' ');
      for (let i = 0; i < tickers.length; ++i) {
        // Pre-add charts and labels
        var container = document.createElement('div'),
            label = document.createElement('label');
        var labelStr = tickers[i].toUpperCase();
        container.id = labelStr;
        label.innerHTML = labelStr;
        container.appendChild(label);
        root.appendChild(container);
      }
      // Draw actual charts asynchronously
      tickers.forEach((ticker) => {
        getChart(ticker, timeRange)
          .then((d) => {
            console.log(d);
            // Canvas
            var div = document.getElementById(d.ticker.toUpperCase());
            var c = document.createElement('canvas');
            c.id = 'canvas';
            c.style = 'width:100%; height:50%; display: block;';
            c.width = 800;
            c.height = 400;
            div.appendChild(c);

            if (c.getContext) {
              var p = new Plot(c.getContext('2d'));
              p.setLabels(['o', 'h', 'l', 'c']);
              p.setData(d.data);
              getFilings(d.ticker).then((filings) => {
                console.log(filings);
                var d = [];
                for (var i in filings.data) {
                  d.push({
                    "date": new Date(filings.data[i].date)
                    .toISOString().slice(0, 10),
                    "label": filings.data[i].value,
                  });
                }
                p.setLines(d);
                p.draw();
              });
              p.draw();
            } else {
              throw 'Could not find canvas';
            }
          }).catch((err) => {
            console.log('Could not get chart:', err);
          }); //getChart
      })
      // FOREACH TICK
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
