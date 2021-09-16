from flask import request, jsonify, safe_join, send_from_directory
from werkzeug.utils import secure_filename
import imghdr
import os


ROOT_DIRECTORY = os.getenv('ROOT_DIRECTORY')

SUPPORTED_TYPES = os.getenv('SUPPORTED_TYPES')


def get_images():

    all_images = [images for _, _, images in os.walk(ROOT_DIRECTORY) if len(images) != 0]

    return jsonify(all_images), 200

        
def get_images_by_ext(image_type):

    #TODO: CRIAR EXCEÇÕES, FAZENDO O TIPO ESTOURAR ERRO

    if not image_type in SUPPORTED_TYPES:
        return {'message': 'Formato inválido'}, 415

    images_path = safe_join(ROOT_DIRECTORY, image_type)

    filtered_images = os.listdir(images_path)

    return jsonify(filtered_images), 200


def download_image(image_name: str):
    image_type = image_name.split('.')[-1]

    image_path = safe_join(ROOT_DIRECTORY, image_type)
    
    return send_from_directory(directory=f'.{image_path}', path=image_name, as_attachment=True)


def download_zip_images(image_type: str):
    compression_rate = request.args.get('compression_rate')

    if image_type == 'jpeg':
        image_type = 'jpg'

    path = safe_join(ROOT_DIRECTORY, image_type)

    #TODO: CRIAR EXCEÇÕES FAZENDO ESTOURAR ERRO QUANDO A PASTA ESTIVER VAZIA

    for dirpath, _, images in os.walk(ROOT_DIRECTORY):
         if dirpath.endswith(image_type) and len(images) == 0:
             return {'message': 'pasta vazia'}, 200

    a = os.system(f'zip -{compression_rate} -r /tmp/{image_type}.zip {path}')

    return send_from_directory(directory='/tmp', path=f'{image_type}.zip', as_attachment=True)



def upload_image():

    received_image = request.files['file']

    image_name = secure_filename(received_image.filename)

    image_type = imghdr.what(received_image)


    if image_type == 'jpeg':
        image_type = 'jpg'

    image_path = safe_join('{0}/{1}'.format(ROOT_DIRECTORY, image_type), image_name)
    

    #TODO: COLOCAR EXCEÇÃO DE TIPO

    try:
        if image_type not in SUPPORTED_TYPES:
            return {'message': 'Formato inválido, Tente enviar arquivos jpg, gif ou png'}, 415

        if os.path.isfile(image_path):
            return {'message': 'Arquivo já existente'}, 409
        
        received_image.save(image_path)

        return {'message': f'Arquivo {image_name} adicionado com sucesso!'}, 201

    except (SyntaxError, TypeError, IsADirectoryError):

        return {'message': """Erro ao adicionar arquivo.\
        Certifique-se de que adicionou a chave e o arquivo corretamente"""}, 406




    
    