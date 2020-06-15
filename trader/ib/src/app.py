from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'helloa'

@app.route('/historyforticker')
def history():
  return 'ticker'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
