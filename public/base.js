var base = location.href.substring(0, location.href.lastIndexOf("/"));

// Menu
items = {
  nasdaq: [
    [ 'index',          'NASDAQ: Chart for ticker' ],
    [ 'chart-test',     'a' ],
    [ 'chart-list',     'NASDAQ: Chart list for given tickers' ],
    [ 'conid',          'a' ],
    [ 'demo',           'a' ],
    [ 'scanner-nasdaq', 'NASDAQ: Scanner top gainers' ]
  ],
  lse: [
    [ 'list-ib',        'LSE: Filter out tickers not in IB' ],
    [ 'list-lse-chart', 'LSE: Chart list for given tickers' ],
    [ 'list-perc',      'LSE: List ticker info' ],
    [ 'lse-chart',      'LSE: Chart for ticker' ],
    [ 'scanner-lse',    'LSE: Scanner top gainers' ]
  ]
};
var d = document;
var menu = d.getElementById('menu');
Array('lse', 'nasdaq').forEach((exch) => {
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
