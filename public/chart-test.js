// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = 'http://localhost:8080/';
var kUrlFilings = 'https://finapi.tk/filings/';
var kPlotNames = [];
var kPlot = null;

// CORS Request
function createRequest(method, url, data = null) {
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
    if (data != null) {
      req.send(JSON.stringify(data));
    } else {
      req.send()
    }
  });
};


/* GETTERS */
function getUrl(url) {
  // A wrapper. It makes a POST to server, and server
  // makes the actual GET
  // workaround for CORS (unsafe)
  return new Promise((resolve, reject) => {
    createRequest('POST', '/get', url)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  });
}

// MAIN
var canvas = document.createElement('canvas');
canvas.id = 'canvas';
canvas.style = 'width:100%; height:50%; display: block;';
canvas.width = 800;
canvas.height = 400;

var kPlot = document.getElementById('plot');
kPlot.appendChild(canvas);
var kTime = '3m';
var url = "https://localhost:5000/v1/portal/iserver/marketdata/history?conid=265598&period=1w";
getUrl(url)
  .then((d) => {
    console.log(d);
    var c = document.getElementById('canvas');
    if (c.getContext) {
      var p = new Plot(c.getContext('2d'));
      p.setLabels(['o', 'h', 'l', 'c']);
      p.setData(d.data);
      p.draw();
    } else {
      throw 'Could not find canvas';
    }
  }).catch((err) => {
    console.log('Could not get chart:', err);
  }); //getChart
