import sys, os
from PIL import Image


def _sort_key(filename):
    key = filename[filename.rfind('-')+1:filename.rfind('.')]
    row, col = key.split('+')
    return int(row + col)

def _files(input_dir):
    # get list of files in input directory
    files = os.listdir(input_dir)
    files = sorted(files, key=_sort_key)
    
    for filename in files:
        key = filename[filename.rfind('-')+1:filename.rfind('.')]
        row, col = key.split('+')
        file_path = os.path.join(input_dir, filename)
        chunk = Image.open(file_path)
        yield (int(row), int(col), chunk)
    
def _file_data(input_dir):
    # get list of files in input directory
    files = os.listdir(input_dir)
    files = sorted(files, key=_sort_key)
    
    # get max rows and cols from last chunk
    filename = files[-1]
    key = filename[filename.rfind('-')+1:filename.rfind('.')]
    row, col = key.split('+')

    # get chunk size from first chunk
    file_path = os.path.join(input_dir, files[0])
    chunk = Image.open(file_path)

    return (int(row)+1, int(col)+1, chunk)


def merge(input_dir, img_file):
    if not os.path.exists(input_dir):
        raise Exception('input directory does not exist')
    
    rows, cols, chunk = _file_data(input_dir)
    img = Image.new(chunk.mode, (cols*chunk.width, rows*chunk.height))
    filename = os.path.basename(chunk.filename)
    filename = filename[:filename.rfind('-')] + filename[filename.rfind('.'):]
    chunk.close()

    for row, col, chunk in _files(input_dir):
        box = (col*chunk.width, row*chunk.height) 
        img.paste(chunk, box)
        chunk.close()

    img.save(img_file, optimize=True, quality=100)
        
