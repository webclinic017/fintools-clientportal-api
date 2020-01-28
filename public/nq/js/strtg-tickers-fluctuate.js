// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlIb = 'http://localhost:8080/';
var missedTickers = [];
var tickerCount = 0;

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

function calFluctuations(data, low, high) {
  // Return: countFlux
  var findLow = true;
  var countFlux = 0;
  for(var i = 0; i < data.length; i++) {
    var dPoint = data[i];
    if (findLow) {
      if (dPoint.l <= low) findLow = false;
    } else {
      if (dPoint.h >= high) {
        findLow = true;
        countFlux++;
      }
    }
  }
  return countFlux;
}

//function round(value, decimals) {
//  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
//}

function round(num, dec) {
  if ((typeof num !== 'number') || (typeof dec !== 'number')) 
    return false; 
  var num_sign = num >= 0 ? 1 : -1;
  return (Math.round((num*Math.pow(10,dec))+(num_sign*0.0001))/Math.pow(10,dec)).toFixed(dec);
}

/* GETTERS */
function getChart(ticker) {
  var url = kUrlIb + 'chart-two-day/' + ticker;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  });
}

function addRow(table, data) {
  // data = [ ticker, avg, entry, exit, c1, c2 ]
  var table = document.getElementById(table);
  var tr = document.createElement('tr');
  // Populate
  for (let i = 0; i < data.length; ++i) {
    var td = document.createElement('td');
    var label = data[i];
    if (i != 0) td.setAttribute('align', 'right');
    td.innerHTML = data[i];
    tr.appendChild(td);
  }
  table.appendChild(tr);
}

function arrayRemove(arr, value) {
  return arr.filter(function(el){
    return el != value;
  });
}

function parseData(ticker, d) {
  // return: [ ticker, avg, entry, exit, countF1, countF2 ]
  var data = {};
  var current = 0;
  var currentDay = 0;
  var days = [];
  var reset = false;
  for(var i = 0; i < d.length; i++) {
    // Split into data[0] data[1]
    var t = new Date(d[i].t);
    var day = t.getDate();
    if (i == 0) {
      currentDay = day;
      reset = true;
    }
    if (currentDay != day) {
      current++;
      reset = true;
    }
    if (reset) {
      currentDay = day;
      days.push(day);
      data[current] = {};
      data[current].data = [];
      data[current].day = day;
      data[current].averages = [];
      reset = false;
    }
    data[current].data.push(d[i]);
    data[current].averages.push((d[i].h + d[i].l)/2);
  }
  // Get averages
  var j = 0;
  for(var i = 0; i < data[0].averages.length; i++) {
    j += data[0].averages[i];
  }
  var avg = j/data[0].averages.length;
  var entry = avg*(100/102);
  var exit = avg*(104/100);

  // Count changes
  var tName = '';
  if (data[1] == null) {
    f1 = 0;
    console.log('Missing day 2 data for', ticker);
  } else {
    f1 = calFluctuations(data[1].data, entry, exit);
  }
  return [
    ticker.toUpperCase(),
    round(avg, 2),
    round(entry, 2),
    round(exit, 2),
    calFluctuations(data[0].data, entry, exit),
    f1
  ];
}

function getTicker(ticker) {
  getChart(ticker)
  .then((d) => {
    // [ ticker, avg, entry, exit, countF0, countF1 ]
    var data = parseData(d.ticker, d.data);
    if (data[4] > 0 && data[5] > 0) {
      tName = 't-success';
    } else if (data[4] > 0 && data[5] == 0) {
      tName = 't-fail';
    } else {
      tName = 't-other';
    }
    addRow(tName, data);
    missedTickers = arrayRemove(missedTickers, d.ticker);
    setCounter('found', ++tickerCount);
  }).catch((err) => {
    console.log('Could not get chart:', err);
  }) //getChart
}

function setCounter(type, value) {
  var div = document.getElementById('count-' + type);
  div.innerHTML = 'Count ' + type + ': ' + value;
}

function drawTables() {
    // TABLE
    ticker = document.getElementById('ticker').value;
    // TICKERS
    if (ticker != '') {
      tickers = ticker.split(' ');
      setCounter('total', tickers.length);
      missedTickers = tickers;
      tickers.forEach(ticker => getTicker(ticker));
      // FOREACH TICKER
      console.log('Print missedTickers for errors');
    } else {
      // No ticker
      alert('Set the ticker');
    }
}

function main() {
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
}
