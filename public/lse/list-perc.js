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

function getSnapshot(conid) {
  var url = kUrlIb + 'snapshot-single/' + conid;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  });
}

// - get conids from list
// - get snapshots
// - draw tables
function drawTables() {
    console.log('Drawing');
    ticker = document.getElementById('ticker').value;
    var table = document.getElementById('table');
    table.border = true;
    table.innerHTML = '';
    var header = document.createElement('thead'),
      headers = [
        { label: 'ticker', field: 'ticker' },
        { label: 'Last Price', field: 31 },
        { label: 'Change Percent', field: 83 },
        { label: 'Open Price', field: 7295 },
        { label: 'Close Price', field: 7296 },
      ],
      row = document.createElement('tr');
    for (let i = 0; i < headers.length; ++i) {
      var th = document.createElement('th');
      th.innerHTML = headers[i].label;
      row.appendChild(th);
      table.appendChild(row);
    }
    if (ticker != '') {
      tickers = ticker.split(' ');
      for (let i = 0; i < tickers.length; ++i) {
        // Pre-add tickers
        var tr = document.createElement('tr'),
            td = document.createElement('td');
        var labelStr = tickers[i].toUpperCase();
        tr.id = labelStr;
        td.innerHTML = labelStr;
        tr.appendChild(td);
        table.appendChild(tr);
      }
      tickers.forEach((ticker) => {
        // Populate table (async)
        getConid(ticker)
          .then((d) => {
            console.log(d);
            getSnapshot(d.conid)
            .then((data) => {
              var d = data;
              console.log(d);
              var tr = document.getElementById(d['55'].toUpperCase());
              for (let i = 1; i < headers.length; ++i) {
                var td = document.createElement('td');
                td.innerHTML = d[headers[i].field];
                tr.appendChild(td);
              }
            }).catch((err) => {
              console.log('Could not get snapshot:', err);
            }); // getSnapshot
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
      drawTables();
    }
  }
});
