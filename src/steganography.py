import sys
import image_model as im


class Steganography:
    def __init__(self, use_bits):
        self.image_model = im.ImageModel(use_bits)

    def hide_image(self):
        self.image_model.create_pixel_matrix(self.image_model.get_original())
        self.image_model.create_pixel_matrix(self.image_model.get_hide())
        self.image_model.merge_rgb_matrices()

        if self.image_model.create_steg_image(str(sys.argv[4])):
            print('Image saved to ' + str(sys.argv[4]))
        else:
            print('Not possible save image.')

    def show_image(self):
        self.image_model.reveal_image()
