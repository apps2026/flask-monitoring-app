from flask import Flask, jsonify
from app.metrics import REQUEST_COUNTER  # Correct import

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

@app.route("/")
def home():
    REQUEST_COUNTER.inc()
    return jsonify({"message": "Hello, Flask with Prometheus!"})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # Must bind to 0.0.0.0 so container is accessible
    app.run(host="0.0.0.0", port=5000)
