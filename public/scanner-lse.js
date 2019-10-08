// Load API token
var debug = true;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlIb = 'http://localhost:8080/';
var perc = 10;
var price = 1;

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
function getData() {
  var url = kUrlIb + 'winners/UK/' + perc + '/' + price;
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

// MAIN
getData()
  .then((d) => {
    var table = document.getElementById('table');
    table.innerHTML = '';
    // Draw table
    var table = document.getElementById('table');
    var t = document.createElement('table');
    t.setAttribute('border', true);
    for (let i = 0; i < d.length; ++i) {
      var tr = document.createElement('tr'),
          symbol = document.createElement('td'),
          name = document.createElement('td');
      symbol.innerHTML = d[i].symbol;
      name.innerHTML = d[i].company_name;
      tr.appendChild(symbol);
      tr.appendChild(name);
      t.appendChild(tr);
    }
    table.appendChild(t);

  }).catch((err) => {
    console.log('Could not get chart:', err);
  }); //getChart
