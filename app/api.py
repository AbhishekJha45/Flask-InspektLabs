# app/api.py
import os
from flask import request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename

from app import app, auth

api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('file', type=str, location='files')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
@auth.token_required
def uploaded_file(filename):
    return make_response(jsonify({'filename': filename}), 200)

class Upload(Resource):
    @auth.token_required
    def post(self):
        args = parser.parse_args()
        file = args['file']

        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            if file.content_length > app.config['MAX_UPLOAD_SIZE']:
                return jsonify({'message': 'File size exceeds the maximum limit'}), 400

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'message': 'File uploaded successfully'}), 201

api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    app.run(debug=True)
