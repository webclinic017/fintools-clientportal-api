var base = location.href.substring(0, location.href.lastIndexOf("/"));

// Menu
items = [
  'index',
  'chart-test',
  'demo',
  'scanner'
];
var d = document;
var menu = d.getElementById('menu');
var ul = d.createElement('ul')
for (i in items) {
  var li = d.createElement('li');
  var a = d.createElement('a');
  a.href = items[i] + ".html";
  a.innerHTML = items[i];
  li.appendChild(a);
  ul.appendChild(li);
}
menu.appendChild(ul);
