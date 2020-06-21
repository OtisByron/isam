import sys, os
from PIL import Image


def _crop(img, chunk_width, chunk_height):
    img_width, img_height = img.size
    for i in range(img_height//chunk_height):
        for j in range(img_width//chunk_width):
            box = (j*chunk_width, i*chunk_height, (j+1)*chunk_width, (i+1)*chunk_height)
            yield (i, j, img.crop(box))

def split(img_file, output_dir, chunk_width=100, chunk_height=100, quality=75):
    if not os.path.exists(img_file):
        raise Exception('input file does not exist')
    if not os.path.exists(output_dir):
        raise Exception('output directory does not exist')

    img = Image.open(img_file)
    filename = os.path.basename(img_file)
    p = filename.rfind('.')
    name, ext = (filename[:p], filename[p:])

    resize = False
    new_width = img.width
    new_height = img.height
    x_offset = 0
    y_offset = 0

    if img.width % chunk_width != 0:
        new_width = img.width + (chunk_width - (img.width % chunk_width))
        x_offset = (new_width - img.width) // 2
        resize = True
    if img.height % chunk_height != 0:
        new_height = img.height + (chunk_height - (img.height % chunk_height))
        y_offset = (new_height - img.height) // 2
        resize = True

    if resize:
        resized_img = Image.new(img.mode, (new_width, new_height), (255, 255, 255))
        resized_img.paste(img, (x_offset, y_offset))
        img.close()
        img = resized_img

    for chunk in _crop(img, chunk_width, chunk_height):
        row, col, chunk = chunk
        #chunk_img = Image.new(chunk.mode, chunk.size)
        #chunk_img.paste(chunk)
        chunk_filename = name + '-' + str(row) + '+' + str(col) + ext
        save_path = os.path.join(output_dir, chunk_filename)
        chunk.save(save_path, optimize=True, quality=quality)
        del chunk

    img.close()

