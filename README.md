# text-in-image
CPSC-353 Project - Text in image (Steganography)

## Requirements
1. Python3
2. [Pillow](https://python-pillow.org/)

## Usage
### Encode Image with text

```bash
./text_in_image.py encode -i img_to_encode.jpg -o encoded_image.png -m "My Message. Use quotes to encapsulate spaces"
```

### Encode Image with text read from a text file

```bash
./text_in_image.py encode-file -i img_to_encode.jpg -o encoded_image.png -m text_file.txt
```

### Decode Image

```bash
./text_in_image.py encode-file -i img_to_decode.png
```

### Help menu

```bash
./text_in_image.py --help
```
