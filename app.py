from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)


# Main application endpoint
@app.route("/")
def home():
    return jsonify({
        "application": "DevOps Challenge API",
        "version": "1.0",
        "status": "running",
        "message": "Hello from Kubernetes!",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


# Health check endpoint
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Readiness check endpoint
@app.route("/ready")
def ready():
    return jsonify({
        "status": "ready"
    }), 200


# Start application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
