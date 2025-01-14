import os
import uuid
from flask import Flask, request, jsonify, render_template, Response

from controller import process_logic, write_result_json


app = Flask(__name__)

# немного конфигов
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# тут загружается форма для теста
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    allowed_extensions = {'pdf'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "Invalid file type"}), 400

    try:
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = str(uuid.uuid4()) + "." + file_extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        print(file_path)
        file.save(file_path)

        results = []
        result = process_logic(file_path)
        print('result', result)
        results.append(result)
        os.remove(file_path) # подчищаем от мусора

        # Записываем результат в файл
        filename_without_extension = os.path.splitext(file.filename)[0]
        json_filename = filename_without_extension + ".json"
        write_result_json(result, app.config['UPLOAD_FOLDER'], json_filename)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)