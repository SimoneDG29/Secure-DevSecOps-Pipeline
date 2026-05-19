from flask import Flask, jsonify

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:5173"]}}
)

@app.route('/api', methods=['GET'])
def get_data():
    """
    A simple placeholder for an API endpoint.
    """
    return jsonify({"data": "Hello from api-service"}), 200

@app.route('/healthz', methods=['GET'])
def health_check():
    """
    A simple health check endpoint.
    """
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)