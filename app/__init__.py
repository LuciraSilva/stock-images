import os


FILES_DIRECTORY = os.environ['FILES_DIRECTORY']
PNG_DIRECTORY = f'{FILES_DIRECTORY}/png'
JPG_DIRECTORY = f'{FILES_DIRECTORY}/jpg'
GIF_DIRECTORY = f'{FILES_DIRECTORY}/gif'


if not os.path.exists(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY)
    os.mkdir(PNG_DIRECTORY)
    os.mkdir(JPG_DIRECTORY)
    os.mkdir(GIF_DIRECTORY)

