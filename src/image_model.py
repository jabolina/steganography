from PIL import Image
import conversion
import sys
from tqdm import trange


class ImageModel:
    def __init__(self, use_bits=4):
        try:
            self.image = Image.open(sys.argv[2])
            self.hide = Image.open(sys.argv[3])
            self.operate = True
            if self.hide.size[0] > self.image.size[0] and self.hide.size[1] > self.image.size[1]:
                print('Original image small than image to hide.')
                self.operate = False
            self.use_bits = use_bits
            self.original_pixel_matrix = self.create_pixel_matrix(self.image)
            self.hide_pixel_matrix = self.create_pixel_matrix(self.hide)
            self.steg_image = None
            self.steganography_matrix = None
        except FileNotFoundError as ex:
            self.image = None
            self.hide = None
            self.use_bits = use_bits

    def get_original(self):
        return self.image

    def get_hide(self):
        return self.hide

    def create_pixel_matrix(self, image):
        if self.operate:
            return image.load()
        else:
            return None

    def merge_rgb(self, rgb_original, rgb_hide):
        if self.operate:
            ro, go, bo, oo = rgb_original
            rh, gh, bh, oh = rgb_hide

            return (ro[:int(self.use_bits)] + rh[:int(8 - self.use_bits)],
                    go[:int(self.use_bits)] + gh[:int(8 - self.use_bits)],
                    bo[:int(self.use_bits)] + bh[:int(8 - self.use_bits)],
                    oo)
        else:
            return None

    def unmerge_rbg(self, rgb):
        r, g, b, o = rgb
        fill_str = '0000'

        return [(r[:self.use_bits] + fill_str,
                 g[:self.use_bits] + fill_str,
                 b[:self.use_bits] + fill_str,
                 o[:self.use_bits] + fill_str),
                (r[self.use_bits:] + fill_str,
                 g[self.use_bits:] + fill_str,
                 b[self.use_bits:] + fill_str,
                 o[self.use_bits:] + fill_str)]

    def merge_rgb_matrices(self):
        if self.hide_pixel_matrix is not None and self.original_pixel_matrix is not None:
            self.steg_image = self.image
            self.steganography_matrix = self.steg_image.load()
            for i in trange((self.hide.size[0])):
                for j in range((self.hide.size[1])):
                    self.steganography_matrix[i, j] = conversion.bin_to_rgb(self.merge_rgb(
                        conversion.rgb_to_bin(self.original_pixel_matrix[i, j]),
                        conversion.rgb_to_bin(self.hide_pixel_matrix[i, j])))
        else:
            self.steganography_matrix = None

    def create_steg_image(self, path):
        if self.steganography_matrix is not None and self.steg_image is not None:
            try:
                self.steg_image.save(path)
                return True
            except Exception as ex:
                print('Exception occurred')
                print(ex)
                return False

    def reveal_image(self):
        self.steg_image = Image.open(sys.argv[4])
        self.steganography_matrix = self.steg_image.load()
        self.unmerge_rgb_matrices(self.steganography_matrix)

    def unmerge_rgb_matrices(self, steg_matrix):
        if steg_matrix is not None:
            self.image = Image.new(self.steg_image.mode, self.steg_image.size)
            self.hide = Image.new(self.steg_image.mode, self.steg_image.size)

            self.original_pixel_matrix = self.image.load()
            self.hide_pixel_matrix = self.hide.load()
            for i in trange(self.steg_image.size[0]):
                for j in range(self.steg_image.size[1]):
                    separated_rgbs = self.unmerge_rbg(conversion.rgb_to_bin(steg_matrix[i, j]))
                    self.original_pixel_matrix[i, j] = conversion.bin_to_rgb(separated_rgbs[0])
                    self.hide_pixel_matrix[i, j] = conversion.bin_to_rgb(separated_rgbs[1])

            try:
                self.image.save(sys.argv[2])
                self.hide.save(sys.argv[3])
            except Exception as ex:
                print('Exception occurred')
                print(ex)
        else:
            self.original_pixel_matrix = None
            self.hide_pixel_matrix = None
