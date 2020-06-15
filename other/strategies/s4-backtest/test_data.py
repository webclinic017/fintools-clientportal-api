# Read the test_data.json file
import json

def get_history():
  # Return object with json decoded data
  with open('test_data.json', 'r') as f:
    return json.load(f)
