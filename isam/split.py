import sys, os
from PIL import Image

# helper function -------------------------------------------------------

# _crop(PIL.Image:img, int:chunk_width, int:chunk_height)
#   img             image to be split
#   chunk_width     width of each chunk in pixels
#   chunk_height    height of each chunk in pixels
#
#   Yield image chunks (to limit memory usage).
#   
#   Returns: tuple(int:row, int:col, PIL.Image:chunk)
#
def _crop(img, chunk_width, chunk_height):
    img_width, img_height = img.size
    # loop through each 'row' of chunks
    for i in range(img_height//chunk_height):
        # loop through each 'column' of chunks
        for j in range(img_width//chunk_width):
            # define a box to crop based on the row, column, and chunk size
            box = (j*chunk_width, i*chunk_height, (j+1)*chunk_width, (i+1)*chunk_height)
            # yield the cropped chunk and row/col info
            yield (i, j, img.crop(box))

# -----------------------------------------------------------------------

# split(str:img_file, str:output_dir, int:chunk_width=100, int:chunk_height=100, int:quality=75)
#   img_file        file path ofimage to be split
#   output_dir      directory path for image chunks
#   chunk_width     width of each chunk in pixels, defaults to 100
#   chunk_height    height of each chunk in pixels, defaults to 100
#   quality         percent jpeg quality of image chunks, defaults to 75
#
#   Load the image, crop it into chunks, and save each chunk as a new image. If the original
#   image size is not divisible by the chunk size, a white margin is added to match the
#   chunk size.
#   
#   Returns: nothing
#
def split(img_file, output_dir, chunk_width=100, chunk_height=100, quality=75):
    # make the sure paths are usable
    if not os.path.exists(img_file):
        raise Exception('input file does not exist')
    if not os.path.exists(output_dir):
        raise Exception('output directory does not exist')

    # open the original image
    img = Image.open(img_file)
    # parse file name info
    filename = os.path.basename(img_file)
    p = filename.rfind('.')
    name, ext = (filename[:p], filename[p:])

    # initialize variables
    resize = False
    new_width = img.width
    new_height = img.height
    x_offset = 0
    y_offset = 0

    # if the original image width is not divisible by the chunk size,
    # the last row/column will be lost
    if img.width % chunk_width != 0:
        # determine how much wider the image has to be to match the
        # chunk size, and how far to offset the image to center it
        new_width = img.width + (chunk_width - (img.width % chunk_width))
        x_offset = (new_width - img.width) // 2
        resize = True
    if img.height % chunk_height != 0:
        # determine how much taller the image has to be to match the
        # chunk size, and how far to offset the image to center it
        new_height = img.height + (chunk_height - (img.height % chunk_height))
        y_offset = (new_height - img.height) // 2
        resize = True

    if resize:
        # create a new image of the required size with a white background
        resized_img = Image.new(img.mode, (new_width, new_height), (255, 255, 255))
        # add the original image
        resized_img.paste(img, (x_offset, y_offset))
        # clean up the original image to conserve memory
        img.close()
        img = resized_img

    # split the image into chunks
    for chunk in _crop(img, chunk_width, chunk_height):
        row, col, chunk = chunk
        # determine the filename of the chunk, including row/col
        chunk_filename = name + '-' + str(row) + '+' + str(col) + ext
        # save the image chunk as a new image
        save_path = os.path.join(output_dir, chunk_filename)
        chunk.save(save_path, optimize=True, quality=quality)
        # remove the chunk to conserve memory
        del chunk

    # clean up the original (or resized) image
    img.close()

