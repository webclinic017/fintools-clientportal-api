// Load API token
var debug = true;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlIb = 'http://localhost:8080/';
var perc = 10;
var price = 2;

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

function getSnapshots(conids) {
  var url = kUrlIb + 'snapshot/' + conids;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  });
}

// MAIN
getData()
  .then((d) => {
    if (debug) console.log(d);
    var conids = [];
    // Draw list
    var list = document.getElementById('list');
    for (let i = 0; i < d.length; ++i) {
      list.innerHTML += d[i].symbol + ' ';
    }
    // Draw table
    var table = document.getElementById('table');
    table.innerHTML = '';
    var t = document.createElement('table');
    t.setAttribute('border', true);
    var thead = document.createElement('thead');
    thead.innerHTML = ''
      + '<tr>'
      + '  <th>Symbol</th>'
      + '  <th>Name</th>'
      + '  <th>prev close</th>'
      + '  <th>price</th>'
      + '  <th>change</th>'
      + '  <th>change (%)</th>'
      + '</tr>';
    t.appendChild(thead);
    for (let i = 0; i < d.length; ++i) {
      conids.push(d[i].con_id);
      var tr = document.createElement('tr'),
          symbol = document.createElement('td'),
          name = document.createElement('td');
      tr.id = d[i].symbol;
      symbol.innerHTML = d[i].symbol;
      name.innerHTML = d[i].company_name;
      tr.appendChild(symbol);
      tr.appendChild(name);
      t.appendChild(tr);
    }
    table.appendChild(t);
    // Get percentages
    console.log(conids);
    conids_list = conids.join(',');
    console.log(conids_list);
    getSnapshots(conids_list)
      .then((d) => {
        console.log(d);
        d.forEach((i) => {
          // Cells
          var tr = document.getElementById(i.symbol);
          td = document.createElement('td');
          td.innerHTML = i.price_ClosePrevious;
          tr.appendChild(td);
          td = document.createElement('td');
          td.innerHTML = i.price_AfterHours;
          tr.appendChild(td);
          td = document.createElement('td');
          td.innerHTML = i.priceChangeAfterHours;
          tr.appendChild(td);
          td = document.createElement('td');
          td.innerHTML = i.priceChangePerc;
          tr.appendChild(td);
        })
    }) //getSnapshots
  }).catch((err) => {
    console.log('Could not get chart:', err);
  }); //getChart
