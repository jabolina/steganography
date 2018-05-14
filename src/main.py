import steganography as Steg
import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Incomplete arguments!')
        exit(0)

    interface = Steg.Steganography(4)

    if str(sys.argv[1]) == 'hide':
        interface.hide_image()
    elif str(sys.argv[1]) == 'show':
        interface.show_image()
    else:
        print('Command not found')
        exit(0)
