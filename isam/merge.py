import sys, os
from PIL import Image

# helper functions -------------------------------------------------------

# _sort_key(str:filename)
#   filename    chunk filename
#
#   Used by sorted() to sort the list of chunk file names.
#
#   Returns: int:key
#
def _sort_key(filename):
    # break down the filename to determine the row/col
    key = filename[filename.rfind('-')+1:filename.rfind('.')]
    row, col = key.split('+')
    # concatenate the row/col before converting to an int
    return int(row + col)

# _files(str:input_dir)
#   input_dir   directory path of image chunks
#
#   Yield image chunks (to limit memory usage).
#
#   Returns: tuple(int:row, int:col, PIL.Image:chunk)
#
def _files(input_dir):
    # get list of files in input directory
    files = os.listdir(input_dir)
    # sort the files based on row/col
    files = sorted(files, key=_sort_key)
    
    for filename in files:
        # break down the filename to determine the row/col
        key = filename[filename.rfind('-')+1:filename.rfind('.')]
        row, col = key.split('+')
        # open the image chunk
        file_path = os.path.join(input_dir, filename)
        chunk = Image.open(file_path)
        # yield the image chunk and row/col info
        yield (int(row), int(col), chunk)

# _file_data(str:input_dir)
#   input_dir   directory path of image chunks
#
#   Get data to initialize merged image.
#
#   Returns: tuple(int:rows, int:cols, PIL.Image:chunk)
#
def _file_data(input_dir):
    # get list of files in input directory
    files = os.listdir(input_dir)
    # sort the files based on row/col
    files = sorted(files, key=_sort_key)
    
    # determine number of rows/cols from the file name of the last chunk
    filename = files[-1]
    key = filename[filename.rfind('-')+1:filename.rfind('.')]
    row, col = key.split('+')
    # open the image chunk
    file_path = os.path.join(input_dir, filename)
    chunk = Image.open(file_path)
    # return the image chunk and rows/cols data
    return (int(row)+1, int(col)+1, chunk)

# ------------------------------------------------------------------------

# merge(str:input_dir, str:img_file)
#   input_dir   directory path of image chunks
#   img_file    output file path for merged image
#
#   Load each image chunk, reassemble the original image, and save it.
#
#   Returns: nothing
#
def merge(input_dir, img_file):
    # make sure paths are usable
    if not os.path.exists(input_dir):
        raise Exception('input directory does not exist')
    img_file_path = os.path.dirname(img_file)
    if not os.path.exists(img_file_path):
        raise Exception('ouput image directory does not exist')
    
    # determine initialization info for merged image
    rows, cols, chunk = _file_data(input_dir)
    # initialize merged image
    img = Image.new(chunk.mode, (cols*chunk.width, rows*chunk.height))
    # save the filename so we can use it later
    filename = os.path.basename(chunk.filename)
    filename = filename[:filename.rfind('-')] + filename[filename.rfind('.'):]
    # clean up the chunk used for initialization
    chunk.close()

    # merge the image chunks
    for row, col, chunk in _files(input_dir):
        # determine the location of the image chunk
        box = (col*chunk.width, row*chunk.height)
        # add the chunk to the merged image
        img.paste(chunk, box)
        # clean up the chunk to conserve memory
        chunk.close()

    # save the merged image
    img.save(img_file, optimize=True, quality=100)
        
