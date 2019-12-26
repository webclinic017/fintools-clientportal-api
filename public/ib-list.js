// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = 'http://localhost:8080/';
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

function getConid(ticker) {
  var url = kUrlIb + 'lseconid/' + ticker;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  });
}

function setCounter(value) {
  var tickerCountDiv = document.getElementById('count');
  tickerCountDiv.innerHTML = 'Count (found): ' + value;
}

// - get conids from list
// - get snapshots
// - draw tables
function drawList() {
    ticker = document.getElementById('ticker').value;
    var list = document.getElementById('list');
    var tickerCount = 0;
    setCounter(tickerCount);
    list.innerHTML = '';
    if (ticker != '') {
      var tickerCountTotal = document.getElementById('total');
      tickers = ticker.split(' ');
      tickerCountTotal.innerHTML = 'Count (total): ' + tickers.length;
      tickers.forEach((ticker) => {
        // Populate table (async)
        getConid(ticker)
          .then((tickerInfo) => {
            console.log('conid', tickerInfo);
            list.innerHTML = list.innerHTML + ' '
              + tickerInfo.ticker.toUpperCase();
            setCounter(++tickerCount);
          }).catch((err) => {
            console.log('Could not get conid:', ticker.toUpperCase());
          }); //getChart
      }) // foreach ticker
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
      drawList();
    }
  }
});
