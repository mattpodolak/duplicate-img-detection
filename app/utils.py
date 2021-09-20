from io import BytesIO

import faiss
import numpy as np

from imagehash import dhash
from PIL import Image
from faiss import IndexBinaryFlat

def load_index(filename:str = 'faiss_index', hash_size: int = 16) -> IndexBinaryFlat:
    d = hash_size**2
    try:
        return faiss.read_index_binary(f'{filename}_{d}')
    except RuntimeError:
        return faiss.IndexBinaryFlat(d)

def save_index(index: IndexBinaryFlat, filename:str = 'faiss_index', hash_size: int = 16) -> None:
    d = hash_size**2
    faiss.write_index_binary(index, f'{filename}_{d}')

def read_imagefile(data) -> Image.Image:
    image = Image.open(BytesIO(data))
    return image

def hash_image(im: Image, hash_size: int) -> np.ndarray:
    im_hash = dhash(im, hash_size=hash_size)

    # convert image hash from [hash_size, hash_size] binary array 
    # to uint8 [1, hash_size**2] array
    return np.packbits(np.array(im_hash.hash).reshape(1,hash_size**2), axis=1)

def check_duplicate(index: IndexBinaryFlat, img_hash: np.ndarray, thresh: int) -> bool:
    (lims, D, I) = index.range_search(img_hash, thresh)
    return len(D) > 0
