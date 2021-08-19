from flask import Flask
from kenzie import image
from os import environ
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(environ['MAX_CONTENT_LENGTH'])


@app.get('/')
def home():
    return 'Hey'


@app.get('/files', defaults={'file_type': None})
@app.get('/files/<file_type>')
def get_files(file_type):
    return image.get_files(file_type)


@app.get('/download/<file_name>')
def download_file(file_name: str):
    return image.download_file(file_name)


@app.get('/download-zip')
def download_zip_file():
    return image.download_zip_file()



@app.post('/upload')
def upload_archive():
    return image.upload_image()

