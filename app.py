import flask

app = flask.Flask(__name__)

@app.route("/")
def hello_world():
  return flask.send_from_directory('.', 'hello.html')

@app.route("/api/v1/greeting", methods=['POST'])
def greeting_api():
  request = flask.request.get_json(silent=True)
  if isinstance(request, dict):
    response = {
      "greeting": "Hello, " + request.get("name", "friend") + "!"
    }
  else:
    response = {
      "error": "Invalid JSON"
    }
  return flask.jsonify(response)
