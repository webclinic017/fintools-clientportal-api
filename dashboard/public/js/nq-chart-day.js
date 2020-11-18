// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = '/';
var kPlotNames = [];
var kPlot = null;
var kTime = '3m';

/* GETTERS */
function getChart(ticker) {
  var url = kUrlIb + 'chart-two-day/' + ticker;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  });
}

function drawPlot() {
    console.log('Drawing');
    ticker = document.getElementById('ticker').value;
    if (ticker != '') {
      getChart(ticker)
        .then((d) => {
          console.log(d);
          var data = {};
          var current = 0;
          var currentDay = 0;
          var days = [];
          var reset = false;
          for(var i = 0; i < d.data.length; i++) {
            // Split into data[0] data[1]
            var t = new Date(d.data[i].t);
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
            data[current].data.push(d.data[i]);
            data[current].averages.push((d.data[i].h+d.data[i].l)/2);
          }
          console.log(data);
          // Get averages
          var j = 0;
          for(var i = 0; i < data[0].averages.length; i++) {
            j += data[0].averages[i];
          }
          var priceAvg = j/data[0].averages.length;
          var priceEntry = priceAvg*(100/102);
          var priceExit = priceAvg*(104/100);
          console.log('Average:', priceAvg);
          console.log('Entry:', priceEntry);
          console.log('Exit:', priceExit);

          // Count changes
          var findLow = true;
          var countFlux = 0;
          for(var i = 0; i < data[0].data.length; i++) {
            var dPoint = data[0].data[i];
            if (findLow) {
              if (dPoint.l <= priceEntry) {
                console.log('FOUND LOW');
                findLow = false;
              }
            } else {
              if (dPoint.h >= priceExit) {
                console.log('FOUND HIGH');
                findLow = true;
                countFlux++;
              }
            }
          }
          console.log('Fluctuations:', countFlux);

          console.log('SECOND DAY')
          var findLow = true;
          var countFlux = 0;
          for(var i = 0; i < data[1].data.length; i++) {
            var dPoint = data[1].data[i];
            if (findLow) {
              if (dPoint.l <= priceEntry) {
                console.log('FOUND LOW:', new Date(dPoint.t));
                findLow = false;
              }
            } else {
              if (dPoint.h >= priceExit) {
                console.log('FOUND HIGH:', new Date(dPoint.t));
                findLow = true;
                countFlux++;
              }
            }
          }
          console.log('Fluctuations:', countFlux);

          // Draw both
          var c = document.getElementById('canvas');
          if (c.getContext) {
            var p = new Plot(c.getContext('2d'));
            //console.log(p);
            p.setLabels(['o', 'h', 'l', 'c']);
            p.setData(data[0].data);
            p.draw();
          } else {
            throw 'Could not find canvas';
          }
          var c = document.getElementById('canvas-two');
          if (c.getContext) {
            var p = new Plot(c.getContext('2d'));
            console.log(p);
            p.setLabels(['o', 'h', 'l', 'c']);
            p.setData(data[1].data);
            p.draw();
          } else {
            throw 'Could not find canvas';
          }
        }).catch((err) => {
          console.log('Could not get chart:', err);
        }); //getChart
    } else {
      alert('Set the ticker');
    }
}

// MAIN
function main() {
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
  // Canvas 2
  var canvas = document.createElement('canvas');
  canvas.id = 'canvas-two';
  canvas.style = 'width:100%; height:50%; display: block;';
  canvas.width = 800;
  canvas.height = 400;
  kPlot.appendChild(canvas);
}
