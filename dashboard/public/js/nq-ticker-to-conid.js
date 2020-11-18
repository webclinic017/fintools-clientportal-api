// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = '/';

/* GETTERS */
function getConidApi(ticker) {
  if(ticker == '')
    throw 'Ticker is not set';
  var url = kUrlIb + 'conid/' + ticker;
  return new Promise((resolve, reject) => {
    createRequest('GET', url)
      .then((res) => { resolve(res); })
      .catch((err) => { reject(err); });
  });
}

function getConid() {
    ticker = document.getElementById('ticker').value;
    if (ticker != '') {
      getConidApi(ticker)
        .then((d) => {
          console.log(d);
          var c = document.getElementById('result');
          c.innerHTML = d.conid;
        }).catch((err) => {
          console.log('Could not get conid:', err);
        }); //getChart
    } else {
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
        getConid();
      }
    }
  });
}
