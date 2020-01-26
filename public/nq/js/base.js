var base = location.href.substring(0, location.href.lastIndexOf("/"));

// Menu
items = {
  nasdaq: [
    [ 'nq-chart-for-ticker', 'NASDAQ: Chart for ticker' ],
    [ 'chart-day',           'NASDAQ: Chart for ticker (day)' ],
    [ 'chart-test',          'a' ],
    [ 'chart-list',          'NASDAQ: Chart list for given tickers' ],
    [ 'conid',               'a' ],
    [ 'demo',                'a' ],
    [ 'list-fluctuate-day',  'NASDAQ: Fluctuate for tickers' ],
    [ 'scanner-nasdaq',      'NASDAQ: Scanner top gainers' ]
  ],
};
var d = document;
var menu = d.getElementById('menu');
Array('nasdaq').forEach((exch) => {
  var div = d.createElement('div')
  div.style = 'display: inline-block;';
  var h3 = d.createElement('h3')
  h3.innerHTML = exch.toUpperCase();
  div.appendChild(h3);
  menu.appendChild(div);
  var ul = d.createElement('ul')
  for (i in items[exch]) {
    var li = d.createElement('li');
    var a = d.createElement('a');
    var item = items[exch][i];
    a.href = item[0] + ".html";
    a.innerHTML = item[0] + ': ' + item[1];
    li.appendChild(a);
    ul.appendChild(li);
  }
  div.appendChild(ul);
  menu.appendChild(div);
})

window.addEventListener('load', function() {
  if (typeof main === 'function') {
    main();
  }
});


// Methods
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
