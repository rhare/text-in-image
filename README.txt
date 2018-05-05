Robert Hare

Text in image uses the python Pillow package to encode an 
image's pixels with a message and decode that same image 
to retrieve the message. 


To use: (I used argparse)
	 -- See help menu -- 
	./text_in_image.py --help


	-- Encode an image with text -- 
	./text_in_image.py encode -i img_to_encode.jpg -o encoded_image.png -m "My Message. Use quotes to encapsulate spaces"


	-- Encode an image with text from a file --
	./text_in_image.py encode-file -i img_to_encode.jpg -o encoded_image.png -m text_file.txt


	-- Encode an image with text from a file -- 
	./text_in_image.py encode-file -i img_to_decode.png

