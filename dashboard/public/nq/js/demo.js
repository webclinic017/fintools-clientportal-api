// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = 'http://localhost:8080/';
var kUrlFilings = 'https://finapi.tk/filings/';
var kPlotNames = [];
var kPlot = null;
var kTime = '3m';

/* GETTERS */
function getDemo(time) {
  if(time == '')
    throw 'Time is not set';
  var url = kUrlIb + 'chartDemo/' + time;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve({ "data": res }); })
      .catch((err) => { reject(err); });
  });
};

function drawPlot(timeRange) {
  // Draw demo ticker for different time ranges
  getDemo(ticker, timeRange)
  .then((d) => {
    var c = document.getElementById('canvas');
    if (c.getContext) {
      var p = new Plot(c.getContext('2d'));
      p.setData(d.data);
      p.draw();
    } else {
      throw 'Could not find canvas';
    }
  }); // getDemo
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
        drawPlot(kTime);
      }
    }
  });

  var kPlot = document.getElementById('plot');
  // Canvas
  var canvas = document.createElement('canvas');
  canvas.id = 'canvas';
  canvas.style = 'width:100%; height:50%; display: block;';
  canvas.width = 800;
  canvas.height = 400;
  kPlot.appendChild(canvas);
}
