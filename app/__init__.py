from app import routes
from flask import safe_join
from flask import Flask
import os

app = Flask(__name__)
    
app.config['MAX_CONTENT_LENGTH'] = int(os.environ['MAX_CONTENT_LENGTH'])

app.register_blueprint(routes.bp)


ROOT_DIRECTORY = os.environ['ROOT_DIRECTORY']


if not os.path.exists(ROOT_DIRECTORY):

    PNG_DIRECTORY = safe_join(ROOT_DIRECTORY, 'png')

    JPG_DIRECTORY = safe_join(ROOT_DIRECTORY, 'jpg')

    GIF_DIRECTORY = safe_join(ROOT_DIRECTORY, 'gif')

    os.mkdir(ROOT_DIRECTORY)
    os.mkdir(PNG_DIRECTORY)
    os.mkdir(JPG_DIRECTORY)
    os.mkdir(GIF_DIRECTORY)
