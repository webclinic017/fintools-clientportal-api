class VolIncrease:
  # Given a list of tickers, return tickers which spiked X% volume within last
  # Y time, e.g. 15% increase from the lowest volume over last 15min.
  def run(self, symbols):
    print('Running on symbols: ' + ' '.join(symbols))
