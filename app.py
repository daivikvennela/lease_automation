from flask import Flask, request, jsonify, send_from_directory
from converter import update_json_with_generated_content
import os

app = Flask(__name__, static_folder='web', static_url_path='')


@app.route('/')
def index():
    return send_from_directory('web', 'index.html')


@app.route('/api/process', methods=['POST'])
def process_json():
    try:
        data = request.get_json(force=True, silent=False)
        if not isinstance(data, dict):
            return jsonify({"error": "JSON payload must be an object"}), 400
        result = update_json_with_generated_content(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


