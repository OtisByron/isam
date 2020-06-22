# isam (image split and merge)
Python 3 package using PIL to split an image into chunks, and reassemble it. The primary goal is to send jpeg image data over high latency/noise mediums (i.e packet radio) that would benefit from being able to request a retransmit of individual packets/chunks. Developed to minimize memory usage, with the goal of using it on a Raspberry Pi or similar.

### Usage example

    import isam
    image_input_path  = '/home/pi/cat.jpg'
    output_directory = '/tmp'
    isam.split(image_input_path, output_directory)
    
    chunk_directory = '/tmp'
    image_output_path = '/home/pi/cat-merged.jpg'
    isam.merge(chunk_directory, image_output_path)

### Function signatures

    isam.split(image_input_path, output_directory, chunk_width=100, chunk_height=100, quality=75)
    isam.merge(chunk_directory, image_output_path)
    
### Dependencies

Python 3 and pip (if you want to pip install PIL)

    sudo apt install python3 python3-pip

PIL (Pillow), available via pip

    pip3 install PIL
