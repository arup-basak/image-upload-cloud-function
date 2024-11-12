from flask import Flask, request, jsonify
from google.cloud import storage
import os

app = Flask(__name__)

BUCKET_NAME = os.environ.get("BUCKET_NAME")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)

        # Upload file to the bucket
        blob.upload_from_file(file, content_type=file.content_type)
        blob.make_public()  # Optional: Make the file public

        return jsonify({
            "message": "File uploaded successfully",
            "file_url": blob.public_url
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
