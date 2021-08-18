from flask import jsonify, request, send_from_directory
import os
from app import FILES_DIRECTORY

SUPPORTED_EXTENSIONS = ['jpg', 'png', 'gif']

def get_files(file_type: str):
    if not file_type:
        output_list = [dir_files for _, _, dir_files in os.walk(FILES_DIRECTORY) if len(dir_files) != 0]
        return jsonify(output_list), 200
    elif file_type in SUPPORTED_EXTENSIONS:
        output_list = os.listdir(f'{FILES_DIRECTORY}/{file_type}')
        return jsonify(output_list), 200
    return {'message': 'Formato inválido'}, 415

def upload_image():
    received_file = request.files['file']
    file_name = received_file.filename
    extension_file = file_name.split('.')[-1]

    if len([extension for extension in SUPPORTED_EXTENSIONS if extension_file == extension]) == 0:
        return 'Formato inválido, Tente enviar arquivos jpg, gif ou png', 415
    elif os.path.exists(f'{FILES_DIRECTORY}/{extension_file}/{file_name}'):
        return {'message': 'Arquivo já existente'}, 409

    try:
        path = f'{FILES_DIRECTORY}/{extension_file}'
        file_name = received_file.filename
        received_file.save(f'{path}/{file_name}')
    except (SyntaxError, TypeError, IsADirectoryError):
        return {'message': """Erro ao adicionar arquivo.
        Certifique-se de que adicionou a chave e o arquivo correto"""}, 406
    return {'message': f'Arquivo {file_name} adicionado com sucesso!'}, 201


def download_file(file_name: str):
    extension_file = file_name.split('.')[-1]
    return send_from_directory(directory=f"../files/{extension_file}", path=file_name, as_attachment=True)


def download_zip_file():
    file_type = request.args.get('file_type')
    compression_rate = request.args.get('compression_rate')
    os.system(f"zip -{compression_rate} -r /tmp/imagens.zip {FILES_DIRECTORY}/{file_type}")
    return send_from_directory(directory="/tmp", path='imagens.zip', as_attachment=True)
