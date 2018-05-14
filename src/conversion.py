def bytes_to_bits(byte_array):
    bit_array = []

    for byte in byte_array:
        bits = ''.join(f'{byte:b}')

        while len(bits) < 8:
            bits = '0' + bits

        bit_array.append(bits)

    return bit_array


def hex_to_bin(chain):
    return ''.join((bin(int(chain[i:i+2], 16))[2:].zfill(8) for i in range(0, len(chain), 2)))


def rgb_to_bin(rgb):
    try:
        r, g, b, o = rgb
    except Exception:
        r, g, b = rgb
        o = 255

    return ('{0:08b}'.format(r),
            '{0:08b}'.format(g),
            '{0:08b}'.format(b),
            '{0:08b}'.format(o))


def bin_to_rgb(bin):
    try:
        r, g, b, o = bin
    except ValueError:
        r, g, b = bin
        o = '11111111'
    return (int(r, 2),
            int(g, 2),
            int(b, 2),
            int(o, 2))
