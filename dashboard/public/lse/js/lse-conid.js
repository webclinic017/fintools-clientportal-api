// Load API token
var debug = false;
var base = location.href.substring(0, location.href.lastIndexOf("/"));
var kUrlBase = 'https://cloud.iexapis.com/stable/';
var kUrlIb = '/';

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
function getConidApi(ticker) {
  if(ticker == '')
    throw 'Ticker is not set';
  var url = kUrlIb + 'lseconid/' + ticker;
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
