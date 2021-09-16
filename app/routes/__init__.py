from flask import Blueprint

from . import images_blueprint

bp = Blueprint('api_bp', __name__, url_prefix='/api')

bp.register_blueprint(images_blueprint.bp)
