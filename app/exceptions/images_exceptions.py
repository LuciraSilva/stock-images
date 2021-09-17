
class InvalidTypeError(Exception):
    def __init__(self):

        message = 'Invalid type of image'

        super().__init__(message)


class EmptyFolderError(Exception):
    def __init__(self):

        message = 'this folder is empty'

        super().__init__(message)


class ImageConflictError(Exception):
    def __init__(self):

        message = 'image already exists'

        super().__init__(message)