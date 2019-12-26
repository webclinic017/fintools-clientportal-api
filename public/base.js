var base = location.href.substring(0, location.href.lastIndexOf("/"));

// Menu
items = [
  [ 'index',          'NASDAQ: Chart for ticker' ],
  [ 'chart-test',     'a' ],
  [ 'chart-list',     'NASDAQ: Chart list for given tickers' ],
  [ 'conid',          'a' ],
  [ 'demo',           'a' ],
  [ 'perc-list',      'LSE: List ticker info' ],
  [ 'scanner-lse',    'LSE: Scanner top gainers' ],
  [ 'ib-list',        'LSE: Filter out tickers not in IB' ],
  [ 'lse-chart-list', 'LSE: Chart list for given tickers' ],
  [ 'lse-chart',      'LSE: Chart for ticker' ],
  [ 'scanner-nasdaq', 'NASDAQ: Scanner top gainers' ]
];
var d = document;
var menu = d.getElementById('menu');
var ul = d.createElement('ul')
for (i in items) {
  var li = d.createElement('li');
  var a = d.createElement('a');
  a.href = items[i][0] + ".html";
  a.innerHTML = items[i][0] + ': ' + items[i][1];
  li.appendChild(a);
  ul.appendChild(li);
}
menu.appendChild(ul);
