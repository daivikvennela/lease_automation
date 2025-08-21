from flask import Flask, request, jsonify, send_from_directory, send_file
from converter import update_json_with_generated_content, keyValueMapping
from lease_automation import getMapping, simple_document_replacement
import io
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
        enriched = update_json_with_generated_content(data)
        mapping = keyValueMapping(enriched)
        return jsonify({
            "mapping": mapping,
            "enriched_json": enriched
        })
@app.route('/api/generate-docx', methods=['POST'])
def generate_docx():
    try:
        payload = request.get_json(force=True, silent=False)
        if not isinstance(payload, dict):
            return jsonify({"error": "JSON payload must be an object"}), 400

        # Optional override for template path and output filename
        template_path = payload.get('template_path') or 'templates/template.docx'
        output_name = payload.get('output_filename') or 'processed_document.docx'
        track_changes = bool(payload.get('track_changes', False))

        # Build mapping using requested flow: getMapping(update_json_with_generated_content(json_data))
        mapping_list = getMapping(payload)

        # Generate document
        ok, docx_bytes, err = simple_document_replacement(template_path, mapping_list, output_filename=output_name, track_changes=track_changes)
        if not ok:
            return jsonify({"error": err}), 400

        return send_file(io.BytesIO(docx_bytes), as_attachment=True, download_name=output_name, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


