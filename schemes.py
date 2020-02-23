from PIL import Image

class TruchetScheme(object):

    def __init__(self, image):
        self.image = image

    def get_size(self):
        return self.image.size

    def get_image(self, i, x, y):
        return self.image

    def __str__(self):
        return 'A standard scheme with no manipulation'

class RotateScheme(TruchetScheme):

    def __init__(self, image, rotation=90):
        super().__init__(image)
        self.rotation = rotation

    def get_image(self, i, x, y):
        return self.image.rotate(self.rotation * i)

    def __str__(self):
        return f'Rotate {self.rotation} every tile placement'
