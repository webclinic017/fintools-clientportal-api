// Draw a OHLC box/candle
var kCandleWidth = 10;

class Candle {
  constructor(ctx, x, open, high, low, close, width = null) {
    // Check
    if (ctx == null) throw 'Context undefined';
    if (x == null) throw 'X undefined';
    if (open == null) throw 'open undefined';

    // Params
    this.ctx = ctx;
    this.x = x; // X position
    this.open = open;
    this.high = high;
    this.low = low;
    this.close = close;
    // Other
    this.cHeight = ctx.canvas.height;
    this.candleWidth = (width != null)? width : kCandleWidth;
    this.maxY = 100;
    this.minY = 0;
  };

  draw() {
    var c     = this.ctx,
        cw    = this.candleWidth,
        open  = this.open,
        high  = this.high,
        low   = this.low,
        close = this.close,
        H     = this.cHeight,
        MAX   = this.maxY;
    // Candlestick: red/green
    if (close >= open) {
      c.fillStyle = 'rgb(0, 200, 0)'; // green
      var higher = close;
      var lower = open;
    } else {
      c.fillStyle = 'rgb(200, 0, 0)'; // red
      var higher = open;
      var lower = close;
    }
    // Candlestick: draw
    //c.beginPath();
    if (higher == lower) {
      // Open equals close, draw a horiz line instead of a candlestick
      c.beginPath();
      c.strokeStyle = 'rgb(0, 0, 0)'; // black
      c.lineWidth = 2;
      c.moveTo(
        this.x,
        this.translate(higher)
      );
      c.lineTo(
        this.x + this.candleWidth,
        this.translate(higher)
      );
      c.stroke();
    } else {
      // Draw candle box
      c.fillRect(
        this.x,
        this.translate(lower),
        this.candleWidth,
        this.translate(higher) - this.translate(lower)
      );
    }
    // Wick: high
    c.beginPath();
    c.strokeStyle = 'rgb(0, 0, 0)'; // black
    c.lineWidth = 2;
    c.moveTo(
      this.x + this.candleWidth/2,
      this.translate(higher)
    );
    c.lineTo(
      this.x + this.candleWidth/2,
      this.translate(this.high)
    );
    c.stroke();
    // Wick: low
    c.beginPath();
    c.moveTo(
      this.x + this.candleWidth/2,
      this.translate(lower)
    );
    c.lineTo(
      this.x + this.candleWidth/2,
      this.translate(this.low)
    );
    c.stroke();
  };

  translate(y) {
    var H = this.cHeight;
    var MIN = this.minY;
    var MAX = this.maxY;
    return H - H*(y-MIN)/(MAX-MIN);
  };
}; //class Candle

/***** PLOT *****/
class Plot {
  ctx = null;
  data = [];
  dataType = 'array';
  lines = [];
  spacing = 2;
  fLabels = {
    open: "open",
    high: "high",
    low: "low",
    close: "close"
  };

  constructor(ctx) {
    this.ctx = ctx;
  }

  setLabels(labels) {
    // Use this if the JSON data has got fields named other than
    // open,high,low,close, e.g. o,h,l,c
    // INPUT: Array, e.g.
    // [ 'o', 'h', 'l', 'c' ]
    this.fLabels = {
      open: labels[0],
      high: labels[1],
      low: labels[2],
      close: labels[3]
    };
  }

  setData(data, fields = [ 'open', 'high', 'low', 'close' ]) {
    var f = fields;
    // Is data an array of arrays, or key-value pairs
    this.dataType = (Array.isArray(data[0]))? 'array' : 'json';

    // Check required fields present
    [ 'open', 'high', 'low', 'close' ].forEach((i) => {
      if (fields.indexOf(i) == -1) {
        throw 'Required field missing: ' + i;
      }
    })

    // Calculate min and max
    // NB: Optimised to make single if/else decision outside loop
    if (this.dataType == 'array') {
      var hi = data[0][f.indexOf('high')];
      var lo = data[0][f.indexOf('low')];
      for (var i in data) {
        if (data[i][f.indexOf('high')] > hi)
          hi = data[i][f.indexOf('high')];
        if (data[i][f.indexOf('low')] < lo)
          lo = data[i][f.indexOf('low')];
      }
    } else if (this.dataType == 'json') {
      var l = this.fLabels;
      var hi = data[0][l.high];
      var lo = data[0][l.low];
      for (var i in data) {
        if (data[i][l.high] > hi)
          hi = data[i][l.high];
        if (data[i][l.low] < lo)
          lo = data[i][l.low];
      }
    } else {
      throw 'Unknown data type';
    }

    // Calculate spacing based on number of datapoints
    var width = this.ctx.canvas.width;
    this.spacing = width/data.length;

    // Set data
    this.data = data;
    this.fields = fields;
    this.max = hi;
    this.min = lo;
  };

  setLines(lines) {
    this.lines = lines;
  };

  clear() {
    var c = this.ctx;
    c.lineWidth = c.canvas.width/100;
    var width = c.canvas.width;
    var height = c.canvas.height;
    c.clearRect(0, 0, width, height); // Clear
    c.strokeRect(0, 0, width, height); // Bounding box
  }

  draw() {
    this.clear();
    // Draw data
    var f = this.fields;

    // Optimised to make single if/else decision outside loop
    if (this.dataType == 'array') {
      for (var i in this.data) {
        var c = new Candle(this.ctx,
          i*this.spacing,                   // date
          this.data[i][f.indexOf('open')],  // open
          this.data[i][f.indexOf('high')],  // high
          this.data[i][f.indexOf('low')],   // low
          this.data[i][f.indexOf('close')], // close
        );
        c.maxY = this.max;
        c.minY = this.min;
        c.draw();
      }
    } else if (this.dataType == 'json') {
      var l = this.fLabels;
      for (var i in this.data) {
        var c = new Candle(this.ctx,
          i*this.spacing,     // date
          this.data[i][l.open],  // open
          this.data[i][l.high],  // high
          this.data[i][l.low],   // low
          this.data[i][l.close], // close
          (0.8)*this.ctx.canvas.width/this.data.length, // candle width
        );
        c.maxY = this.max;
        c.minY = this.min;
        c.draw();
      }
    } else {
      throw 'Unknown data type';
    }
    // Lines (Optimised to make single if/else decision outside loop)
    if (this.lines.length != 0) {
      var c = this.ctx;
      if(this.dataType == 'array') {
        for (var i in this.lines) {
          if (this.lines[i] != null) {
            // Draw line
            c.setLineDash([5, 3]);/*dashes are 5px and spaces are 3px*/
            c.beginPath();
            c.strokeStyle = 'rgba(0, 0, 100, 0.4)'; // black
            c.lineWidth = 2;
            c.moveTo(i*this.spacing+kCandleWidth/2, 0);
            c.lineTo(i*this.spacing+kCandleWidth/2, c.canvas.height);
            c.stroke();
          }
        }
      } else if (this.dataType == 'json') {
        for (var i in this.data) {
          // Line
          if (this.lines.find((line) => {
            return this.data[i].date == line.date;
          }) != null) {
            // Draw line
            c.save();
            c.setLineDash([5, 3]);/*dashes are 5px and spaces are 3px*/
            c.beginPath();
            c.strokeStyle = 'rgba(0, 0, 100, 0.4)'; // black
            c.lineWidth = 2;
            c.moveTo(i*this.spacing+kCandleWidth/2, 0);
            c.lineTo(i*this.spacing+kCandleWidth/2, c.canvas.height);
            c.stroke();
            c.restore();
          }
        } //for data
      } else {
        throw 'Unknown data type';
      }
    }

  };
}; //class Plot
