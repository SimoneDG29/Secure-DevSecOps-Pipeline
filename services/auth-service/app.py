from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/auth', methods=['POST'])
def authenticate():
    """
    A simple placeholder for an authentication endpoint.
    In a real application, this would handle user credentials.
    """
    return jsonify({"message": "User authenticated successfully"}), 200

@app.route('/healthz', methods=['GET'])
def health_check():
    """
    A simple health check endpoint.
    """
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)