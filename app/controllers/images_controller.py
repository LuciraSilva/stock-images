from flask import request, jsonify, safe_join, send_from_directory
from werkzeug.utils import secure_filename
from app.exceptions.images_exceptions import EmptyFolderError, InvalidTypeError, ImageConflictError
import imghdr
import os


ROOT_DIRECTORY = os.getenv('ROOT_DIRECTORY')

SUPPORTED_TYPES = os.getenv('SUPPORTED_TYPES')


def get_images():

    all_images = [images for _, _, images in os.walk(ROOT_DIRECTORY) if len(images) != 0]

    return jsonify(all_images), 200

        
def get_images_by_type(image_type: str):

    try:
        if not image_type in SUPPORTED_TYPES:
            raise InvalidTypeError

        if image_type == 'jpeg':
            image_type = 'jpg'

        images_path = safe_join(ROOT_DIRECTORY, image_type)

        filtered_images = os.listdir(images_path)

        return jsonify(filtered_images), 200

    except InvalidTypeError as e:

        return {'message': str(e)}, 415

def download_image(image_name: str):

    image_type = image_name.split('.')[-1]

    image_path = safe_join(ROOT_DIRECTORY, image_type)
    
    return send_from_directory(directory=f'.{image_path}', path=image_name, as_attachment=True)


def download_zip_images(image_type: str):

    compression_rate = request.args.get('compression_rate', 6, int)

    try:

        if image_type not in SUPPORTED_TYPES:
            raise InvalidTypeError

        if image_type == 'jpeg':
            image_type = 'jpg'

        path = safe_join(ROOT_DIRECTORY, image_type)

        for dirpath, _, images in os.walk(ROOT_DIRECTORY):

            if dirpath.endswith(image_type) and len(images) == 0:

                raise EmptyFolderError

        os.system(f'zip -{compression_rate} -r /tmp/{image_type}.zip {path}')

        return send_from_directory(directory='/tmp', path=f'{image_type}.zip', as_attachment=True)

    except InvalidTypeError as e:

        return {'message': str(e)}, 415

    except EmptyFolderError as e:

        return {'message': str(e)}, 200

    

def upload_image():

    try:

        received_image = request.files['file']

        image_name = secure_filename(received_image.filename)

        image_type = imghdr.what(received_image)


        if image_type not in SUPPORTED_TYPES:
            raise InvalidTypeError

        if image_type == 'jpeg':
            image_type = 'jpg'

        image_path = safe_join('{0}/{1}'.format(ROOT_DIRECTORY, image_type), image_name)


        if os.path.isfile(image_path):
            raise ImageConflictError
   
        received_image.save(image_path)

        return {'message': f'File {image_name} added with successful!'}, 201

    except InvalidTypeError as e:

        return {'message': str(e)}, 415

    except ImageConflictError as e:

        return {'message': str(e)}, 409

    except (SyntaxError, TypeError, IsADirectoryError):

        return {'message': """Failed to upload.\
        Make sure you send the correct data"""}, 406



    
    