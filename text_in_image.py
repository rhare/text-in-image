#!/usr/bin/env python3
# Robert Hare
# CPSC-353
# Projct 1 - Text in Image


from PIL import Image
from math import ceil
import argparse
import sys

def decode(image):
    bits = []
    x, y = image.size
    px = image.load()
    msg_len = get_text_length(image, x, y)
    nbits = msg_len + 33  # First 11 pixels is for msg len
    npixels = ceil(nbits/3.0)  # 3bits per pixel

    if npixels > x * y:
        print('[ERROR] Cannot decode message. Required pixels: {0} - Actual pixels: {1}'.format(npixels, x*y))
        sys.exit(1)

    for i in range(npixels):
        rbit, gbit, bbit = decode_pixel(px[(x-1-i) % x, y-1-(i//x)])
        bits.append(rbit)
        bits.append(gbit)
        bits.append(bbit)
    bstring = ''.join(bits[33:nbits])  # Trim off message length and trailing bits

    if len(bstring) % 8 != 0:
        print('[ERROR] Cannot decode message. Invalid bit string length')
        sys.exit(1)

    # Chunk the long binary string into a list of chars
    char_arr_bstring = [bstring[i:i + 8] for i in range(0, len(bstring), 8)]
    char_arr = [chr(int(c,2)) for c in char_arr_bstring]
    return ''.join(char_arr)


def encode(image, message):
    x, y = image.size
    bmessage = get_binary_message(message)
    bnbits = "{0:032b}".format(len(bmessage))

    # We add one extra bit here to not worry about counting bits when writing the message length
    bstring = "{0}0{1}".format(bnbits, bmessage)
    nbits = len(bstring)
    npixels = ceil(nbits/3.0)  # 3bits per pixel
    px = image.load()

    if npixels > x*y:
        print((
            '[ERROR] Cannot encode message. Message too large or image too small. '
            'Required pixels: {0}  - Available pixels: {1}'
        ).format(npixels, x*y))
        sys.exit(1)
    sent_bits = []
    for i in range(npixels):
        sent_bits.append(bstring[i*3:i*3+3])
        epx = encode_pixel(px[(x-1-i) % x, y-1-(i//x)], bstring[i*3:i*3+3])
        px[(x-1-i) % x, y-1-(i//x)] = epx


def decode_pixel(pixel):
    r, g, b = pixel
    rbit = str(r & 1)
    gbit = str(g & 1)
    bbit = str(b & 1)
    return (rbit, gbit, bbit)


def encode_pixel(pixel, sbits):
    bits = []
    sbits = '{:<03}'.format(sbits)
    for i, bit in enumerate(sbits):
        b = pixel[i] | 1 if int(bit) else pixel[i] & 0xfe
        bits.append(b)
    return tuple(bits)


def get_binary_message(message):
    bstring = ''
    for l in message:
        l_int = ord(l)
        bstring += "{0:08b}".format(l_int)
    return bstring


def get_text_length(image, x, y):
    bits = []
    px = im.load()
    for i in range(11):
        r, g, b = px[x - 1 - i, y - 1]
        rbit = str(r & 1)
        gbit = str(g & 1)
        bbit = str(b & 1)
        bits.append(rbit)
        bits.append(gbit)
        bits.append(bbit)

    bits.pop() # pop 33rd bit
    size = int(''.join(bits), 2)
    return size


def parse_args():
    parser = argparse.ArgumentParser(description='Hide text into a picture ("Steganography")')

    # Action subcommands (encode/decode)
    subparsers = parser.add_subparsers(dest='action', description='Action to perform')
    subparsers.required = True;
    encode_parser = subparsers.add_parser("encode", help="Encode an image with a text message.")
    encode_parser.add_argument('-m', '--message', help='Message to encode image with.', required=True)
    encode_parser.add_argument('-i', '--input-image', help='input image to perform action against', required=True)
    encode_parser.add_argument(
        '-o', 
        '--output-image', 
        help='Output image. Output will be in PNG format.', 
        default='encoded-image.png',
        required=True,
    )

    encode_file_parser = subparsers.add_parser("encode-file", help="Encode an image with text from a text file.")
    encode_file_parser.add_argument('-m', '--message-file', help='Text file to encode image with.', required=True)
    encode_file_parser.add_argument('-i', '--input-image', help='input image to perform action against', required=True)
    encode_file_parser.add_argument(
        '-o', 
        '--output-image', 
        help='Output image. Output will be in PNG format.', 
        default='encoded-image.png',
        required=True,
    )

    decode_parser = subparsers.add_parser("decode", help="Decode an image.")
    decode_parser.add_argument('-i', '--input-image', help='input image to perform action against', required=True)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if args.action == 'encode':
        im = Image.open(args.input_image)
        encode(im, args.message)
        try:
            im.save(args.output_image, 'PNG')
        except IsADirectoryError:
            print("Failed to save image. Output destination is a directory")
    elif args.action == 'encode-file':
        try:
            msg = open(args.message_file).read().strip()
        except:
            print("Failed to read file.")
            sys.exit(1)
        im = Image.open(args.input_image)
        encode(im, msg)
        try:
            im.save(args.output_image, 'PNG')
        except IsADirectoryError:
            print("Failed to save image. Output destination is a directory")
    else:
        im = Image.open(args.input_image)
        msg = decode(im)

        print(msg)

    sys.exit(0)

