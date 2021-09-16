from app.controllers.images_controller import download_image, download_zip_images, get_images, get_images_by_ext, upload_image

from flask import Blueprint

bp = Blueprint('bp_images', __name__, url_prefix='/images')

bp.get('')(get_images)

bp.get('/<image_type>')(get_images_by_ext)

bp.get('/download/<image_name>')(download_image)

bp.get('/download/<image_type>/zip')(download_zip_images)

bp.post('/upload')(upload_image)
